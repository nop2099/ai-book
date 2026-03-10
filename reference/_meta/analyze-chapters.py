#!/usr/bin/env python3
"""
Analyze all book chapters and output JSON metrics for visualization.
Usage: python3 analyze-chapters.py > chapter-metrics.json
"""

import json
import os
import re
import sys
import textstat

BOOK_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "chapters")

JARGON = [
    "metamer", "metamers", "idempotent", "orthogonal", "polymorphism",
    "paradigm", "methodology", "utilize", "utilized", "utilizing",
    "leverage", "leveraging", "leveraged",
    "facilitate", "facilitating", "facilitated",
    "encapsulate", "encapsulating", "encapsulated",
    "instantiate", "instantiating", "instantiated",
    "aforementioned", "heretofore", "therein", "wherein",
    "synergy", "scalable", "performant", "opinionated",
]


def strip_frontmatter(text):
    stripped = text.lstrip()
    if stripped.startswith("---"):
        end = stripped.find("---", 3)
        if end != -1:
            return stripped[end + 3:].strip()
    return text


def strip_non_prose(text):
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"^>.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^#+\s.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\|.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", text)
    text = re.sub(r"^[\s]*[-*]\s(.+)$", r"\1.", text, flags=re.MULTILINE)
    text = re.sub(r"^[\s]*\d+\.\s(.+)$", r"\1.", text, flags=re.MULTILINE)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def get_title(text):
    # Try h1 first, then h2, then frontmatter
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    match = re.search(r"^##\s+(.+)$", text, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    match = re.search(r"^title:\s*(.+)$", text, flags=re.MULTILINE)
    if match:
        return match.group(1).strip().strip('"')
    return None


def classify_line(line):
    stripped = line.strip()
    if not stripped:
        return "blank"
    if stripped.startswith("```"):
        return "code_fence"
    if stripped.startswith("#"):
        return "header"
    if stripped.startswith(">"):
        return "prompt"
    if "?" in stripped and not stripped.startswith("-"):
        return "question"
    if re.match(r"^[-*]\s", stripped) or re.match(r"^\d+\.\s", stripped):
        return "list"
    return "prose"


def get_rhythm(text):
    lines = text.split("\n")
    rhythm = []
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            rhythm.append("C")
            continue
        if in_code:
            rhythm.append("C")
            continue
        kind = classify_line(line)
        char = {"prose": "P", "code_fence": "C", "prompt": ">",
                "question": "?", "list": "L", "header": "H", "blank": "."}[kind]
        rhythm.append(char)
    return rhythm


def sentence_lengths(prose):
    sentences = re.split(r"[.!?]+", prose)
    return [len(s.split()) for s in sentences if s.strip()]


def count_jargon(text):
    count = 0
    for word in JARGON:
        count += len(re.findall(r"\b" + re.escape(word) + r"\b", text, re.IGNORECASE))
    return count


def analyze_file(filepath):
    with open(filepath) as f:
        raw = f.read()

    title = get_title(raw)
    if not title:
        return None

    text = strip_frontmatter(raw)
    prose = strip_non_prose(text)

    if not prose.strip() or len(prose.split()) < 20:
        return None

    word_count = textstat.lexicon_count(prose)
    sentence_count = textstat.sentence_count(prose)

    # Grade and ease
    grade_fk = textstat.flesch_kincaid_grade(prose)
    grade_consensus = textstat.text_standard(prose, float_output=True)
    reading_ease = textstat.flesch_reading_ease(prose)

    # Sentence rhythm
    sent_lens = sentence_lengths(prose)
    avg_sent = sum(sent_lens) / len(sent_lens) if sent_lens else 0
    stdev = (sum((x - avg_sent)**2 for x in sent_lens) / len(sent_lens)) ** 0.5 if len(sent_lens) >= 2 else 0

    # Content mix
    rhythm = get_rhythm(text)
    code_lines = rhythm.count("C")
    prompt_lines = rhythm.count(">")
    list_lines = rhythm.count("L")
    prose_lines = rhythm.count("P")
    question_lines = rhythm.count("?")
    total_lines = len([r for r in rhythm if r != "."])

    # Prose runs (longest stretch without a break)
    max_prose_run = 0
    run = 0
    for ch in rhythm:
        if ch == "P":
            run += 1
            max_prose_run = max(max_prose_run, run)
        else:
            run = 0

    # Questions
    no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    questions = no_code.count("?")

    # Jargon
    jargon_count = count_jargon(prose)

    # Texture (compressed rhythm)
    chunk_size = 5
    texture = []
    for i in range(0, len(rhythm), chunk_size):
        chunk = rhythm[i:i+chunk_size]
        counts = {}
        for ch in chunk:
            if ch != ".":
                counts[ch] = counts.get(ch, 0) + 1
        if counts:
            texture.append(max(counts, key=counts.get))
        else:
            texture.append(".")

    return {
        "title": title,
        "file": os.path.basename(filepath),
        "words": word_count,
        "sentences": sentence_count,
        "grade_fk": round(grade_fk, 1),
        "grade_consensus": round(grade_consensus, 1),
        "reading_ease": round(reading_ease, 1),
        "sentence_avg": round(avg_sent, 1),
        "sentence_stdev": round(stdev, 1),
        "questions": questions,
        "jargon": jargon_count,
        "max_prose_run": max_prose_run,
        "code_pct": round(100 * code_lines / total_lines, 1) if total_lines else 0,
        "prompt_pct": round(100 * prompt_lines / total_lines, 1) if total_lines else 0,
        "list_pct": round(100 * list_lines / total_lines, 1) if total_lines else 0,
        "prose_pct": round(100 * prose_lines / total_lines, 1) if total_lines else 0,
        "texture": "".join(texture),
    }


def analyze_text(raw, title):
    """Analyze a chunk of text with a given title (for subsections)."""
    text = strip_frontmatter(raw)
    prose = strip_non_prose(text)

    if not prose.strip() or len(prose.split()) < 20:
        return None

    word_count = textstat.lexicon_count(prose)
    sentence_count = textstat.sentence_count(prose)
    grade_fk = textstat.flesch_kincaid_grade(prose)
    grade_consensus = textstat.text_standard(prose, float_output=True)
    reading_ease = textstat.flesch_reading_ease(prose)

    sent_lens = sentence_lengths(prose)
    avg_sent = sum(sent_lens) / len(sent_lens) if sent_lens else 0
    stdev = (sum((x - avg_sent)**2 for x in sent_lens) / len(sent_lens)) ** 0.5 if len(sent_lens) >= 2 else 0

    rhythm = get_rhythm(text)
    code_lines = rhythm.count("C")
    prompt_lines = rhythm.count(">")
    list_lines = rhythm.count("L")
    prose_lines = rhythm.count("P")
    total_lines = len([r for r in rhythm if r != "."])

    max_prose_run = 0
    run = 0
    for ch in rhythm:
        if ch == "P":
            run += 1
            max_prose_run = max(max_prose_run, run)
        else:
            run = 0

    no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    questions = no_code.count("?")
    jargon_count = count_jargon(prose)

    chunk_size = 5
    texture = []
    for i in range(0, len(rhythm), chunk_size):
        chunk = rhythm[i:i+chunk_size]
        counts = {}
        for ch in chunk:
            if ch != ".":
                counts[ch] = counts.get(ch, 0) + 1
        texture.append(max(counts, key=counts.get) if counts else ".")

    return {
        "title": title,
        "file": "(subsection)",
        "words": word_count,
        "sentences": sentence_count,
        "grade_fk": round(grade_fk, 1),
        "grade_consensus": round(grade_consensus, 1),
        "reading_ease": round(reading_ease, 1),
        "sentence_avg": round(avg_sent, 1),
        "sentence_stdev": round(stdev, 1),
        "questions": questions,
        "jargon": jargon_count,
        "max_prose_run": max_prose_run,
        "code_pct": round(100 * code_lines / total_lines, 1) if total_lines else 0,
        "prompt_pct": round(100 * prompt_lines / total_lines, 1) if total_lines else 0,
        "list_pct": round(100 * list_lines / total_lines, 1) if total_lines else 0,
        "prose_pct": round(100 * prose_lines / total_lines, 1) if total_lines else 0,
        "texture": "".join(texture),
    }


def main():
    parts = sorted(d for d in os.listdir(BOOK_DIR)
                   if os.path.isdir(os.path.join(BOOK_DIR, d)) and not d.startswith("."))

    all_chapters = []
    for part in parts:
        part_dir = os.path.join(BOOK_DIR, part)
        # Get part name from _section.md
        section_file = os.path.join(part_dir, "_section.md")
        part_name = part
        if os.path.exists(section_file):
            with open(section_file) as f:
                t = get_title(f.read())
                if t:
                    part_name = t

        files = sorted(f for f in os.listdir(part_dir)
                       if f.endswith(".md") and f != "_section.md")

        for filename in files:
            filepath = os.path.join(part_dir, filename)

            # Break large files into subsections (### headers)
            with open(filepath) as f:
                raw = f.read()

            subsections = re.split(r"^(###\s+.+)$", raw, flags=re.MULTILINE)

            # If the file has subsections and is large, analyze each
            if len(subsections) > 3 and len(raw.split()) > 1000:
                file_title = get_title(raw) or filename
                # Group pairs: (header, body)
                # First element is pre-header content
                if subsections[0].strip():
                    result = analyze_text(subsections[0], f"{file_title} (intro)")
                    if result:
                        result["part"] = part
                        result["part_name"] = part_name
                        all_chapters.append(result)

                for i in range(1, len(subsections), 2):
                    header = subsections[i].lstrip("#").strip()
                    body = subsections[i+1] if i+1 < len(subsections) else ""
                    section_text = subsections[i] + body
                    result = analyze_text(section_text, f"{file_title}: {header}")
                    if result:
                        result["part"] = part
                        result["part_name"] = part_name
                        all_chapters.append(result)
            else:
                result = analyze_file(filepath)
                if result:
                    result["part"] = part
                    result["part_name"] = part_name
                    all_chapters.append(result)

    json.dump(all_chapters, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
