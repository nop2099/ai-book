---
name: publish
description: Run the full pre-publication checklist — PII scan, tests, build, deploy, security review, git commit, dev log update
---

# Publish

Run this checklist every time we ship. Every step runs; none are optional. If a step fails, stop and fix it before continuing.

## 1. PII Scan

Scan the working tree for credentials, secrets, and personal data. Block the publish if anything is found.

```bash
grep -rn --include='*.md' --include='*.html' --include='*.py' --include='*.sh' --include='*.js' --include='*.ts' --include='*.json' --include='*.yaml' --include='*.yml' --include='*.toml' --include='*.env' --include='*.cfg' --include='*.ini' --include='*.conf' -E '(password|passwd|pwd)\s*[:=]' -E 'postgresql://|mysql://|mongodb://|redis://' -E '[A-Za-z0-9_-]{20,}\.apps\.googleusercontent\.com' -E 'AIza[0-9A-Za-z_-]{35}' -E 'sk-[a-zA-Z0-9]{20,}' -E 'Bearer [A-Za-z0-9_-]{20,}' -E 'AKIA[0-9A-Z]{16}' -E 'ghp_[A-Za-z0-9]{36}' -E 'xoxb-[0-9]+-[A-Za-z0-9]+' .
```

Run each pattern separately if needed. Exclude gitignored directories (`data/`, `convo/`, `repos/`, `reference/wall-of-data/`, `reference/site/`, `reference/_meta/.venv/`). Known acceptable matches:
- The PII Scanner slush entry in `worklog.md` describes these patterns — that's documentation, not a leak.
- Example/placeholder credentials in documentation are fine if they're clearly fake.

If real credentials are found: remove them, add the file or directory to `.gitignore` if needed, and restart from step 1.

## 2. Run tests

```bash
# Chapter readability analysis
cd reference/_meta && .venv/bin/python3 analyze-chapters.py > /dev/null
```

If `analyze-chapters.py` errors out, fix before continuing. Check for any new readability warnings (grade > 12).

## 3. Build the site

```bash
bash reference/_meta/build.sh
```

The build must succeed with zero errors. Check the page count — it should match or exceed the previous build. If pages are missing, investigate before deploying.

## 4. Deploy to shapes.exe.xyz

```bash
rsync -avz --delete reference/site/ shapes.exe.xyz:/var/www/html/
```

Verify the deploy succeeded. If rsync fails (SSH, permissions, disk space), fix before continuing.

## 5. Spot-check the live site

After deploy, verify at least two pages load correctly:
- The index page: confirm new cards appear if any were added
- Any page that was modified this session: confirm changes are visible

You can use `curl -s -o /dev/null -w "%{http_code}" https://shapes.exe.xyz/` to verify 200 status, or just confirm rsync transferred the expected files.

## 6. Security review

Scan for common vulnerabilities in any code that changed:
- **XSS**: User-controlled content rendered without escaping? Template injection?
- **Command injection**: Shell commands built from user input?
- **Path traversal**: File operations using unsanitized paths?
- **Exposed internals**: Internal hostnames, IPs, file paths that reveal infrastructure?
- **Dependency risks**: New dependencies added? Known vulnerabilities?

This is a quick scan, not a full audit. Flag anything suspicious and fix it. For static HTML pages, the main risks are XSS in any JavaScript and exposed infrastructure details.

## 7. Git commit and push

Stage only the files that changed. Never `git add -A` or `git add .` — name the files explicitly.

```bash
git add <specific files>
git commit -m "<message>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push
```

The commit message should describe what changed and why, not just "publish." If pre-commit hooks fail, fix the issue and create a new commit (never amend).

## 8. Update the dev log

If this publish includes meaningful changes (new pages, major content updates, new features), add an entry to `reference/_meta/static/devlog.html` with:
- Today's date
- A title summarizing the changes
- A description paragraph
- Bullet points for specific items

Then re-run steps 3-4 (build and deploy) to push the updated dev log live. Step 7 (commit) can wait until the end — batch the dev log commit with other work if more is coming.

## Summary

```
1. PII scan          — no credentials in tracked files
2. Tests             — readability analysis passes
3. Build             — site builds with no errors
4. Deploy            — rsync to shapes.exe.xyz
5. Spot-check        — live pages render correctly
6. Security review   — no XSS, injection, or exposed internals
7. Git commit + push — named files only, descriptive message
8. Dev log           — entry for meaningful changes, rebuild + redeploy
```
