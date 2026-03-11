---
name: publish
description: Run the full pre-publication checklist — PII scan, tests, security review, dev log, build, link check, spot-check, final PII check, deploy, git commit and push
---

# Publish

Run this checklist every time we ship. Every step runs; none are optional. If a step fails, stop and fix it before continuing.

Do all content modifications (dev log, fixes, etc.) BEFORE building, deploying, and pushing. Validate everything BEFORE deploying. The deploy and push happen once at the end, after everything is finalized and verified.

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

## 6. Link check

Crawl the built site for broken internal links. For every HTML file in `reference/site/`, extract all `href` attributes that point to local files (not `http://`, `https://`, `mailto:`, or `#` anchors). Verify each target file exists in `reference/site/`.

```bash
cd reference/site && python3 -c "
import os, re
broken = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if not f.endswith('.html'): continue
        fpath = os.path.join(root, f)
        with open(fpath) as fh:
            content = fh.read()
        for m in re.finditer(r'href=\"([^\"]+)\"', content):
            href = m.group(1)
            if href.startswith(('http://', 'https://', 'mailto:', '#', 'javascript:')): continue
            target = os.path.normpath(os.path.join(os.path.dirname(fpath), href.split('#')[0]))
            if target and not os.path.exists(target):
                broken.append(f'{fpath} -> {href}')
for b in broken: print(f'BROKEN: {b}')
if not broken: print('All links OK')
"
```

If broken links are found, fix the source files (in `reference/_meta/static/` or markdown sources), rebuild, and recheck before continuing. Common causes: numbered file prefixes (`30-chatbot.html` vs `chatbot.html`), renamed pages, missing pages that are referenced but not yet written.

## 7. Spot-check the built site

Before deploying, verify a few built pages render correctly:
- The index page: confirm new cards appear if any were added
- Any page that was modified this session: confirm changes are visible
- The dev log: confirm new entries show up

## 8. PII Scan (final)

Run the same PII scan from step 1 one more time. This catches anything introduced during the dev log update or other modifications made between steps 1 and now. If anything new appears, fix it and rebuild (step 5) before continuing. Nothing leaves the machine until this passes.

## 9. Review outstanding local changes

Before deploying or committing, review the whole working tree:

```bash
git status --short
```

Do not assume every pre-existing local change is unrelated. Explicitly sort outstanding changes into three buckets:
- **Belongs in this publish**: related, complete, validated, and should ship now. Read it, test it if needed, and include it.
- **Important but not ready / unclear**: meaningful work that might belong in the publish, but you are not sure it is complete or intended. Stop and ask the user instead of silently omitting it.
- **Clearly unrelated**: leave it out, but mention it in the final publish summary.

Important rule: do not let meaningful local work get stranded just because it predated the current task. The publish skill must make a conscious decision about it.

Examples of changes that often deserve a second look:
- New folders like `flywheel/`, `ops/`, or other project scaffolds
- Modified guide pages that affect the same release theme
- Unpublished static page edits already sitting in the tree
- Support files that the new pages depend on

## 10. Deploy to shapes.exe.xyz

```bash
rsync -avz --delete reference/site/ shapes.exe.xyz:/var/www/html/
```

Verify the deploy succeeded. If rsync fails (SSH, permissions, disk space), fix before continuing. Use `curl -s -o /dev/null -w "%{http_code}" https://shapes.exe.xyz/` to confirm 200.

## 11. Git commit and push

Stage only the files that changed. Never `git add -A` or `git add .` — name the files explicitly.

```bash
git add <specific files>
git commit -m "<message>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push
```

The commit message should describe what changed and why, not just "publish." If pre-commit hooks fail, fix the issue and create a new commit (never amend).

When staging, include all validated files that belong in this publish — including important local changes discovered in step 9. Do not quietly stage only the newest diff if older related work is part of the release.

## Summary

```
 1. PII scan (early)  — no credentials in tracked files
 2. Tests             — readability analysis passes
 3. Security review   — no XSS, injection, or exposed internals
 4. Dev log           — entry for meaningful changes
 5. Build             — site builds with no errors
 6. Link check        — no broken internal hrefs in built site
 7. Spot-check        — built pages render correctly
 8. PII scan (final)  — one last check before anything leaves the machine
 9. Review tree       — sort outstanding changes into include / ask / leave-out
10. Deploy            — rsync to shapes.exe.xyz
11. Git commit + push — named files only, descriptive message
```
