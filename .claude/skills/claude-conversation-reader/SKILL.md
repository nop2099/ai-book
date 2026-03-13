---
name: claude-conversation-reader
description: Read, tail, and summarize Claude Code conversation JSONL files. Use when asked to inspect what happened in a Claude session, find the latest Claude conversation for the current repo, pull recent user turns, follow a live conversation, or explain Claude's tool/edit history.
---

# Claude Conversation Reader

Claude conversations usually do not live in the repo-local `.claude/` folder. That folder often holds only settings and skills. The actual session logs usually live in `~/.claude/projects/<sanitized-cwd>/` as root `*.jsonl` files, with subagent logs under `subagents/`.

## Use This Skill When

- The user says "read the Claude conversation," "tail the conversation," or "what's going on in Claude?"
- You need the latest Claude session for the current repo.
- You need to separate the real thread from tool noise, progress hooks, or file-history snapshots.
- You need to explain what Claude changed, what the user corrected, and what is still unresolved.

## Workflow

### 1. Resolve the project session store

Use the helper script:

```bash
python3 SKILL_DIR/scripts/find_latest_session.py
```

This prints the newest root session file for the current working directory. Use `--list` to see the recent sessions instead of just the newest one.

If the repo-local `.claude/` has no `jsonl` files, check `~/.claude/projects/` before assuming there is no conversation.

### 2. Read signal before raw tail

Start with the cleaned summary:

```bash
SESSION=$(python3 SKILL_DIR/scripts/find_latest_session.py)
python3 SKILL_DIR/scripts/recent_signal.py "$SESSION" --limit 25
```

This filters out most noise and shows the recent user and assistant text turns. Use `--include-tools` when the tool calls themselves matter.

### 3. Pull the thread shape

When summarizing, extract these five things:

1. The current user objective
2. What Claude actually changed or proposed
3. Where the user corrected or redirected the work
4. Any mistaken action or risky assumption
5. The current open question or next decision

This is usually more useful than narrating every tool call.

### 4. Tail live only after you know the file

```bash
tail -n 30 -f "$SESSION"
```

Use the cleaned reader first, then raw `tail -f` only to watch new events arrive in real time.

### 5. Check supporting evidence when needed

- Root session file: the main conversation
- `subagents/*.jsonl`: delegated side threads
- `tool-results/`: raw command output captured by Claude
- `file-history/`: snapshots of changed files during the session

If the user asks "what did Claude do?" do not stop at assistant prose. Check the file-history snapshot and relevant tool results.

## How To Read The JSONL

Useful record types:

- `type:"user"`: main user turns and tool results returned to Claude
- `type:"assistant"`: Claude responses, including text and tool-use blocks
- `type:"progress"`: hook noise; usually skip
- `type:"system"`: timing and harness events; usually skip
- `type:"file-history-snapshot"`: what files changed during the turn

Important details:

- Root session files are the top-level `UUID.jsonl` files in the project directory. Do not confuse them with `subagents/*.jsonl`.
- Timestamps are usually ISO UTC (`...Z`). Use exact dates and times when summarizing.
- `cwd` can shift during a session if Claude `cd`s into a build or output directory. The session still belongs to the same root file.
- Tool results often appear as `type:"user"` records because the harness feeds them back into Claude as user content.

## Quick Commands

Recent user turns only:

```bash
SESSION=$(python3 SKILL_DIR/scripts/find_latest_session.py)
python3 SKILL_DIR/scripts/recent_signal.py "$SESSION" --limit 20 --users-only
```

Recent turns including tool-use summaries:

```bash
SESSION=$(python3 SKILL_DIR/scripts/find_latest_session.py)
python3 SKILL_DIR/scripts/recent_signal.py "$SESSION" --limit 30 --include-tools
```

List recent sessions for this repo:

```bash
python3 SKILL_DIR/scripts/find_latest_session.py --list
```

## Reporting Style

When the user wants "what's going on," do not dump raw JSONL unless they ask for it. Give:

- the active session file
- the latest meaningful topic
- the last correction or redirect from the user
- the concrete files Claude touched
- the current unresolved question

The point is to surface the conversation's shape, not just its exhaust.
