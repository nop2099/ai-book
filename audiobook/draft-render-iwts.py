#!/usr/bin/env python3
"""Draft render of I Want to Share using macOS say voices."""

import subprocess, hashlib, re, os, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRIPT = Path(__file__).parent / "i-want-to-share.md"
OUTDIR = Path(__file__).parent / "output" / "iwts-draft"
LINES_DIR = OUTDIR / "lines"

VOICES = {
    "JAMES":  "Daniel",
    "RICH":   "Rishi",
    "PARROT": "Karen",
    "SAM":    "Tessa",
    "SAL":    "Moira",
    "GUS":    "Aman",
    "ALEX":   "Samantha",
    "MO":     "Kathy",
}

RATES = {
    "GUS": 162,  # 10% slower
}
DEFAULT_RATE = 170  # slightly slower than before
GAP_MS = 400  # silence between lines
WORKERS = 8

def parse_lines(script_path):
    lines = []
    speaker = None
    for raw in script_path.read_text().splitlines():
        m = re.match(r'^\[([A-Z]+)\]$', raw.strip())
        if m:
            speaker = m.group(1)
            continue
        if not raw.strip() or raw.startswith('#') or raw.startswith('|') or raw.startswith('---') or raw.startswith('>') or raw.startswith('-'):
            continue
        if speaker and speaker in VOICES:
            lines.append((speaker, raw.strip()))
    return lines

def render_line(idx, speaker, text):
    h = hashlib.sha256(text.encode()).hexdigest()[:12]
    padded = f"{idx:04d}"
    outfile = LINES_DIR / f"{padded}_{speaker}_{h}.aiff"

    if text == "...":
        if not outfile.exists():
            subprocess.run(["say", "-v", VOICES["JAMES"], "-o", str(outfile), " "],
                         check=True, capture_output=True)
        return idx, outfile

    if not outfile.exists():
        voice = VOICES[speaker]
        rate = RATES.get(speaker, DEFAULT_RATE)
        subprocess.run(["say", "-v", voice, "-r", str(rate), "-o", str(outfile), text],
                     check=True, capture_output=True)
        return idx, outfile
    return idx, outfile

def assemble(files):
    # Generate a silence file for gaps
    silence_file = OUTDIR / "silence.aiff"
    if not silence_file.exists():
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            f"anullsrc=r=22050:cl=mono:d={GAP_MS/1000}",
            "-c:a", "pcm_s16be", str(silence_file)
        ], check=True, capture_output=True)

    concat_file = OUTDIR / "concat.txt"
    with open(concat_file, 'w') as f:
        for i, fp in enumerate(files):
            f.write(f"file '{fp.resolve()}'\n")
            if i < len(files) - 1:
                f.write(f"file '{silence_file.resolve()}'\n")

    out_mp3 = OUTDIR / "iwts-draft.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:a", "libmp3lame", "-q:a", "4",
        str(out_mp3)
    ], check=True, capture_output=True)
    return out_mp3

def write_player():
    html = OUTDIR / "listen.html"
    voice_tags = []
    for speaker, voice in VOICES.items():
        voice_tags.append(f'  <span class="voice">{speaker} — {voice}</span>')
    html.write_text(f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>I Want to Share — Draft Listen</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, system-ui, sans-serif; background: #0a0a10; color: #d0d0e2; padding: 2rem; max-width: 700px; margin: 0 auto; }}
  h1 {{ font-size: 1.4rem; margin-bottom: 0.5rem; color: #e8a83e; }}
  p.sub {{ color: #8888aa; margin-bottom: 1.5rem; font-size: 0.9rem; }}
  audio {{ width: 100%; margin-bottom: 1rem; }}
  .voices {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem; }}
  .voice {{ padding: 0.3rem 0.7rem; border-radius: 4px; font-size: 0.8rem; background: #1e1e32; color: #d0d0e2; }}
</style>
</head>
<body>
<h1>I Want to Share — Draft Render</h1>
<p class="sub">macOS say voices. Eight characters. {WORKERS}x parallel render.</p>
<div class="voices">
{chr(10).join(voice_tags)}
</div>
<audio controls src="iwts-draft.mp3"></audio>
</body>
</html>''')
    return html

if __name__ == "__main__":
    if LINES_DIR.exists():
        print("Clearing old cache...")
        shutil.rmtree(LINES_DIR)
    LINES_DIR.mkdir(parents=True, exist_ok=True)

    print("Parsing script...")
    lines = parse_lines(SCRIPT)
    print(f"Found {len(lines)} voice lines")

    print(f"Rendering with {WORKERS} workers...")
    results = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(render_line, i, s, t): i for i, (s, t) in enumerate(lines, 1)}
        done = 0
        for future in as_completed(futures):
            idx, outfile = future.result()
            results[idx] = outfile
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{len(lines)} rendered")

    # Reassemble in order
    ordered = [results[i] for i in range(1, len(lines) + 1)]
    print(f"\nRendered {len(ordered)} lines. Assembling...")
    mp3 = assemble(ordered)
    print(f"MP3: {mp3} ({mp3.stat().st_size // 1024}KB)")

    player = write_player()
    print(f"Player: {player}")
