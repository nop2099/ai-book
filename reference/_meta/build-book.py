#!/usr/bin/env python3
"""
Build book chapters into HTML pages for the reference site.
Usage: python3 reference/_meta/build-book.py

Generates:
  reference/site/book/index.html       — table of contents
  reference/site/book/<part>/<ch>.html  — individual chapters
  reference/site/book/full.html         — full text (all chapters)
"""

import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(SCRIPT_DIR))
CHAPTERS_DIR = os.path.join(REPO, "chapters")
SITE_DIR = os.path.join(REPO, "reference", "site", "book")

PART_ORDER = [
    "00-front-matter",
    "01-learning",
    "02-working",
    "03-building",
    "04-living",
    "05-keeping-up",
    "06-study-guide",
]


def md_to_html(md_text):
    """Convert markdown to HTML using marked CLI."""
    result = subprocess.run(
        ["marked"], input=md_text, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  marked error: {result.stderr}", file=sys.stderr)
        return f"<pre>{md_text}</pre>"
    return result.stdout


def get_title(text):
    """Extract first heading as title."""
    for pattern in [r"^#\s+(.+)$", r"^##\s+(.+)$"]:
        m = re.search(pattern, text, re.MULTILINE)
        if m:
            return m.group(1).strip()
    return None


def get_part_name(part_dir):
    """Get display name from _section.md or folder name."""
    section_file = os.path.join(part_dir, "_section.md")
    if os.path.exists(section_file):
        with open(section_file) as f:
            title = get_title(f.read())
            if title:
                return title
    return os.path.basename(part_dir).replace("-", " ").title()


def slug(filename):
    """Convert filename to URL-safe slug."""
    return os.path.splitext(filename)[0]


def short_slug(s):
    """Strip leading number prefix from a slug: '06-memory-is-files' -> 'memory-is-files'."""
    import re
    return re.sub(r'^[0-9]+[a-z]*-', '', s)


def chapter_route(ch_slug):
    """Canonical public route for a chapter."""
    return f"/book/{short_slug(ch_slug)}"


CHAPTER_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Shapes of Intelligence</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300;1,400&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #151518;
      --surface: #1c1c22;
      --text: #d0d0d8;
      --text-dim: #808098;
      --text-bright: #f0f0f5;
      --accent: #e8a840;
      --accent-dim: rgba(232,168,64,0.12);
      --link: #70aef8;
      --code-bg: #0e0e12;
      --border: #2a2a38;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Source Serif 4', Georgia, serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.8;
      max-width: 65ch;
      margin: 0 auto;
      padding: 3rem 1.5rem 4rem;
      font-size: 1.05rem;
      font-weight: 300;
    }}
    nav {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      color: var(--text-dim);
      margin-bottom: 2.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      letter-spacing: 0.03em;
    }}
    nav a {{
      color: var(--text-dim);
      text-decoration: none;
      transition: color 0.15s;
    }}
    nav a:hover {{ color: var(--accent); }}
    .nav-arrows {{ display: flex; gap: 1.5rem; }}
    .nav-arrows a {{ font-size: 0.8rem; }}
    .part-label {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-bottom: 0.5rem;
    }}
    h1, h2 {{
      color: var(--text-bright);
      font-weight: 600;
      letter-spacing: -0.01em;
    }}
    h1 {{ font-size: 1.8rem; margin-bottom: 2rem; line-height: 1.2; }}
    h2 {{ font-size: 1.8rem; margin: 0 0 2rem; line-height: 1.2; }}
    h3 {{
      font-size: 1.15rem;
      color: var(--accent);
      margin: 2rem 0 0.75rem;
      font-weight: 600;
    }}
    p {{ margin: 0.8rem 0; }}
    a {{ color: var(--link); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82em;
      background: var(--code-bg);
      padding: 0.15em 0.4em;
      border-radius: 3px;
    }}
    pre {{
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1rem 1.25rem;
      overflow-x: auto;
      margin: 1.2rem 0;
    }}
    pre code {{ background: none; padding: 0; font-size: 0.8rem; line-height: 1.6; }}
    blockquote {{
      border-left: 2px solid var(--accent);
      padding: 0.5rem 1rem;
      margin: 1rem 0;
      background: var(--accent-dim);
      border-radius: 0 4px 4px 0;
      font-style: italic;
      color: var(--text-dim);
    }}
    ul, ol {{ padding-left: 1.5rem; margin: 0.75rem 0; }}
    li {{ margin: 0.35rem 0; }}
    strong {{ color: var(--text-bright); font-weight: 600; }}
    em {{ font-style: italic; }}
    hr {{
      border: none;
      border-top: 1px solid var(--border);
      margin: 2.5rem 0;
    }}
    .chapter-nav {{
      margin-top: 3rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
    }}
    .chapter-nav a {{
      color: var(--text-dim);
      text-decoration: none;
      max-width: 45%;
    }}
    .chapter-nav a:hover {{ color: var(--accent); }}
    .chapter-nav .next {{ text-align: right; }}
    @media (max-width: 600px) {{
      body {{ padding: 1.5rem 1rem; font-size: 1rem; }}
      h2 {{ font-size: 1.4rem; }}
    }}
  </style>
</head>
<body>
  <nav>
    <a href="/book/">Shapes of Intelligence</a>
    <div class="nav-arrows">
      {prev_link}
      {next_link}
    </div>
  </nav>
  <div class="part-label">{part_name}</div>
  <article>
    {content}
  </article>
  <div class="chapter-nav">
    {prev_nav}
    {next_nav}
  </div>
</body>
</html>
"""


def build():
    os.makedirs(SITE_DIR, exist_ok=True)

    # Collect all chapters in order
    all_chapters = []  # (part_slug, part_name, filename, title, md_text, slug)
    for part in PART_ORDER:
        part_dir = os.path.join(CHAPTERS_DIR, part)
        if not os.path.isdir(part_dir):
            continue
        part_name = get_part_name(part_dir)
        files = sorted(
            f for f in os.listdir(part_dir)
            if f.endswith(".md") and f != "_section.md"
        )
        for filename in files:
            filepath = os.path.join(part_dir, filename)
            with open(filepath) as f:
                md_text = f.read()
            title = get_title(md_text) or slug(filename).replace("-", " ").title()
            ch_slug = slug(filename)
            all_chapters.append((part, part_name, filename, title, md_text, ch_slug))

    # Build individual chapter pages
    for i, (part, part_name, filename, title, md_text, ch_slug) in enumerate(all_chapters):
        part_dir = os.path.join(SITE_DIR, part)
        os.makedirs(part_dir, exist_ok=True)

        content = md_to_html(md_text)

        # Prev/next links
        prev_link = ""
        prev_nav = "<span></span>"
        next_link = ""
        next_nav = "<span></span>"

        if i > 0:
            pp, _, _, pt, _, ps = all_chapters[i - 1]
            prev_link = f'<a href="{chapter_route(ps)}">&larr; prev</a>'
            prev_nav = f'<a href="{chapter_route(ps)}">&larr; {pt}</a>'
        if i < len(all_chapters) - 1:
            np, _, _, nt, _, ns = all_chapters[i + 1]
            next_link = f'<a href="{chapter_route(ns)}">next &rarr;</a>'
            next_nav = f'<a class="next" href="{chapter_route(ns)}">{nt} &rarr;</a>'

        html = CHAPTER_TEMPLATE.format(
            title=title,
            part_name=part_name,
            content=content,
            prev_link=prev_link,
            next_link=next_link,
            prev_nav=prev_nav,
            next_nav=next_nav,
        )

        outpath = os.path.join(part_dir, f"{ch_slug}.html")
        with open(outpath, "w") as f:
            f.write(html)

    # Build table of contents
    build_toc(all_chapters)

    # Build full text
    build_full(all_chapters)

    print(f"Book built: {len(all_chapters)} chapters")
    print(f"  TOC: {SITE_DIR}/index.html")
    print(f"  Full: {SITE_DIR}/full.html")


def build_toc(all_chapters):
    """Build the table of contents page."""
    parts_html = ""
    current_part = ""
    ch_num = 0

    for part, part_name, filename, title, md_text, ch_slug in all_chapters:
        if part != current_part:
            if current_part:
                parts_html += "</ul></div>\n"
            parts_html += f'<div class="toc-part"><div class="toc-part-title">{part_name}</div><ul>\n'
            current_part = part

        ch_num += 1
        word_count = len(md_text.split())
        parts_html += f'  <li><a href="{chapter_route(ch_slug)}"><span class="toc-num">{ch_num}</span>{title}</a><span class="toc-words">{word_count}w</span></li>\n'

    parts_html += "</ul></div>\n"

    total_words = sum(len(md.split()) for _, _, _, _, md, _ in all_chapters)

    toc_html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shapes of Intelligence</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@300;400;600&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #151518;
      --surface: #1c1c22;
      --text: #d0d0d8;
      --text-dim: #808098;
      --text-bright: #f0f0f5;
      --accent: #e8a840;
      --link: #70aef8;
      --border: #2a2a38;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Source Serif 4', Georgia, serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.7;
      max-width: 65ch;
      margin: 0 auto;
      padding: 3rem 1.5rem 4rem;
    }}
    h1 {{
      font-size: 2.2rem;
      color: var(--text-bright);
      font-weight: 600;
      letter-spacing: -0.02em;
      margin-bottom: 0.3rem;
    }}
    .byline {{
      color: var(--text-dim);
      font-size: 0.95rem;
      font-style: italic;
      margin-bottom: 0.5rem;
    }}
    .meta {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      color: var(--text-dim);
      margin-bottom: 2.5rem;
      letter-spacing: 0.03em;
    }}
    .meta a {{ color: var(--text-dim); text-decoration: none; }}
    .meta a:hover {{ color: var(--accent); }}
    .toc-part {{
      margin-bottom: 2rem;
    }}
    .toc-part-title {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid var(--border);
      margin-bottom: 0.5rem;
    }}
    ul {{ list-style: none; padding: 0; }}
    li {{
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }}
    li a {{
      color: var(--text);
      text-decoration: none;
      padding: 0.5rem 0;
      flex: 1;
      display: flex;
      gap: 0.8rem;
      align-items: baseline;
      transition: color 0.12s;
    }}
    li a:hover {{ color: var(--accent); }}
    .toc-num {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      color: var(--text-dim);
      min-width: 2rem;
    }}
    .toc-words {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      color: var(--text-dim);
      white-space: nowrap;
      padding: 0.5rem 0;
    }}
    .links {{
      margin-top: 2rem;
      padding-top: 1rem;
      border-top: 1px solid var(--border);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      color: var(--text-dim);
      display: flex;
      gap: 2rem;
    }}
    .links a {{ color: var(--text-dim); text-decoration: none; }}
    .links a:hover {{ color: var(--accent); }}
  </style>
</head>
<body>
  <h1>Shapes of Intelligence</h1>
  <p class="byline">The patterns nobody teaches you about working with AI</p>
  <div class="meta">
    James Wilson &middot; {len(all_chapters)} chapters &middot; {total_words:,} words &middot;
    <a href="/book/full">read full text</a>
  </div>
  {parts_html}
  <div class="links">
    <a href="/">&larr; Reference site</a>
    <a href="/chapter-dashboard">Chapter dashboard</a>
    <a href="/book/full">Full text</a>
  </div>
</body>
</html>
"""

    with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
        f.write(toc_html)


def build_full(all_chapters):
    """Build the full text page."""
    body = ""
    current_part = ""

    for part, part_name, filename, title, md_text, ch_slug in all_chapters:
        if part != current_part:
            body += f'<div class="full-part">{part_name}</div>\n'
            current_part = part
        body += f'<div id="{ch_slug}">\n'
        body += md_to_html(md_text)
        body += '</div>\n<hr>\n'

    full_html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shapes of Intelligence — Full Text</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300;1,400&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #151518;
      --surface: #1c1c22;
      --text: #d0d0d8;
      --text-dim: #808098;
      --text-bright: #f0f0f5;
      --accent: #e8a840;
      --accent-dim: rgba(232,168,64,0.12);
      --link: #70aef8;
      --code-bg: #0e0e12;
      --border: #2a2a38;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Source Serif 4', Georgia, serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.8;
      max-width: 65ch;
      margin: 0 auto;
      padding: 3rem 1.5rem 4rem;
      font-size: 1.05rem;
      font-weight: 300;
    }}
    nav {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      color: var(--text-dim);
      margin-bottom: 3rem;
      position: sticky;
      top: 0;
      background: var(--bg);
      padding: 0.8rem 0;
      border-bottom: 1px solid var(--border);
      z-index: 10;
    }}
    nav a {{ color: var(--text-dim); text-decoration: none; }}
    nav a:hover {{ color: var(--accent); }}
    h1, h2 {{ color: var(--text-bright); font-weight: 600; }}
    h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
    h2 {{ font-size: 1.6rem; margin: 3rem 0 1rem; }}
    h3 {{ font-size: 1.15rem; color: var(--accent); margin: 2rem 0 0.75rem; font-weight: 600; }}
    p {{ margin: 0.8rem 0; }}
    a {{ color: var(--link); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code {{ font-family: 'JetBrains Mono', monospace; font-size: 0.82em; background: var(--code-bg); padding: 0.15em 0.4em; border-radius: 3px; }}
    pre {{ background: var(--code-bg); border: 1px solid var(--border); border-radius: 6px; padding: 1rem 1.25rem; overflow-x: auto; margin: 1.2rem 0; }}
    pre code {{ background: none; padding: 0; font-size: 0.8rem; line-height: 1.6; }}
    blockquote {{ border-left: 2px solid var(--accent); padding: 0.5rem 1rem; margin: 1rem 0; background: var(--accent-dim); border-radius: 0 4px 4px 0; font-style: italic; color: var(--text-dim); }}
    ul, ol {{ padding-left: 1.5rem; margin: 0.75rem 0; }}
    li {{ margin: 0.35rem 0; }}
    strong {{ color: var(--text-bright); font-weight: 600; }}
    hr {{ border: none; border-top: 1px solid var(--border); margin: 3rem 0; }}
    .full-part {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin: 4rem 0 1rem;
      padding-top: 2rem;
      border-top: 2px solid var(--accent);
    }}
    .full-part:first-child {{ margin-top: 0; border-top: none; padding-top: 0; }}
    @media (max-width: 600px) {{
      body {{ padding: 1.5rem 1rem; font-size: 1rem; }}
    }}
  </style>
</head>
<body>
  <nav>
    <a href="/book/">&larr; Table of Contents</a> &middot;
    <a href="/">Reference</a> &middot;
    <a href="/chapter-dashboard">Dashboard</a>
  </nav>
  {body}
</body>
</html>
"""

    with open(os.path.join(SITE_DIR, "full.html"), "w") as f:
        f.write(full_html)


if __name__ == "__main__":
    build()
