#!/usr/bin/env python3
"""
Validate internal links and route aliases for the built reference site.

Usage:
  python3 reference/_meta/check-site-links.py [reference/site]
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlsplit

HREF_RE = re.compile(r'href=["\']([^"\']+)["\']')


def short_slug(slug: str) -> str:
    return re.sub(r"^[0-9]+[a-z]*-", "", slug)


def part_short_slug(part: str) -> str:
    return re.sub(r"^[0-9]+-", "", part)


def route_variants(rel_path: Path) -> set[str]:
    route = "/" + rel_path.as_posix()
    variants = {route}
    if route.endswith(".html"):
        no_ext = route[:-5]
        variants.add(no_ext)
        if rel_path.name == "index.html":
            parent = "/" + rel_path.parent.as_posix() if rel_path.parent != Path(".") else ""
            variants.add("/index" if not parent else f"{parent}/index")
            variants.add("/" if not parent else parent)
            variants.add("/" if not parent else f"{parent}/")
    return variants


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


def build_route_index(site_dir: Path) -> tuple[set[str], dict[Path, set[str]], dict[str, str]]:
    valid_routes: set[str] = set()
    routes_by_file: dict[Path, set[str]] = {}

    for path in site_dir.rglob("*"):
        if path.is_dir():
            continue
        rel_path = path.relative_to(site_dir)
        variants = route_variants(rel_path)
        valid_routes.update(variants)
        routes_by_file[rel_path] = variants

    aliases = parse_slug_map(site_dir / "slug-map.conf")
    for src, target in aliases.items():
        valid_routes.add(src)
        rel_target = Path(target.lstrip("/"))
        if rel_target in routes_by_file:
            routes_by_file[rel_target].add(src)

    return valid_routes, routes_by_file, aliases


def check_slug_aliases(site_dir: Path, aliases: dict[str, str]) -> list[str]:
    errors: list[str] = []
    reserved_root_routes = set()

    for path in site_dir.iterdir():
        if path.name in {"book", "slug-map.conf"} or path.is_dir():
            continue
        for route in route_variants(Path(path.name)):
            reserved_root_routes.add(route)

    for chapter_path in sorted((site_dir / "book").glob("*/*.html")):
        part = chapter_path.parent.name
        file_stem = chapter_path.stem
        short = short_slug(file_stem)
        part_short = part_short_slug(part)
        target = f"/book/{part}/{chapter_path.name}"

        required = [
            f"/book/{short}",
            f"/book/{short}.html",
            f"/book/{part_short}/{short}",
            f"/book/{part_short}/{short}.html",
            f"/book/{part}/{short}",
            f"/book/{part}/{short}.html",
        ]

        if f"/{short}" not in reserved_root_routes and f"/{short}.html" not in reserved_root_routes:
            required.extend([f"/{short}", f"/{short}.html"])

        for route in required:
            actual = aliases.get(route)
            if actual != target:
                errors.append(f"Missing or wrong slug alias: {route} -> {target}")

    return errors


def iter_supported_entry_routes(rel_path: Path, routes_for_file: set[str]) -> list[str]:
    if rel_path.parts[:1] == ("book",) and len(rel_path.parts) == 3 and rel_path.suffix == ".html":
        # Exercise the canonical numbered path, the short /book alias, and the root alias if present.
        preferred = []
        for route in sorted(routes_for_file):
            if route.startswith("/book/"):
                preferred.append(route)
        for route in sorted(routes_for_file):
            if route.startswith("/") and not route.startswith("/book/"):
                preferred.append(route)
        return preferred or sorted(routes_for_file)
    return sorted(routes_for_file)


def check_internal_links(site_dir: Path, valid_routes: set[str], routes_by_file: dict[Path, set[str]]) -> list[str]:
    errors: list[str] = []

    for rel_path, entry_routes in sorted(routes_by_file.items()):
        if rel_path.suffix != ".html":
            continue
        text = (site_dir / rel_path).read_text()
        hrefs = HREF_RE.findall(text)

        for href in hrefs:
            if href.startswith(("http://", "https://", "mailto:", "javascript:", "#")):
                continue

            for entry in iter_supported_entry_routes(rel_path, entry_routes):
                resolved = urljoin(entry, href)
                path = urlsplit(resolved).path
                if path not in valid_routes:
                    errors.append(
                        f"{rel_path.as_posix()} @ {entry} -> {href} -> {path}"
                    )

    return errors


def main() -> int:
    site_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("reference/site")
    if not site_dir.is_dir():
        print(f"Site directory not found: {site_dir}", file=sys.stderr)
        return 1

    valid_routes, routes_by_file, aliases = build_route_index(site_dir)
    alias_errors = check_slug_aliases(site_dir, aliases)
    link_errors = check_internal_links(site_dir, valid_routes, routes_by_file)
    errors = alias_errors + link_errors

    if errors:
        for error in errors:
            print(error)
        print(f"FAILED: {len(errors)} route/link errors", file=sys.stderr)
        return 1

    total_hrefs = 0
    for rel_path in routes_by_file:
        if rel_path.suffix != ".html":
            continue
        total_hrefs += len(HREF_RE.findall((site_dir / rel_path).read_text()))

    print(
        f"OK: {len(routes_by_file)} files, {len(valid_routes)} routes, {len(aliases)} aliases, {total_hrefs} hrefs checked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
