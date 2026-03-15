# Shapes of Intelligence — Project Instructions

## Site editing — CRITICAL
- **NEVER edit files in `reference/site/` directly.** The build script (`reference/_meta/build.sh`) overwrites `reference/site/` on every build. Edits to `reference/site/` WILL be lost.
- **Edit static HTML pages in `reference/_meta/static/`.** The build copies these to `reference/site/`.
- **Edit markdown content in `reference/*.md`.** The build converts these to HTML.
- **MP3s and other assets go in `reference/_meta/static/`.** They survive the build.
- After editing, run `bash reference/_meta/build.sh` to rebuild, then deploy.

## JSONL / JSON processing
- Prefer `jq` over Python for JSONL inspection, extraction, and filtering
- Use `jq` streaming (no `-s`) for large files, `-s` (slurp) only when you need cross-record operations
- Common patterns:
  - Extract messages: `jq 'select(.type == "message") | .message' file.jsonl`
  - Filter by role: `jq 'select(.message.role == "human")' file.jsonl`
  - Count records: `jq -s 'length' file.jsonl`
- Fall back to Python only when you need complex aggregation, cross-referencing, or rendering
