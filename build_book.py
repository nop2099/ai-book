#!/usr/bin/env python3
"""Assemble book.md from chapter files."""

from pathlib import Path

sections = [
    "00-front-matter",
    "01-learning",
    "02-working",
    "03-building",
    "04-living",
    "05-keeping-up",
    "06-study-guide",
]

output = []

for section in sections:
    section_dir = Path(f"chapters/{section}")
    if not section_dir.exists():
        continue

    if section == "00-front-matter":
        # Header first
        header = section_dir / "header.md"
        if header.exists():
            output.append(header.read_text().strip())
            output.append("")

        # Introduction
        intro = section_dir / "introduction.md"
        if intro.exists():
            output.append(intro.read_text().strip())
            output.append("")
        continue

    # Section header
    section_file = section_dir / "_section.md"
    if section_file.exists():
        output.append(section_file.read_text().strip())
        output.append("")
        output.append("---")
        output.append("")

    # Articles in order
    articles = sorted(section_dir.glob("[0-9]*.md"))
    for article in articles:
        content = article.read_text().strip()
        # Ensure article ends with separator
        if not content.endswith("---"):
            content += "\n\n---"
        output.append(content)
        output.append("")

# Footer
footer = Path("chapters/00-front-matter/footer.md")
if footer.exists():
    output.append(footer.read_text().strip())
    output.append("")

# Clean up any double separators
book_text = "\n".join(output)
import re
book_text = re.sub(r'(---\n+){2,}', '---\n\n', book_text)
Path("book.md").write_text(book_text)
print(f"Built book.md ({len(book_text)} chars, {book_text.count(chr(10))} lines)")
