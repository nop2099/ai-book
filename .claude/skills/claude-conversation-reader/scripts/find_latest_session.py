#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path


def sanitize_project_path(project_path: Path) -> str:
    return str(project_path.resolve()).replace(os.sep, "-")


def find_project_dir(project_path: Path) -> Path:
    project_key = sanitize_project_path(project_path)
    return Path.home() / ".claude" / "projects" / project_key


def list_root_sessions(project_dir: Path) -> list[Path]:
    if not project_dir.is_dir():
        return []
    return sorted(
        [p for p in project_dir.glob("*.jsonl") if p.is_file()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def fmt_mtime(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find Claude session JSONL files for the current repo."
    )
    parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Project path to resolve into ~/.claude/projects/<sanitized-cwd>/",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List recent root session files instead of printing only the newest one.",
    )
    args = parser.parse_args()

    project_path = Path(args.project_path)
    project_dir = find_project_dir(project_path)
    sessions = list_root_sessions(project_dir)

    if not project_dir.exists():
        print(
            f"error: no Claude project store for {project_path.resolve()} at {project_dir}",
            file=sys.stderr,
        )
        return 1

    if not sessions:
        print(f"error: no root session jsonl files in {project_dir}", file=sys.stderr)
        return 1

    if args.list:
        for session in sessions:
            print(f"{fmt_mtime(session)} {session}")
        return 0

    print(sessions[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
