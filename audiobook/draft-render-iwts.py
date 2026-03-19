#!/usr/bin/env python3
"""Draft render of I Want to Share using macOS say voices.

Produces 4 MP3s, each with cold open prepended:
  - iwts-full.mp3 (complete episode)
  - iwts-act1.mp3 (Act 1: The Room)
  - iwts-act2.mp3 (Act 2: The Arguments)
  - iwts-act3.mp3 (Act 3: The People)
"""

import subprocess, hashlib, re, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRIPT = Path("/Users/jameswilson/work/aibook/audiobook/i-want-to-share.md")
COLD_OPEN = Path("/Users/jameswilson/work/aibook/audiobook/assets/cold-open/cold-open-short.wav")
OUTDIR = Path(__file__).parent / "output" / "iwts-draft"
LINES_DIR = OUTDIR / "lines"
PROD_DIR = Path("/Users/jameswilson/work/aibook/reference/_meta/static")

VOICES = {
    "JAMES":  "Daniel",
    "RICH":   "Rishi",
    "PARROT": "Karen",
    "SAM":    "Tessa",
    "SAL":    "Moira",
    "GUS":    "Aman",
    "ALEX":   "Samantha",
    "MO":     "Rocko (English (US))",
    # Act 4 fake masters — reuse main cast voices
    # Fake masters — spread across all 8 voices, never same as James (Daniel)
    # since James introduces each one. No two consecutive fakes share a voice.
    # Order in script: IRA, JAD, KRULWICH, SARAH, GUY, FEYNMAN, 3B1B, MCPHEE, DOUG
    "FAKE-IRA":      "Tessa",                # Sam's voice
    "FAKE-JAD":      "Moira",                # Sal's voice
    "FAKE-KRULWICH": "Rocko (English (US))", # Mo's voice
    "FAKE-SARAH":    "Samantha",             # Alex's voice
    "FAKE-GUY":      "Rishi",                # Rich's voice
    "FAKE-FEYNMAN":  "Eddy (English (UK))",  # Gus's voice
    "FAKE-3B1B":     "Samantha",             # Alex's voice
    "FAKE-MCPHEE":   "Tessa",                # Sam's voice
    "FAKE-DOUG":     "Moira",                # Sal's voice
    # Idol section — character picks, then idol speaks in different voice
    "FAKE-HEMINGWAY": "Rishi",               # Rich's voice (Sal picks him)
    "FAKE-CARLIN":    "Samantha",            # Alex's voice (Gus picks him)
    "FAKE-JOBS":      "Eddy (English (UK))", # Gus's voice (Alex picks him)
    "FAKE-GROVE":     "Karen",               # Parrot's voice (Sam picks him)
    "FAKE-ADA":       "Tessa",               # Sam's voice (Parrot picks her)
    "FAKE-MOM":       "Moira",               # Sal's voice (Mo picks her)
    "FAKE-MIKE":      "Rocko (English (US))",# Mo's voice (Rich picks him)
}

RATES = {
    "GUS": 162,
}
DEFAULT_RATE = 170
GAP_MS = 400
WORKERS = 8

# Act boundaries (1-indexed line numbers in .md where each act ENDS)
# Acts are marked in the script with === ACT N === lines
ACT_MARKER_RE = re.compile(r'^=== ACT \d+ ===$')

def parse_lines(script_path):
    """Parse script into voice lines with act assignments."""
    lines_raw = script_path.read_text().splitlines()
    # Find ## Script
    script_start = 0
    for i, line in enumerate(lines_raw):
        if line.strip() == '## Script':
            script_start = i + 1
            break

    # Find act markers
    break_indices = []
    for i, raw in enumerate(lines_raw[script_start:], start=script_start + 1):
        if ACT_MARKER_RE.match(raw.strip()):
            break_indices.append(i)

    lines = []
    speaker = None
    current_act = 0
    for i, raw in enumerate(lines_raw[script_start:], start=script_start + 1):
        s = raw.strip()
        while current_act < len(break_indices) and i >= break_indices[current_act]:
            current_act += 1
        m = re.match(r'^\[([A-Z][\w-]*)\]$', s)
        if m:
            speaker = m.group(1)
            continue
        if not s or s.startswith('#') or s.startswith('|') or s.startswith('---') or s.startswith('>') or s.startswith('-') or ACT_MARKER_RE.match(s):
            continue
        if speaker and speaker in VOICES:
            lines.append((speaker, s, current_act))
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

def make_silence():
    silence_file = OUTDIR / "silence.aiff"
    if not silence_file.exists():
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            f"anullsrc=r=22050:cl=mono:d={GAP_MS/1000}",
            "-c:a", "pcm_s16be", str(silence_file)
        ], check=True, capture_output=True)
    return silence_file

def assemble_mp3(files, silence_file, name):
    """Concatenate AIFF files with gaps into an MP3."""
    concat_file = OUTDIR / f"concat-{name}.txt"
    with open(concat_file, 'w') as f:
        for i, fp in enumerate(files):
            f.write(f"file '{fp.resolve()}'\n")
            if i < len(files) - 1:
                f.write(f"file '{silence_file.resolve()}'\n")

    raw_mp3 = OUTDIR / f"{name}-raw.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-af", "loudnorm=I=-18:TP=-1.5:LRA=11",
        "-c:a", "libmp3lame", "-q:a", "4",
        str(raw_mp3)
    ], check=True, capture_output=True)
    return raw_mp3

def prepend_cold_open(raw_mp3, output_mp3):
    """Prepend cold open WAV to an MP3."""
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(COLD_OPEN),
        "-i", str(raw_mp3),
        "-filter_complex",
        "[0:a]aformat=sample_rates=44100:channel_layouts=mono[cold];"
        "[1:a]aformat=sample_rates=44100:channel_layouts=mono[ep];"
        "[cold][ep]concat=n=2:v=0:a=1[out]",
        "-map", "[out]", "-c:a", "libmp3lame", "-q:a", "4",
        str(output_mp3)
    ], check=True, capture_output=True)
    return output_mp3

if __name__ == "__main__":
    if LINES_DIR.exists():
        print("Clearing old cache...")
        shutil.rmtree(LINES_DIR)
    LINES_DIR.mkdir(parents=True, exist_ok=True)

    print("Parsing script...")
    lines = parse_lines(SCRIPT)
    print(f"Found {len(lines)} voice lines")

    # Count per act
    num_acts = max(act for _, _, act in lines) + 1 if lines else 1
    act_counts = [0] * num_acts
    for _, _, act in lines:
        act_counts[act] += 1
    for i, c in enumerate(act_counts):
        print(f"  Act {i+1}: {c} lines")

    print(f"Rendering with {WORKERS} workers...")
    results = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(render_line, i, s, t): i for i, (s, t, _) in enumerate(lines, 1)}
        done = 0
        for future in as_completed(futures):
            idx, outfile = future.result()
            results[idx] = outfile
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{len(lines)} rendered")

    # Order files and split by act
    ordered = [results[i] for i in range(1, len(lines) + 1)]
    act_files = [[] for _ in range(num_acts)]
    for i, (_, _, act) in enumerate(lines):
        act_files[act].append(ordered[i])

    silence = make_silence()

    # Assemble 4 MP3s
    print("\nAssembling...")
    names = [f"iwts-act{i+1}" for i in range(num_acts)]
    act_mp3s = []
    for i, name in enumerate(names):
        raw = assemble_mp3(act_files[i], silence, name)
        final = OUTDIR / f"{name}.mp3"
        prepend_cold_open(raw, final)
        raw.unlink()  # clean up raw
        size = final.stat().st_size // 1024
        print(f"  {name}.mp3 ({size}KB)")
        act_mp3s.append(final)

    # Full episode = all files
    raw_full = assemble_mp3(ordered, silence, "iwts-full")
    full = OUTDIR / "iwts-full.mp3"
    prepend_cold_open(raw_full, full)
    raw_full.unlink()
    size = full.stat().st_size // 1024
    print(f"  iwts-full.mp3 ({size}KB)")

    # Copy to prod static dir
    print("\nCopying to prod...")
    shutil.copy2(full, PROD_DIR / "i-want-to-share.mp3")
    for i, mp3 in enumerate(act_mp3s, 1):
        shutil.copy2(mp3, PROD_DIR / "sections" / f"act{i}.mp3")
        print(f"  → sections/act{i}.mp3")
    shutil.copy2(SCRIPT, PROD_DIR / "transcript-i-want-to-share.md")
    print("  → transcript-i-want-to-share.md")
    print("Done.")
