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

# ── 2. Copy static pages (hand-crafted HTML) ──
if [ -d "$STATIC_DIR" ]; then
  echo "Copying static pages..."
  for html_file in "$STATIC_DIR"/*.html; do
    [ -f "$html_file" ] || continue
    cp "$html_file" "$SITE_DIR/"
    echo "  $(basename "$html_file") (static)"
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

echo ""
echo "Site built at: $SITE_DIR/"
echo "Pages: $(find "$SITE_DIR" -name '*.html' | wc -l | tr -d ' ')"
echo ""
echo "To preview: cd $SITE_DIR && python3 -m http.server 8000"
echo "To deploy:  rsync -avz --delete $SITE_DIR/ shapes.exe.xyz:/var/www/html/"
