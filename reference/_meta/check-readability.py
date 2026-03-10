#!/usr/bin/env python3
"""
Check reading level, vocabulary, and pacing of reference pages.
Usage: python3 reference/_meta/check-readability.py

Flags pages that use jargon, long words, complex sentences, or uneven pacing.
Target: 8th grade reading level. Varied rhythm. Breathing room.
"""

import math
import os
import re
import sys
import textstat

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REF_DIR = os.path.dirname(SCRIPT_DIR)

# ANSI colors
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
GREEN = "\033[0;32m"
DIM = "\033[2m"
BOLD = "\033[1m"
CYAN = "\033[0;36m"
RESET = "\033[0m"

# Jargon that should always be simplified
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

# Technical terms that are fine — the reader is learning these
ALLOWED_LONG = {
    "html", "css", "javascript", "typescript", "python", "websocket",
    "json", "api", "cli", "github", "ssh", "npm", "vps", "cors",
    "ui", "ux", "rng", "ascii", "dom", "jsonl", "http", "https",
    "localhost", "dataclass", "reducer", "shapegame", "integration",
    "individually", "reconnection", "reproducible", "configuration",
    "troubleshoot", "troubleshooting", "deterministic", "heuristic",
    "heuristics", "architecture", "dependencies", "intelligence",
    "repositories", "authentication", "automatically", "conversation",
    "conversations", "spreadsheets", "understanding", "installation",
    "instructions", "multiplayer", "bidirectional",
}

MAX_GRADE = 8
MAX_SENTENCE_WORDS = 30


def strip_frontmatter(text):
    """Remove YAML frontmatter between --- markers."""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].strip()
    return text


def strip_non_prose(text):
    """Remove code blocks, blockquotes, headers, tables, links, formatting."""
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


def find_long_sentences(text, max_words=MAX_SENTENCE_WORDS):
    """Find sentences over max_words."""
    sentences = re.split(r"[.!?]+", text)
    long = []
    for s in sentences:
        s = s.strip()
        words = s.split()
        if len(words) > max_words:
            preview = " ".join(words[:15]) + "..."
            long.append((len(words), preview))
    return long


def find_jargon(text, lines):
    """Find jargon words and their line numbers."""
    found = []
    for word in JARGON:
        pattern = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                match = pattern.search(line).group()
                found.append((match, i))
    return found


def find_long_words(text, lines):
    """Find words 12+ chars that aren't in the allowed list."""
    words = re.findall(r"\b[a-zA-Z]{12,}\b", text)
    unique = sorted(set(w.lower() for w in words) - ALLOWED_LONG)
    results = []
    for w in unique[:10]:
        pattern = re.compile(r"\b" + re.escape(w) + r"\b", re.IGNORECASE)
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                results.append((w, i))
                break
        else:
            results.append((w, None))
    return results


# ── Pacing ──────────────────────────────────────────────────────────


def parse_sections(text):
    """Split markdown into sections by ## headers. Returns [(title, body)]."""
    # Remove frontmatter first
    text = strip_frontmatter(text)
    parts = re.split(r"^(#{1,3}\s+.+)$", text, flags=re.MULTILINE)

    sections = []
    current_title = "(intro)"
    current_body = ""

    for part in parts:
        if re.match(r"^#{1,3}\s+", part):
            if current_body.strip():
                sections.append((current_title, current_body.strip()))
            current_title = part.strip().lstrip("#").strip()
            current_body = ""
        else:
            current_body += part

    if current_body.strip():
        sections.append((current_title, current_body.strip()))

    return sections


def count_code_blocks(text):
    """Count fenced code blocks in text."""
    return len(re.findall(r"^```", text, flags=re.MULTILINE)) // 2


def count_questions(text):
    """Count question marks in prose (not in code blocks)."""
    no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return no_code.count("?")


def count_blockquotes(text):
    """Count blockquote lines (sample prompts, callouts)."""
    return len(re.findall(r"^>", text, flags=re.MULTILINE))


def sentence_lengths(prose):
    """Return list of word counts per sentence."""
    sentences = re.split(r"[.!?]+", prose)
    lengths = []
    for s in sentences:
        s = s.strip()
        wc = len(s.split())
        if wc > 0:
            lengths.append(wc)
    return lengths


def classify_line(line):
    """Classify a line by what it does for the reader.
    Returns one of: prose, code, prompt, question, list, header, blank"""
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


def get_line_rhythm(text):
    """Walk the raw markdown and produce a rhythm string.
    Each character represents a line's role:
      P=prose  C=code  >=prompt  ?=question  L=list  H=header  .=blank
    """
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
        char = {
            "prose": "P", "code_fence": "C", "prompt": ">",
            "question": "?", "list": "L", "header": "H", "blank": ".",
        }[kind]
        rhythm.append(char)
    return rhythm


def analyze_pacing(text, prose):
    """Analyze the internal rhythm of a page."""
    sections = parse_sections(text)
    issues = []

    # ── Section-level word counts ──
    section_words = []
    for title, body in sections:
        body_prose = strip_non_prose(body)
        wc = len(body_prose.split()) if body_prose.strip() else 0
        section_words.append((title, wc))

    # ── Sentence rhythm ──
    sent_lens = sentence_lengths(prose)
    if len(sent_lens) >= 5:
        avg_sent = sum(sent_lens) / len(sent_lens)
        stdev = (sum((x - avg_sent)**2 for x in sent_lens) / len(sent_lens)) ** 0.5

        if stdev < 3 and avg_sent > 8:
            issues.append(f"Monotone — sentences all ~{avg_sent:.0f} words (stdev {stdev:.1f})")
    else:
        stdev = 0
        avg_sent = sum(sent_lens) / len(sent_lens) if sent_lens else 0

    # ── Page-level metrics ──
    code_blocks = count_code_blocks(text)
    total_words = len(prose.split()) if prose.strip() else 0
    questions = count_questions(text)
    prompts = count_blockquotes(text)

    if total_words > 500 and code_blocks == 0 and prompts == 0:
        issues.append("No code blocks or sample prompts — wall of text")

    if total_words > 300 and questions == 0:
        issues.append("No questions — reads like a lecture")

    # ── Internal rhythm: prose runs ──
    # The idea: prose is inhale, code/prompt/list is exhale.
    # Flag long stretches of unbroken prose without a break.
    rhythm = get_line_rhythm(text)

    # Find runs of consecutive prose lines (P)
    prose_run = 0
    max_run = 0
    run_starts = []  # (start_line, length) for long runs
    for i, ch in enumerate(rhythm):
        if ch == "P":
            prose_run += 1
        else:
            if prose_run > 12:
                run_starts.append((i - prose_run + 1, prose_run))
            max_run = max(max_run, prose_run)
            prose_run = 0
    if prose_run > 12:
        run_starts.append((len(rhythm) - prose_run + 1, prose_run))
        max_run = max(max_run, prose_run)

    for start, length in run_starts:
        # Find which section this falls in
        raw_lines = text.split("\n")
        context = raw_lines[min(start, len(raw_lines)-1)][:60] if start < len(raw_lines) else ""
        issues.append(f"{length} prose lines without a break near line {start}: \"{context}...\"")

    # ── Internal rhythm: code/prompt bunching ──
    # Flag long stretches of code/prompts without prose (reader loses the thread)
    non_prose_run = 0
    for i, ch in enumerate(rhythm):
        if ch in ("C", ">", "L"):
            non_prose_run += 1
        elif ch == "P":
            if non_prose_run > 20:
                issues.append(f"Long code/prompt block ({non_prose_run} lines) without prose explanation near line {i}")
            non_prose_run = 0

    # ── Rhythm visualization ──
    # Compress rhythm into a visual: show the texture of the page
    # Group into ~5-line chunks and show dominant type
    chunk_size = 5
    rhythm_viz = []
    for i in range(0, len(rhythm), chunk_size):
        chunk = rhythm[i:i+chunk_size]
        # Pick dominant character
        counts = {}
        for ch in chunk:
            if ch != ".":
                counts[ch] = counts.get(ch, 0) + 1
        if counts:
            dominant = max(counts, key=counts.get)
            rhythm_viz.append(dominant)
        else:
            rhythm_viz.append(".")

    return {
        "sections": section_words,
        "sentence_avg": avg_sent,
        "sentence_stdev": stdev,
        "code_blocks": code_blocks,
        "questions": questions,
        "prompts": prompts,
        "max_prose_run": max_run,
        "rhythm_viz": "".join(rhythm_viz),
        "issues": issues,
    }


# ── Main check ──────────────────────────────────────────────────────


def check_file(filepath):
    """Run all checks on a single markdown file."""
    filename = os.path.basename(filepath)
    with open(filepath) as f:
        raw = f.read()
        f.seek(0)
        raw_lines = f.readlines()

    text = strip_frontmatter(raw)
    prose = strip_non_prose(text)

    if not prose.strip():
        return None

    # Grade level metrics
    grade_fk = textstat.flesch_kincaid_grade(prose)
    grade_cl = textstat.coleman_liau_index(prose)
    grade_ari = textstat.automated_readability_index(prose)
    grade_consensus = textstat.text_standard(prose, float_output=True)
    reading_ease = textstat.flesch_reading_ease(prose)
    word_count = textstat.lexicon_count(prose)
    sentence_count = textstat.sentence_count(prose)
    syllable_count = textstat.syllable_count(prose)

    # Vocabulary checks
    jargon = find_jargon(prose, raw_lines)
    long_sents = find_long_sentences(prose)
    long_words = find_long_words(prose, raw_lines)

    # Pacing
    pacing = analyze_pacing(text, prose)

    # Status
    if jargon:
        status = "FAIL"
    elif grade_consensus > MAX_GRADE or long_sents or pacing["issues"]:
        status = "WARN"
    else:
        status = "PASS"

    return {
        "filename": filename,
        "status": status,
        "grade_fk": grade_fk,
        "grade_cl": grade_cl,
        "grade_ari": grade_ari,
        "grade_consensus": grade_consensus,
        "reading_ease": reading_ease,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "syllable_count": syllable_count,
        "jargon": jargon,
        "long_sentences": long_sents,
        "long_words": long_words,
        "pacing": pacing,
    }


def print_result(r):
    colors = {"PASS": GREEN, "WARN": YELLOW, "FAIL": RED}
    c = colors[r["status"]]

    pacing = r["pacing"]
    print(f"{c}{r['status']}{RESET}  {r['filename']}  "
          f"{DIM}(grade ~{r['grade_consensus']:.0f}, "
          f"FK {r['grade_fk']:.1f}, "
          f"ease {r['reading_ease']:.0f}, "
          f"{r['word_count']} words){RESET}")

    # Pacing summary
    print(f"  {DIM}rhythm: "
          f"sentences avg {pacing['sentence_avg']:.0f}w ±{pacing['sentence_stdev']:.1f}, "
          f"longest prose run {pacing['max_prose_run']} lines, "
          f"{pacing['code_blocks']} code, "
          f"{pacing['questions']}? "
          f"{pacing['prompts']}>{RESET}")

    # Rhythm visualization — the texture of the page
    # P=prose C=code >=prompt H=header L=list .=blank
    viz = pacing["rhythm_viz"]
    if viz:
        # Color each character
        viz_colored = ""
        char_colors = {"P": "", "C": GREEN, ">": CYAN, "H": BOLD, "L": DIM, ".": DIM}
        for ch in viz:
            color = char_colors.get(ch, "")
            viz_colored += f"{color}{ch}{RESET}"
        print(f"  {DIM}texture:{RESET} {viz_colored}  {DIM}(P=prose C=code >=prompt H=header L=list){RESET}")

    if r["jargon"]:
        print(f"  {RED}Jargon:{RESET}")
        for word, line in r["jargon"]:
            print(f"    \"{word}\" (line {line})")

    if r["long_sentences"]:
        print(f"  {YELLOW}Long sentences (>{MAX_SENTENCE_WORDS} words):{RESET}")
        for count, preview in r["long_sentences"]:
            print(f"    {count} words: {preview}")

    if pacing["issues"]:
        print(f"  {CYAN}Rhythm:{RESET}")
        for issue in pacing["issues"]:
            print(f"    {issue}")

    if r["long_words"]:
        print(f"  {DIM}Long words (review):{RESET}")
        for word, line in r["long_words"]:
            loc = f"line {line}" if line else "?"
            print(f"    {word} ({loc})")

    print()


def main():
    print()
    print("=== Readability & Pacing Check ===")
    print()

    total = {"PASS": 0, "WARN": 0, "FAIL": 0}

    md_files = sorted(
        f for f in os.listdir(REF_DIR)
        if f.endswith(".md") and not f.startswith("_")
    )

    for filename in md_files:
        filepath = os.path.join(REF_DIR, filename)
        result = check_file(filepath)
        if result:
            print_result(result)
            total[result["status"]] += 1

    print("---")
    if total["FAIL"]:
        print(f"{RED}{total['FAIL']} page(s) have jargon to simplify.{RESET}")
    if total["WARN"]:
        print(f"{YELLOW}{total['WARN']} page(s) have readability or pacing warnings.{RESET}")
    if not total["FAIL"] and not total["WARN"]:
        print(f"{GREEN}All pages pass readability and pacing checks.{RESET}")
    print()

    return 1 if total["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
