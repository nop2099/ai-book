---
name: publish
description: Run the full pre-publication checklist — PII scan, tests, security review, dev log, build, deploy, final PII check, git commit and push
---

# Publish

Run this checklist every time we ship. Every step runs; none are optional. If a step fails, stop and fix it before continuing.

Do all content modifications (dev log, fixes, etc.) BEFORE building, deploying, and pushing. The deploy and push happen once at the end, after everything is finalized.

## 1. PII Scan (early)

Scan the working tree for credentials, secrets, and personal data. Block the publish if anything is found.

Patterns to scan for (run each separately if needed):
- `(password|passwd|pwd)\s*[:=]`
- `postgresql://|mysql://|mongodb://|redis://`
- `[A-Za-z0-9_-]{20,}\.apps\.googleusercontent\.com`
- `AIza[0-9A-Za-z_-]{35}`
- `sk-[a-zA-Z0-9]{20,}`
- `Bearer [A-Za-z0-9_-]{20,}`
- `AKIA[0-9A-Z]{16}`
- `ghp_[A-Za-z0-9]{36}`
- `xoxb-[0-9]+-[A-Za-z0-9]+`

Scan tracked file types: `*.md`, `*.html`, `*.py`, `*.sh`, `*.js`, `*.ts`, `*.json`, `*.yaml`, `*.yml`, `*.toml`, `*.env`, `*.cfg`, `*.ini`, `*.conf`.

Exclude gitignored directories (`data/`, `convo/`, `repos/`, `reference/wall-of-data/`, `reference/site/`, `reference/_meta/.venv/`).

Known acceptable matches:
- The PII Scanner slush entry in `worklog.md` describes these patterns — that's documentation, not a leak.
- Example/placeholder credentials in documentation are fine if they're clearly fake.

If real credentials are found: remove them, add the file or directory to `.gitignore` if needed, and restart from step 1.

## 2. Run tests

```bash
cd reference/_meta && .venv/bin/python3 analyze-chapters.py > /dev/null
```

If `analyze-chapters.py` errors out, fix before continuing. Check for any new readability warnings (grade > 12).

## 3. Security review

Scan for common vulnerabilities in any code that changed this session:
- **XSS**: User-controlled content rendered without escaping? Template injection?
- **Command injection**: Shell commands built from user input?
- **Path traversal**: File operations using unsanitized paths?
- **Exposed internals**: Internal hostnames, IPs, file paths that reveal infrastructure?
- **Dependency risks**: New dependencies added? Known vulnerabilities?

Quick scan, not a full audit. Flag anything suspicious and fix it before continuing.

## 4. Update the dev log

If this publish includes meaningful changes (new pages, major content updates, new features), add an entry to `reference/_meta/static/devlog.html` with:
- Today's date
- A title summarizing the changes
- A description paragraph
- Bullet points for specific items

Skip this step if the changes are trivial (typo fixes, minor tweaks).

## 5. Build the site

```bash
bash reference/_meta/build.sh
```

The build must succeed with zero errors. Check the page count — it should match or exceed the previous build. If pages are missing, investigate before deploying.

## 6. Deploy to shapes.exe.xyz

```bash
rsync -avz --delete reference/site/ shapes.exe.xyz:/var/www/html/
```

Verify the deploy succeeded. If rsync fails (SSH, permissions, disk space), fix before continuing.

## 7. Spot-check the live site

After deploy, verify at least two pages load correctly:
- The index page: confirm new cards appear if any were added
- Any page that was modified this session: confirm changes are visible

Use `curl -s -o /dev/null -w "%{http_code}" https://shapes.exe.xyz/` to verify 200 status, or confirm rsync transferred the expected files.

## 8. PII Scan (final)

Run the same PII scan from step 1 one more time. This catches anything introduced during the dev log update or other modifications made between steps 1 and now. If anything new appears, fix it, rebuild (step 5), and redeploy (step 6) before continuing.

## 9. Git commit and push

Stage only the files that changed. Never `git add -A` or `git add .` — name the files explicitly.

```bash
git add <specific files>
git commit -m "<message>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push
```

The commit message should describe what changed and why, not just "publish." If pre-commit hooks fail, fix the issue and create a new commit (never amend).

## Summary

```
1. PII scan (early)  — no credentials in tracked files
2. Tests             — readability analysis passes
3. Security review   — no XSS, injection, or exposed internals
4. Dev log           — entry for meaningful changes
5. Build             — site builds with no errors
6. Deploy            — rsync to shapes.exe.xyz
7. Spot-check        — live pages render correctly
8. PII scan (final)  — one last check after all modifications
9. Git commit + push — named files only, descriptive message
```
