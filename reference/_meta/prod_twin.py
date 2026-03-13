#!/usr/bin/env python3
"""
Production-twin static server for the built site.

Mirrors the current shapes.exe.xyz nginx behavior:
- root reference/site
- index index.html
- slug-map.conf aliases
- if ($slug_rewrite) rewrite ^ $slug_rewrite last;
- location / { try_files $uri $uri.html $uri/ =404; }
"""

from __future__ import annotations

import argparse
import contextlib
import mimetypes
import socket
import threading
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


def parse_slug_map(slug_map_path: Path) -> dict[str, str]:
    aliases: dict[str, str] = {}
    if not slug_map_path.exists():
        return aliases

    for line in slug_map_path.read_text().splitlines():
        line = line.strip()
        if not line.startswith("/") or not line.endswith(";"):
            continue
        src, target = line[:-1].split(None, 1)
        aliases[src] = target
    return aliases


@dataclass(frozen=True)
class ResolvedPath:
    request_path: str
    filesystem_path: Path


class ProdTwinApp:
    def __init__(self, site_dir: Path):
        self.site_dir = site_dir.resolve()
        self.slug_map = parse_slug_map(self.site_dir / "slug-map.conf")

    def resolve(self, raw_target: str) -> ResolvedPath | None:
        path = unquote(urlsplit(raw_target).path or "/")
        if not path.startswith("/"):
            path = "/" + path

        rewritten = self.slug_map.get(path, path)
        for candidate in self._candidate_paths(rewritten):
            if candidate.is_file():
                return ResolvedPath(request_path=rewritten, filesystem_path=candidate)
            if candidate.is_dir():
                index_path = candidate / "index.html"
                if index_path.is_file():
                    return ResolvedPath(request_path=rewritten, filesystem_path=index_path)
        return None

    def _candidate_paths(self, request_path: str) -> list[Path]:
        relative = request_path.lstrip("/")
        candidates = [
            self.site_dir / relative,
            self.site_dir / f"{relative}.html",
            self.site_dir / relative / "",
        ]

        safe_candidates: list[Path] = []
        for candidate in candidates:
            resolved = candidate.resolve()
            if self.site_dir == resolved or self.site_dir in resolved.parents:
                safe_candidates.append(resolved)
        return safe_candidates


class ProdTwinHandler(BaseHTTPRequestHandler):
    server_version = "ProdTwin/1.0"

    def log_message(self, fmt: str, *args: object) -> None:
        return

    def do_HEAD(self) -> None:  # noqa: N802
        self._serve(send_body=False)

    def do_GET(self) -> None:  # noqa: N802
        self._serve(send_body=True)

    def _serve(self, send_body: bool) -> None:
        app: ProdTwinApp = self.server.app  # type: ignore[attr-defined]
        resolved = app.resolve(self.path)
        if not resolved:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return

        body = resolved.filesystem_path.read_bytes()
        content_type, _ = mimetypes.guess_type(str(resolved.filesystem_path))
        if resolved.filesystem_path.suffix == ".conf":
            content_type = "text/plain; charset=utf-8"
        if resolved.filesystem_path.suffix == ".json":
            content_type = "application/json; charset=utf-8"

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.end_headers()
        if send_body:
            self.wfile.write(body)


def make_server(site_dir: Path, host: str, port: int) -> ThreadingHTTPServer:
    app = ProdTwinApp(site_dir)
    server = ThreadingHTTPServer((host, port), ProdTwinHandler)
    server.app = app  # type: ignore[attr-defined]
    return server


@contextlib.contextmanager
def run_server(site_dir: Path, host: str = "127.0.0.1", port: int = 8000):
    server = make_server(site_dir, host, port)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def find_free_port(host: str = "127.0.0.1") -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1])


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve reference/site with prod-twin routing.")
    parser.add_argument("site_dir", nargs="?", default="reference/site")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    site_dir = Path(args.site_dir)
    if not site_dir.is_dir():
        raise SystemExit(f"Site directory not found: {site_dir}")

    server = make_server(site_dir, args.host, args.port)
    print(f"Prod twin serving {site_dir.resolve()} at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
