#!/bin/bash
# Build reference site from markdown + static pages + book chapters
# Usage: bash reference/_meta/build.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REF_DIR="$(dirname "$SCRIPT_DIR")"
SITE_DIR="$REF_DIR/site"
TEMPLATE="$SCRIPT_DIR/template.html"
STATIC_DIR="$SCRIPT_DIR/static"
BOOK_DIR="$(dirname "$REF_DIR")/chapters"

# Check for marked CLI
if ! command -v marked &> /dev/null; then
  echo "Installing marked..."
  npm install -g marked
fi

# Clean and create site directory
rm -rf "$SITE_DIR"
mkdir -p "$SITE_DIR"

# ── 1. Build markdown reference pages ──
echo "Building reference pages..."
for md_file in "$REF_DIR"/*.md; do
  [ -f "$md_file" ] || continue

  filename=$(basename "$md_file" .md)

  # Extract frontmatter
  title=$(grep '^title:' "$md_file" | head -1 | sed 's/^title: *//')
  summary=$(grep '^summary:' "$md_file" | head -1 | sed 's/^summary: *//')
  platforms_raw=$(grep '^platforms:' "$md_file" | head -1 | sed 's/^platforms: *//')

  # Build platform tags HTML
  platform_html=""
  if [ -n "$platforms_raw" ]; then
    for p in $(echo "$platforms_raw" | tr -d '[]' | tr ',' ' '); do
      platform_html="$platform_html<span class=\"platform-tag\">$p</span>"
    done
  fi

  # Strip frontmatter and convert to HTML
  body=$(sed '1{/^---$/!q;};1,/^---$/d' "$md_file" | marked)

  # Use python for template replacement (handles multiline content)
  python3 -c "
import sys
with open('$TEMPLATE') as f:
    template = f.read()
template = template.replace('{{title}}', '''$title''')
template = template.replace('{{summary}}', '''$summary''')
template = template.replace('{{platforms}}', '''$platform_html''')
with open('$md_file') as f:
    lines = f.readlines()
    in_front = False
    content_lines = []
    front_done = False
    for line in lines:
        if line.strip() == '---' and not front_done:
            if in_front:
                front_done = True
            else:
                in_front = True
            continue
        if in_front and not front_done:
            continue
        content_lines.append(line)
import subprocess
md_content = ''.join(content_lines)
result = subprocess.run(['marked'], input=md_content, capture_output=True, text=True)
template = template.replace('{{content}}', result.stdout)
print(template)
" > "$SITE_DIR/${filename}.html"

  echo "  ${filename}.html"
done

# ── 2. Copy static pages and assets ──
if [ -d "$STATIC_DIR" ]; then
  echo "Copying static pages and assets..."
  for static_file in "$STATIC_DIR"/*; do
    [ -f "$static_file" ] || continue
    cp "$static_file" "$SITE_DIR/"
    echo "  $(basename "$static_file") (static)"
  done
fi

# ── 3. Build book pages ──
if [ -f "$SCRIPT_DIR/build-book.py" ] && [ -d "$BOOK_DIR" ]; then
  echo "Building book..."
  cd "$SCRIPT_DIR"
  python3 build-book.py
fi

# ── 4. Generate chapter metrics ──
if [ -f "$SCRIPT_DIR/analyze-chapters.py" ] && [ -d "$BOOK_DIR" ]; then
  echo "Generating chapter metrics..."
  cd "$SCRIPT_DIR"
  # Use venv if available (textstat dependency)
  if [ -f "$SCRIPT_DIR/.venv/bin/python3" ]; then
    PYBIN="$SCRIPT_DIR/.venv/bin/python3"
  else
    PYBIN=python3
  fi
  $PYBIN analyze-chapters.py > "$SITE_DIR/chapter-metrics.json"

  # Inline metrics into dashboard if it exists
  if [ -f "$SITE_DIR/chapter-dashboard.html" ]; then
    python3 -c "
import json
with open('$SITE_DIR/chapter-metrics.json') as f:
    data = json.load(f)
with open('$SITE_DIR/chapter-dashboard.html') as f:
    html = f.read()
if 'CHAPTER_DATA_PLACEHOLDER' in html:
    html = html.replace('CHAPTER_DATA_PLACEHOLDER', json.dumps(data))
    with open('$SITE_DIR/chapter-dashboard.html', 'w') as f:
        f.write(html)
    print('  Inlined metrics into chapter-dashboard.html')
else:
    print('  Dashboard already has data inlined, skipping')
"
  fi
fi

# ── 5. Generate nginx slug map for book chapters ──
# Agents guess "book/memory-is-files.html" not "book/02-working/06-memory-is-files.html"
# This generates a map file that nginx includes to rewrite slug URLs internally.
echo "Generating nginx slug map..."
BOOK_SITE_DIR="$SITE_DIR/book"
SLUG_MAP="$SITE_DIR/slug-map.conf"
if [ -d "$BOOK_SITE_DIR" ]; then
  SITE_DIR_ENV="$SITE_DIR" python3 - <<'PY'
from pathlib import Path
import os
import re

site_dir = Path(os.environ["SITE_DIR_ENV"])
book_dir = site_dir / "book"
slug_map = site_dir / "slug-map.conf"

def short_slug(name: str) -> str:
    return re.sub(r"^[0-9]+[a-z]*-", "", name)

def part_short(part: str) -> str:
    return re.sub(r"^[0-9]+-", "", part)

root_reserved = set()
for path in site_dir.iterdir():
    if path.name in {"book", "slug-map.conf"} or path.is_dir():
        continue
    route = f"/{path.name}"
    root_reserved.add(route)
    if path.suffix == ".html":
        root_reserved.add(f"/{path.stem}")
        if path.name == "index.html":
            root_reserved.update({"/", "/index"})

mappings = {}
root_aliases = 0
skipped_root_aliases = []

def add_mapping(src: str, target: str) -> None:
    existing = mappings.get(src)
    if existing and existing != target:
        raise SystemExit(f"Conflicting slug mapping: {src} -> {existing} and {target}")
    mappings[src] = target

for chapter_file in sorted(book_dir.glob("*/*.html")):
    part = chapter_file.parent.name
    file_stem = chapter_file.stem
    file_short = short_slug(file_stem)
    target = f"/book/{part}/{chapter_file.name}"
    short_part = part_short(part)

    add_mapping(f"/book/{file_short}", target)
    add_mapping(f"/book/{file_short}.html", target)
    add_mapping(f"/book/{short_part}/{file_short}", target)
    add_mapping(f"/book/{short_part}/{file_short}.html", target)
    add_mapping(f"/book/{part}/{file_short}", target)
    add_mapping(f"/book/{part}/{file_short}.html", target)

    for root_route in (f"/{file_short}", f"/{file_short}.html"):
        if root_route in root_reserved:
            skipped_root_aliases.append(root_route)
            continue
        add_mapping(root_route, target)
        root_aliases += 1

with slug_map.open("w") as fh:
    fh.write("# Auto-generated by build.sh — public aliases for book chapters\n")
    fh.write("# Include this in nginx: include /var/www/html/slug-map.conf;\n")
    fh.write("map $uri $slug_rewrite {\n")
    fh.write('  default "";\n')
    for src in sorted(mappings):
        fh.write(f"  {src} {mappings[src]};\n")
    fh.write("}\n")

print(f"  {len(mappings)} slug mappings in slug-map.conf")
if skipped_root_aliases:
    print(f"  skipped {len(skipped_root_aliases)} root aliases due to top-level route conflicts")
if root_aliases:
    print(f"  added {root_aliases} root-level chapter aliases")
PY
fi

# ── 6. Generate sitemap, pages.json, and hashes ──
echo "Generating sitemap, pages.json, and hashes..."
python3 -c "
import os, re, json, hashlib

site_dir = '$SITE_DIR'
urls, pages, hashes = [], [], {}

def include_in_sitemap(rel_path: str) -> bool:
    if rel_path in {
        'index.html',
        'sitemap.xml',
        'slush-archive.html',
        'slush-pile.html',
    }:
        return True
    if rel_path.endswith('/header.html') or rel_path.endswith('/footer.html'):
        return False
    if rel_path.startswith('book/00-front-matter/') and rel_path.endswith(('/header.html', '/footer.html')):
        return False
    return True

for root, dirs, files in os.walk(site_dir):
    for f in files:
        if not f.endswith('.html'): continue
        fpath = os.path.join(root, f)
        rel = os.path.relpath(fpath, site_dir)
        with open(fpath, 'rb') as fh:
            content = fh.read()
        sha = hashlib.sha256(content).hexdigest()
        hashes[rel] = sha
        with open(fpath) as fh:
            text = fh.read()
        tm = re.search(r'<title>([^<]+)</title>', text)
        title = tm.group(1).strip() if tm else f
        title = re.sub(r'\s*[—–-]\s*Shapes of Intelligence$', '', title)
        pages.append({'path': rel, 'title': title, 'url': 'https://shapes.exe.xyz/' + rel})
        if include_in_sitemap(rel):
            urls.append('https://shapes.exe.xyz/' + rel)

urls.sort(); pages.sort(key=lambda p: p['path'])

# sitemap.xml
lines = ['<?xml version=\"1.0\" encoding=\"UTF-8\"?>','<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">']
for u in urls: lines.append(f'  <url><loc>{u}</loc></url>')
lines.append('</urlset>')
with open(os.path.join(site_dir, 'sitemap.xml'), 'w') as f: f.write('\n'.join(lines) + '\n')

# pages.json
with open(os.path.join(site_dir, 'pages.json'), 'w') as f: json.dump(pages, f, indent=2)

# hashes.json
with open(os.path.join(site_dir, 'hashes.json'), 'w') as f: json.dump(hashes, f, indent=2, sort_keys=True)

print(f'  sitemap.xml: {len(urls)} URLs')
print(f'  pages.json: {len(pages)} pages')
print(f'  hashes.json: {len(hashes)} hashes')
"

# ── 7. Validate internal links and route aliases ──
echo "Validating internal links..."
python3 "$SCRIPT_DIR/check-site-links.py" "$SITE_DIR"

echo "Validating prod-twin HTTP routes..."
python3 "$SCRIPT_DIR/check-prod-twin.py" "$SITE_DIR"

echo ""
echo "Site built at: $SITE_DIR/"
echo "Pages: $(find "$SITE_DIR" -name '*.html' | wc -l | tr -d ' ')"
echo ""
echo "To preview (prod twin): python3 reference/_meta/serve-prod-twin.py $SITE_DIR --port 8000"
echo "To deploy:  rsync -avz --delete $SITE_DIR/ shapes.exe.xyz:/var/www/html/"
