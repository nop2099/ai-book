#!/usr/bin/env python3
"""
HTTP-check the built site against the production-twin routing rules.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from urllib.request import Request, urlopen

from prod_twin import find_free_port, run_server


def load_check_site_links_module():
    script_path = Path(__file__).with_name("check-site-links.py")
    spec = importlib.util.spec_from_file_location("check_site_links", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    site_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("reference/site")
    if not site_dir.is_dir():
        print(f"Site directory not found: {site_dir}", file=sys.stderr)
        return 1

    check_site_links = load_check_site_links_module()
    valid_routes, _, _ = check_site_links.build_route_index(site_dir)
    test_routes = sorted(
        route for route in valid_routes
        if route != "/slug-map.conf"
    )

    host = "127.0.0.1"
    port = find_free_port(host)
    failures: list[str] = []

    with run_server(site_dir, host=host, port=port):
        for route in test_routes:
            url = f"http://{host}:{port}{route}"
            try:
                with urlopen(Request(url, method="HEAD")) as response:
                    status = response.status
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{route}: {exc}")
                continue

            if status != 200:
                failures.append(f"{route}: {status}")

    if failures:
        for failure in failures:
            print(failure)
        print(f"FAILED: {len(failures)} prod-twin HTTP checks", file=sys.stderr)
        return 1

    print(f"OK: {len(test_routes)} prod-twin HTTP checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
