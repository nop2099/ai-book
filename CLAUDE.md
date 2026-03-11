# Shapes of Intelligence — Project Instructions

## JSONL / JSON processing
- Prefer `jq` over Python for JSONL inspection, extraction, and filtering
- Use `jq` streaming (no `-s`) for large files, `-s` (slurp) only when you need cross-record operations
- Common patterns:
  - Extract messages: `jq 'select(.type == "message") | .message' file.jsonl`
  - Filter by role: `jq 'select(.message.role == "human")' file.jsonl`
  - Count records: `jq -s 'length' file.jsonl`
- Fall back to Python only when you need complex aggregation, cross-referencing, or rendering
