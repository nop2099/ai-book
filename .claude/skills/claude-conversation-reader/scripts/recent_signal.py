#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def load_records(session_path: Path):
    with session_path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def flatten_text(value):
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = []
        for item in value:
            if not isinstance(item, dict):
                continue
            item_type = item.get("type")
            if item_type == "text":
                text = item.get("text", "").strip()
                if text:
                    parts.append(text)
            elif item_type == "tool_result":
                content = item.get("content", "")
                if isinstance(content, str) and content.strip():
                    parts.append(f"[tool_result] {content.strip()}")
        return "\n".join(parts).strip()
    return ""


def assistant_chunks(record, include_tools):
    message = record.get("message", {})
    content = message.get("content")
    if isinstance(content, str):
        text = content.strip()
        if text:
            yield ("assistant", text)
        return
    if not isinstance(content, list):
        return
    for item in content:
        if not isinstance(item, dict):
            continue
        item_type = item.get("type")
        if item_type == "text":
            text = item.get("text", "").strip()
            if text:
                yield ("assistant", text)
        elif include_tools and item_type == "tool_use":
            name = item.get("name", "tool")
            tool_input = item.get("input", {})
            summary = ""
            if isinstance(tool_input, dict):
                summary = tool_input.get("description") or tool_input.get("command") or ""
            summary = str(summary).strip()
            line = f"[tool] {name}"
            if summary:
                line += f": {summary}"
            yield ("assistant", line)


def extract_signal(record, include_tools=False):
    record_type = record.get("type")
    ts = record.get("timestamp", "")
    if record_type == "user":
        message = record.get("message", {})
        text = flatten_text(message.get("content"))
        if text:
            return [(ts, "user", text)]
        return []
    if record_type == "assistant":
        return [(ts, role, text) for role, text in assistant_chunks(record, include_tools)]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print recent high-signal Claude conversation turns from a session JSONL."
    )
    parser.add_argument("session_path", help="Path to a root Claude session JSONL file.")
    parser.add_argument("--limit", type=int, default=20, help="Number of signal items to print.")
    parser.add_argument(
        "--users-only",
        action="store_true",
        help="Print only user turns and tool results.",
    )
    parser.add_argument(
        "--include-tools",
        action="store_true",
        help="Include assistant tool-use summaries.",
    )
    args = parser.parse_args()

    session_path = Path(args.session_path)
    if not session_path.is_file():
        print(f"error: session file not found: {session_path}", file=sys.stderr)
        return 1

    signal = []
    for record in load_records(session_path):
        signal.extend(extract_signal(record, include_tools=args.include_tools))

    if args.users_only:
        signal = [item for item in signal if item[1] == "user"]

    for ts, role, text in signal[-args.limit :]:
        print(f"[{ts}] {role}")
        print(text)
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
