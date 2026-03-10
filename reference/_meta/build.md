# Build Process

## Source
Markdown files in `reference/`. Each file is one topic. That's where content lives.

## Outputs
1. **Static site** — HTML pages with shared CSS. No framework.
2. **Individual skill files** — each page can be read by an AI agent as a standalone skill
3. **PDF** — someday. Pandoc.

## Build steps
1. For each `.md` file in `reference/` (excluding `_meta/`):
   - Convert to HTML via marked/pandoc
   - Wrap in `_meta/template.html`
   - Write to `site/` directory
2. Copy CSS to `site/`
3. Generate index page from frontmatter

## Agentic review
Before publishing, an AI agent reads every page and checks:
- Does it have all required sections (what/why/setup/prompt/verify)?
- Are platform instructions complete (Mac/Win/Linux where applicable)?
- Do the shell commands actually work?
- Does it link back to the right book chapter?
- Is the "how to prompt" section something an agent can actually parse?

## Local preview
```bash
cd site && python3 -m http.server 8000
```
