#!/usr/bin/env python3
"""Generate any episode from a markdown script using Qwen3-TTS voice cloning.

Reads [SPEAKER] tags from any script file. Resolves voices from a shared
voice map. Each episode gets its own output directory. Incremental — skips
cached lines, resumes on restart.

Usage:
    python generate_episode.py vic-and-sam.md
    python generate_episode.py wall-of-data.md --batch 20
    python generate_episode.py vic-and-sam.md --assemble-only
    python generate_episode.py vic-and-sam.md --cold-open cold-open.md
"""

import argparse
import gc
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf

try:
    import torch
except ImportError:
    torch = None  # Only needed for generation, not assembly

BASE_DIR = Path(__file__).parent

# ── Voice reference map ──────────────────────────────────────────────
# Speaker tag → voice reference WAV path (relative to ~/voices/ on DGX
# or ~/w9/wall/ locally). Resolver tries multiple locations.

# ── Draft voice map (macOS TTS understudies) ─────────────────────────
# Used with --draft flag. No GPU, no DGX, renders locally via `say`.
# Format: speaker tag → (macos_voice_name, engine)
# engine: "say" for macOS TTS, "espeak" for espeak-ng

DRAFT_VOICE_MAP = {
    # Main cast — macOS natural voices
    "SAM":             ("Rishi", "say"),
    "SAM-HYPE":        ("Daniel", "say"),
    "VIC":             ("Daniel", "say"),
    "AUBREY":          ("Moira", "say"),
    "KAI":             ("Karen", "say"),
    "CHARLOTTE":       ("Samantha", "say"),
    "KAREN":           ("Karen", "say"),
    "HEADLINE":        ("Karen", "say"),
    "PARROT":          ("Karen", "say"),
    "OCTOPUS":         ("Tessa", "say"),
    "RICH":            ("Rishi", "say"),
    "VIC-U":           ("Moira", "say"),
    "SAM-U":           ("Daniel", "say"),
    "ERROR":           ("Fred", "say"),
    "CRAB":            ("Moira", "say"),
    "JAMES":           ("Daniel", "say"),
    "HYPE":            ("Tessa", "say"),
    "STAGE":           ("Samantha", "say"),

    # Episode 1-2 legacy
    "NARRATOR":        ("Daniel", "say"),
    "SHAPE":           ("Daniel", "say"),
    "SHAPE-CLOSE":     ("Eddy (English (US))", "say"),
    "SHAPE-WARN":      ("Tessa", "say"),
    "TRAVELLER":       ("Daniel", "say"),
    "DEAN":            ("Rishi", "say"),
    "HANN":            ("Daniel", "say"),
    "ELIZA":           ("Moira", "say"),
    "HERBERT":         ("Rishi", "say"),
    "ARTHUR":          ("Daniel", "say"),

    # Episode 3 extras
    "VIC-EXPLORER":    ("Daniel", "say"),
    "VIC-COMPLIANCE":  ("Fred", "say"),
    "VIC-STEWARD":     ("Rishi", "say"),

    # Roll call — robot voices (they're uncast, robotic fits)
    "LEIA-WHISPER":    ("en+f3 -p 95", "espeak"),     # 354 Hz — highest
    "HANN-SHOUT":      ("en+m3 -p 80", "espeak"),     # 327 Hz
    "LUC-SHOUT":       ("en+m2 -p 75", "espeak"),     # 317 Hz
    "LEIA-CHAT":       ("en+f2 -p 70", "espeak"),     # 277 Hz
    "VAYDAR-CHAT":     ("en+m1 -p 55", "espeak"),     # 232 Hz
    "NARRATOR-WELLS":  ("en -p 40", "espeak"),         # 161 Hz
    "LUC":             ("en+m2 -p 30", "espeak"),      # 135 Hz
    "LUC-WHISPER":     ("en+whisper -p 45", "espeak"), # 191 Hz
    "HANN-WHISPER":    ("en+croak -p 20", "espeak"),   # 118 Hz
    "VAYDAR-WHISPER":  ("en+m1 -p 12", "espeak"),      # 99 Hz
    "BEN-WHISPER":     ("en -p 10 -s 120", "espeak"),  # 97 Hz — lowest
}

# Speakers that have real rendered WAVs already — skip TTS in draft mode
DRAFT_USE_REAL = {"CHARLOTTE", "JAMES"}


def generate_draft_line(speaker, text, out_path):
    """Render a single line using macOS say or espeak-ng. Returns sample rate."""
    if speaker not in DRAFT_VOICE_MAP:
        sys.exit(f"No draft voice mapped for [{speaker}]. Add it to DRAFT_VOICE_MAP.")

    voice_spec, engine = DRAFT_VOICE_MAP[speaker]

    if engine == "say":
        # macOS say → AIFF → WAV via ffmpeg
        aiff_path = out_path.with_suffix(".aiff")
        subprocess.run(
            ["say", "-v", voice_spec, "-o", str(aiff_path), text],
            check=True, capture_output=True,
        )
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(aiff_path),
             "-ar", "24000", "-ac", "1", str(out_path)],
            check=True, capture_output=True,
        )
        aiff_path.unlink()
    elif engine == "espeak":
        # espeak-ng -v <voice_spec> -w output.wav "text"
        # voice_spec may include flags like "en+f3 -p 95"
        parts = voice_spec.split()
        cmd = ["espeak-ng", "-v", parts[0]] + parts[1:] + ["-w", str(out_path), text]
        subprocess.run(cmd, check=True, capture_output=True)
        # Resample to 24kHz mono
        tmp_path = out_path.with_suffix(".tmp.wav")
        out_path.rename(tmp_path)
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(tmp_path),
             "-ar", "24000", "-ac", "1", str(out_path)],
            check=True, capture_output=True,
        )
        tmp_path.unlink()
    else:
        sys.exit(f"Unknown draft engine '{engine}' for [{speaker}].")

    return 24000


def generate_draft_episode(script_path, cold_open_path=None):
    """Generate all lines using local TTS (macOS say + espeak-ng) and assemble."""
    episode_name = script_path.stem
    output_dir = BASE_DIR / "output" / f"{episode_name}-draft"
    output_dir.mkdir(parents=True, exist_ok=True)
    lines_dir = output_dir / "lines"
    lines_dir.mkdir(exist_ok=True)

    # Real lines dir for DRAFT_USE_REAL speakers
    real_lines_dir = BASE_DIR / "output" / episode_name / "lines"

    segments = []
    if cold_open_path and cold_open_path.exists():
        segments.extend(parse_script(cold_open_path))
        segments.append(("BREAK", ""))
        print(f"Cold open: {cold_open_path.name}")
    segments.extend(parse_script(script_path))

    voice_lines = [(s, t) for s, t in segments if s != "BREAK"]
    speakers = sorted(set(s for s, _ in voice_lines))
    print(f"Episode: {episode_name} (DRAFT)")
    print(f"Parsed {len(segments)} segments ({len(voice_lines)} voice lines)")
    print(f"Speakers: {', '.join(speakers)}")

    # Check all speakers have draft voices (except DRAFT_USE_REAL)
    for s in speakers:
        if s not in DRAFT_VOICE_MAP and s not in DRAFT_USE_REAL:
            sys.exit(f"No draft voice for [{s}]. Add to DRAFT_VOICE_MAP or DRAFT_USE_REAL.")

    seq = 0
    generated = 0
    cached = 0
    reused_real = 0
    t_start = time.time()

    for speaker, text in segments:
        if speaker == "BREAK":
            continue

        seq += 10
        found = find_line_file(lines_dir, speaker, text, seq)

        if found:
            cached += 1
            continue

        out_path = lines_dir / line_filename(speaker, text, seq)

        # Try to reuse real rendered WAVs for certain speakers
        if speaker in DRAFT_USE_REAL:
            slug = line_slug(speaker, text)
            real_matches = []
            # Search the episode's own real lines dir first
            if real_lines_dir.exists():
                real_matches = list(real_lines_dir.glob(f"*_{slug}.wav"))
            # Then search all other episode output dirs
            if not real_matches:
                for other_dir in sorted((BASE_DIR / "output").iterdir()):
                    if other_dir.name.endswith("-draft"):
                        continue
                    other_lines = other_dir / "lines"
                    if other_lines.exists():
                        real_matches = list(other_lines.glob(f"*_{slug}.wav"))
                        if real_matches:
                            break
            if real_matches:
                import shutil
                shutil.copy2(str(real_matches[0]), str(out_path))
                reused_real += 1
                print(f"  [{seq:03d}] {speaker}: (real voice) {text[:50]}...")
                continue

        generate_draft_line(speaker, text, out_path)
        generated += 1

        if generated <= 3 or generated % 25 == 0:
            print(f"  [{seq:03d}] {speaker}: {text[:50]}...")

    elapsed = time.time() - t_start
    print(f"\nDraft: {generated} rendered, {cached} cached, "
          f"{reused_real} real reused — {elapsed:.1f}s total")

    _assemble(segments, lines_dir, output_dir, f"{episode_name}-draft")


VOICE_MAP = {
    # Episode 1: Shapes for Rich
    "NARRATOR":    "dorian-moreau.wav",
    "SHAPE":       "cast/old_ben_kenobi_conversation.wav",
    "SHAPE-CLOSE": "cast/ser_vaydar_whisper.wav",
    "SHAPE-WARN":  "cast/lady_leia_commanding.wav",

    # Episode 2: The Lightweight Wall
    "TRAVELLER":   "wells-bttf/the-traveller.wav",
    "DEAN":        "wells-bttf/dean-griffin.wav",
    "HANN":        "cast/hann_of_soloh_conversation.wav",
    "ELIZA":       "wells-bttf/eliza.wav",
    "HERBERT":     "wells-bttf/young-herbert.wav",
    "ARTHUR":      "wells-bttf/arthur.wav",

    # Episode 3: Vic and Sam
    "VIC":             "wells-bttf/dorian-moreau.wav",
    "VIC-EXPLORER":    "wells-bttf/dean-griffin.wav",
    "VIC-COMPLIANCE":  "cast/ser_vaydar_commanding.wav",
    "VIC-STEWARD":     "cast/hann_of_soloh_whisper.wav",
    "SAM":             "cast/old_ben_kenobi_conversation.wav",
    "SAM-HYPE":        "cast/old_ben_kenobi_commanding.wav",
    "STAGE":           "smithers_clone.wav",
    "HYPE":            "cast/lady_leia_commanding.wav",
    "AUBREY":          "aubrey.wav",
    "KAI":             "aubrey.wav",  # Same voice, emphasis boost handles the LOUD
    "CHARLOTTE":       "cast/charlotte_conversation.wav",

    # Roll call voices (ep 3 wall tour)
    "LEIA-WHISPER":    "cast/lady_leia_whisper.wav",
    "LEIA-CHAT":       "cast/lady_leia_conversation.wav",
    "HANN-SHOUT":      "cast/hann_of_soloh_shout.wav",
    "HANN-WHISPER":    "cast/hann_of_soloh_whisper.wav",
    "LUC-SHOUT":       "cast/luc_skywalden_shout.wav",
    "LUC-WHISPER":     "cast/luc_skywalden_whisper.wav",
    "LUC":             "cast/luc_skywalden_conversation.wav",
    "VAYDAR-CHAT":     "cast/ser_vaydar_conversation.wav",
    "VAYDAR-WHISPER":  "cast/ser_vaydar_whisper.wav",
    "BEN-WHISPER":     "cast/old_ben_kenobi_whisper.wav",
    "NARRATOR-WELLS":  "wells-bttf/narrator.wav",

    # Shared
    "JAMES":       "james_reference.wav",
}

# RMS scaling per speaker (1.0 = normal, <1 = quieter, >1 = louder)
VOLUME_SCALE = {
    "STAGE":     0.7,   # Stage directions mixed quieter
    "SAM":       0.85,  # Ben Kenobi runs hot, pull back slightly
    "KAI":       1.4,   # She's shy but LOUD
    "CHARLOTTE": 0.9,   # Warm, slightly pulled back
    "AUBREY":    0.95,  # Flat, resigned
}

# Emphasis boost: lines with ! get a small volume lift
EMPHASIS_BOOST = 1.30

# Stereo pan: -1.0 = full left, 0.0 = center, 1.0 = full right
STEREO_PAN = {
    "VIC":   -0.30,   # Left 30%
    "SAM":    0.30,   # Right 30%
    "STAGE":  0.00,   # Center
    "JAMES":  0.00,   # Center
}

# Telephone filter for stage directions (bandpass 300-3400 Hz)
TELEPHONE_SPEAKERS = {"STAGE"}

# Wall speaker filter — voices that interrupt from the wall speakers
# Wider bandpass than telephone, with extra reverb and volume boost
WALL_SPEAKERS = {"HANN-SHOUT", "LEIA-CHAT"}

# Roll call speakers — these overlap in assembly instead of playing sequentially
ROLL_CALL_SPEAKERS = {
    "LEIA-WHISPER", "HANN-SHOUT", "LUC-SHOUT", "LEIA-CHAT",
    "VAYDAR-CHAT", "DEAN", "TRAVELLER", "LUC-WHISPER",
    "HERBERT", "ARTHUR", "ELIZA", "NARRATOR-WELLS",
    "LUC", "HANN-WHISPER", "VAYDAR-WHISPER", "BEN-WHISPER",
}
ROLL_CALL_TARGET = 2/3  # compress roll call to this fraction of sequential time

# Fade in/out duration (seconds)
FADE_IN = 0.05  # Just an anti-click, not a dramatic ramp
FADE_OUT = 2.0

# Room tone: faint pink noise in pauses
ROOM_TONE_LEVEL = 0.003

# Pause durations (seconds)
PAUSE_SAME_SPEAKER = 0.4
PAUSE_SPEAKER_CHANGE = 0.8
PAUSE_SECTION_BREAK = 2.0

# Assembly normalization
TARGET_RMS = 0.045
PEAK_LIMIT = 0.95


def resolve_voice(speaker):
    """Find the voice reference WAV for a speaker tag."""
    if speaker not in VOICE_MAP:
        sys.exit(f"No voice mapped for [{speaker}]. Add it to VOICE_MAP.")

    ref = VOICE_MAP[speaker]

    # Search paths in priority order
    search = [
        Path.home() / "voices" / ref,          # DGX: ~/voices/
        Path.home() / "w9" / "wall" / ref,     # Local: ~/w9/wall/
        BASE_DIR / "voices" / ref,              # Project: audiobook/voices/
        BASE_DIR / "voices" / "harvest" / ref,  # Harvest dir
    ]
    # Also try without subdirectory (flat layout)
    flat = Path(ref).name
    search += [
        Path.home() / "voices" / flat,
        Path.home() / "w9" / "wall" / flat,
        BASE_DIR / "voices" / flat,
    ]

    for i, p in enumerate(search):
        if p.exists():
            if i > 0:  # Not the first (preferred) path
                print(f"  FALLBACK: {speaker} voice found at path #{i+1}: {p}")
            return p

    tried = "\n  ".join(str(s) for s in search)
    sys.exit(f"Voice ref not found for [{speaker}] ({ref}):\n  {tried}")


def line_slug(speaker, text):
    """Content slug: speaker + hash of text. The stable, cache-safe part."""
    h = hashlib.sha256(text.encode()).hexdigest()[:12]
    tag = speaker.lower().replace('-', '_')
    return f"{tag}_{h}"


def line_filename(speaker, text, seq=0):
    """Sequenced content-addressed filename: seq_speaker_hash.wav

    Sequence numbers count by 10s for easy insertion (Apple II style).
    The hash is authoritative for cache; the sequence is for human readability.
    """
    slug = line_slug(speaker, text)
    return f"{seq:03d}_{slug}.wav"


def find_line_file(lines_dir, speaker, text, seq=0):
    """Find a line's WAV, tolerating sequence renumbering.

    Tries exact match first (seq_speaker_hash.wav), then falls back to
    any file matching *_speaker_hash.wav. If found under a different seq,
    renames it to the current seq.
    """
    slug = line_slug(speaker, text)
    exact = lines_dir / f"{seq:03d}_{slug}.wav"
    if exact.exists():
        return exact

    # Fallback: find by hash under any sequence prefix
    matches = list(lines_dir.glob(f"*_{slug}.wav"))
    if matches:
        old_name = matches[0].name
        matches[0].rename(exact)
        print(f"  FALLBACK: {old_name} → {exact.name} (seq renumber)")
        return exact

    # Legacy: bare slug without sequence prefix (pre-migration)
    bare = lines_dir / f"{slug}.wav"
    if bare.exists():
        print(f"  FALLBACK: {bare.name} → {exact.name} (legacy migration)")
        bare.rename(exact)
        return exact

    return None


def parse_script(path):
    """Parse a markdown script into [(speaker, text), ...] segments.

    Recognizes any [UPPERCASE-TAG] as a speaker. --- = section break.
    Skips lines starting with > (directives) and # (headers).
    """
    text = path.read_text()

    # Strip everything before "## Script"
    script_start = text.find("## Script")
    if script_start >= 0:
        text = text[script_start:]

    segments = []
    current_speaker = None
    current_lines = []
    tag_re = re.compile(r'^\[([A-Z][A-Z0-9-]*)\]\s*$')

    for line in text.split('\n'):
        stripped = line.strip()

        # Section break
        if stripped == '---':
            if current_speaker and current_lines:
                segments.append((current_speaker, ' '.join(current_lines).strip()))
                current_lines = []
            segments.append(("BREAK", ""))
            current_speaker = None
            continue

        # Speaker tag
        m = tag_re.match(stripped)
        if m:
            if current_speaker and current_lines:
                segments.append((current_speaker, ' '.join(current_lines).strip()))
                current_lines = []
            current_speaker = m.group(1)
            continue

        # Skip directives, headers, empty lines outside a speaker block
        if stripped.startswith('>') or stripped.startswith('#') or not stripped:
            continue

        if current_speaker:
            current_lines.append(stripped)

    # Flush
    if current_speaker and current_lines:
        segments.append((current_speaker, ' '.join(current_lines).strip()))

    return segments


def trim_leading_silence(audio, sr, threshold=0.01, max_trim_s=1.0):
    """Trim leading silence/breathing from generated audio."""
    max_samples = int(max_trim_s * sr)
    abs_audio = np.abs(audio)
    above = np.where(abs_audio > threshold)[0]
    if len(above) == 0:
        return audio
    start = min(above[0], max_samples)
    start = max(0, start - int(0.02 * sr))
    return audio[start:]


def trim_trailing_silence(audio, sr, rms_thresh=0.005, window_s=0.25,
                          min_gap_s=0.75, keep_s=0.15):
    """Trim trailing dead space from TTS output.

    TTS sometimes generates silence followed by spurious pops after the
    voice stops. Scans the back half of the audio for the longest silence
    gap. If that gap is > min_gap_s and there's little signal after it
    relative to before, trim at the gap start.
    """
    window = int(window_s * sr)
    n = len(audio)
    if n < window * 4:
        return audio

    # Build RMS profile per window
    is_signal = []
    starts = []
    for start in range(0, n - window + 1, window):
        chunk = audio[start:start + window]
        rms = np.sqrt(np.mean(chunk ** 2))
        is_signal.append(rms >= rms_thresh)
        starts.append(start)

    # Find all silence gaps in the back half
    half = len(is_signal) // 2
    best_gap_start = None
    best_gap_len = 0
    gap_start_idx = None

    for idx in range(half, len(is_signal)):
        if not is_signal[idx]:
            if gap_start_idx is None:
                gap_start_idx = idx
        else:
            if gap_start_idx is not None:
                gap_len = idx - gap_start_idx
                if gap_len > best_gap_len:
                    best_gap_len = gap_len
                    best_gap_start = gap_start_idx
                gap_start_idx = None
    # Check if we ended in a gap
    if gap_start_idx is not None:
        gap_len = len(is_signal) - gap_start_idx
        if gap_len > best_gap_len:
            best_gap_len = gap_len
            best_gap_start = gap_start_idx

    if best_gap_start is None:
        return audio

    gap_duration_s = best_gap_len * window_s
    if gap_duration_s < min_gap_s:
        return audio

    # Trim at the start of the longest gap
    trim_sample = starts[best_gap_start] + int(keep_s * sr)
    return audio[:min(trim_sample, n)]


def add_reverb(audio, sr, decay=0.3, delay_ms=40, taps=6):
    """Simple reverb: repeated decaying echoes."""
    result = audio.copy()
    for i in range(1, taps + 1):
        offset = int(sr * delay_ms * i / 1000)
        gain = decay ** i
        padded = np.zeros(len(result))
        if offset < len(audio):
            padded[offset:offset + len(audio) - offset] = audio[:len(audio) - offset] * gain
            result += padded[:len(result)]
    return result


def horror_filter(audio, sr):
    """Growl on 'No!', back off to dry by 'exists' (~4.1s).

    0.0-0.8s: full blast — telephone + heavy overdrive + pitch drop + tight reverb
    0.8-1.3s: crossfade blast → medium grit
    1.3-4.1s: grit fading to fully dry
    4.1s+:    clean/dry (normal voice)
    """
    n = len(audio)
    hit_end = min(int(0.8 * sr), n)
    xfade_end = min(int(1.3 * sr), n)
    dry_by = min(int(4.1 * sr), n)  # "exists" ends here

    # === Full blast ===
    drive_heavy = 5.0
    blast = np.tanh(audio * drive_heavy) / np.tanh(drive_heavy)
    blast = telephone_filter(blast, sr, low=200, high=4000)
    blast = add_reverb(blast, sr, decay=0.2, delay_ms=25, taps=3)
    idx = np.linspace(0, n - 1, int(n * 1.08)).astype(int)
    idx = np.clip(idx, 0, n - 1)
    blast = blast[idx][:n]

    # === Medium grit ===
    drive_med = 2.0
    grit = np.tanh(audio * drive_med) / np.tanh(drive_med)
    grit = add_reverb(grit, sr, decay=0.15, delay_ms=30, taps=3)

    result = np.zeros(n)

    # Phase 1: full blast
    result[:hit_end] = blast[:hit_end]

    # Phase 2: blast → grit
    xfade_len = xfade_end - hit_end
    ramp = np.linspace(1.0, 0.0, xfade_len)
    result[hit_end:xfade_end] = (
        blast[hit_end:xfade_end] * ramp +
        grit[hit_end:xfade_end] * (1.0 - ramp)
    )

    # Phase 3: grit → dry (fully clean by "exists")
    fade_len = dry_by - xfade_end
    if fade_len > 0:
        ramp = np.linspace(1.0, 0.0, fade_len)
        result[xfade_end:dry_by] = (
            grit[xfade_end:dry_by] * ramp +
            audio[xfade_end:dry_by] * (1.0 - ramp)
        )

    # Phase 4: fully dry
    if dry_by < n:
        result[dry_by:] = audio[dry_by:]

    return result


def normalize(audio, target_rms=TARGET_RMS, peak_limit=PEAK_LIMIT):
    """RMS normalize with soft peak limiter."""
    rms = np.sqrt(np.mean(audio ** 2))
    if rms > 0:
        audio = audio * (target_rms / rms)
    peak = np.max(np.abs(audio))
    if peak > peak_limit:
        audio = audio * (peak_limit / peak)
    return audio


def telephone_filter(audio, sr, low=300, high=3400):
    """Bandpass filter to simulate telephone/intercom quality."""
    # Simple brick-wall FFT filter
    n = len(audio)
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    spectrum = np.fft.rfft(audio)
    mask = (freqs >= low) & (freqs <= high)
    spectrum[~mask] = 0
    return np.fft.irfft(spectrum, n)


def wall_speaker_filter(audio, sr):
    """Filter for voices coming from wall speakers — wider than telephone,
    with volume boost and extra reverb to sound like room speakers."""
    # Mild bandpass (200-5000 Hz) — less harsh than telephone
    n = len(audio)
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    spectrum = np.fft.rfft(audio)
    mask = (freqs >= 200) & (freqs <= 5000)
    spectrum[~mask] = 0
    audio = np.fft.irfft(spectrum, n)
    # Volume boost — these need to cut through
    audio = audio * 1.5
    # Extra reverb — room speaker bounce
    audio = add_reverb(audio, sr, decay=0.4, delay_ms=30, taps=8)
    return audio


def pan_stereo(audio, pan=0.0):
    """Pan mono audio to stereo. pan: -1=left, 0=center, 1=right."""
    left_gain = np.sqrt(0.5 * (1.0 - pan))
    right_gain = np.sqrt(0.5 * (1.0 + pan))
    return np.column_stack([audio * left_gain, audio * right_gain])


def pink_noise(n):
    """Generate pink noise (1/f) using Voss-McCartney algorithm."""
    white = np.random.randn(n)
    # Simple 1/f approximation: cumulative filter
    b = np.array([0.049922035, -0.095993537, 0.050612699, -0.004709510])
    a = np.array([1.0, -2.494956002, 2.017265875, -0.522189400])
    # Use rolling average as cheap approximation
    kernel = np.ones(64) / 64
    pink = np.convolve(white, kernel, mode='same')
    return pink / (np.max(np.abs(pink)) + 1e-10)


def make_room_tone(length, sr, level=ROOM_TONE_LEVEL):
    """Generate stereo room tone (faint pink noise). Returns silence if DRY_MIX."""
    if DRY_MIX:
        return np.zeros((length, 2))
    noise = pink_noise(length) * level
    return np.column_stack([noise, noise])


def generate_episode(script_path, cold_open_path=None, batch_size=0,
                     assemble_only=False):
    """Generate all lines for an episode and assemble."""
    episode_name = script_path.stem
    output_dir = BASE_DIR / "output" / episode_name
    output_dir.mkdir(parents=True, exist_ok=True)
    lines_dir = output_dir / "lines"
    lines_dir.mkdir(exist_ok=True)
    prompt_cache_dir = output_dir / "prompt_cache"
    prompt_cache_dir.mkdir(exist_ok=True)

    # Parse script (with optional cold open prepended)
    segments = []
    if cold_open_path and cold_open_path.exists():
        segments.extend(parse_script(cold_open_path))
        segments.append(("BREAK", ""))
        print(f"Cold open: {cold_open_path.name}")

    segments.extend(parse_script(script_path))

    voice_lines = [(s, t) for s, t in segments if s != "BREAK"]
    speakers = sorted(set(s for s, _ in voice_lines))
    print(f"Episode: {episode_name}")
    print(f"Parsed {len(segments)} segments ({len(voice_lines)} voice lines)")
    print(f"Speakers: {', '.join(speakers)}")

    if assemble_only:
        _assemble(segments, lines_dir, output_dir, episode_name)
        return

    # Resolve all voice references (only needed for generation)
    ref_paths = {}
    for speaker in speakers:
        ref_paths[speaker] = resolve_voice(speaker)
        print(f"  {speaker:15s} → {ref_paths[speaker].name}")

    # Check if any lines need generating
    needs_generation = False
    seq = 0
    for speaker, text in segments:
        if speaker == "BREAK":
            continue
        seq += 10
        found = find_line_file(lines_dir, speaker, text, seq)
        if not found:
            needs_generation = True
            break

    if not needs_generation:
        print("All lines cached — assembling directly.")
        _assemble(segments, lines_dir, output_dir, episode_name)
        return

    # Load model
    device = "cuda" if torch.cuda.is_available() else (
        "mps" if torch.backends.mps.is_available() else "cpu"
    )
    dtype = torch.float32
    print(f"Device: {device}")

    from qwen_tts import Qwen3TTSModel
    print("Loading Qwen3-TTS 0.6B Base...")
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-0.6B-Base",
        device_map=device, dtype=dtype,
    )

    # Build input manifest — trace every input before committing to the run
    manifest = {
        "episode": episode_name,
        "speakers": {},
        "cross_similarity": {},
    }
    for speaker in speakers:
        ref_hash = hashlib.sha256(
            ref_paths[speaker].read_bytes()).hexdigest()[:8]
        manifest["speakers"][speaker] = {
            "voice_ref": str(ref_paths[speaker]),
            "voice_ref_hash": ref_hash,
            "voice_map_entry": VOICE_MAP.get(speaker, "MISSING"),
            "prompt_cache": "PENDING",
        }

    # Compute voice prompts (cached per episode, keyed by voice ref hash)
    # If the voice reference WAV changes, the cache auto-invalidates.
    prompt_cache = {}
    for speaker in speakers:
        tag = speaker.lower().replace('-', '_')
        ref_hash = manifest["speakers"][speaker]["voice_ref_hash"]
        cache_file = prompt_cache_dir / f"{tag}_{ref_hash}.pt"

        if cache_file.exists():
            try:
                prompt_cache[speaker] = torch.load(
                    cache_file, map_location=device, weights_only=False)
                print(f"  Loaded cached prompt: {speaker} (ref {ref_hash})")
                manifest["speakers"][speaker]["prompt_cache"] = "HIT"
                continue
            except Exception as e:
                print(f"  FALLBACK: {speaker} prompt cache load failed: {e}")
                manifest["speakers"][speaker]["prompt_cache"] = f"LOAD_FAILED: {e}"

        # Invalidate any stale caches for this speaker (different ref hash)
        for stale in prompt_cache_dir.glob(f"{tag}_*.pt"):
            if stale != cache_file:
                stale.unlink()
                print(f"  Invalidated stale prompt: {stale.name}")

        print(f"  Computing voice prompt: {speaker} ({ref_paths[speaker].name}, ref {ref_hash})")
        prompts = model.create_voice_clone_prompt(
            ref_audio=str(ref_paths[speaker]), x_vector_only_mode=True,
        )
        prompt_cache[speaker] = prompts[0]
        torch.save(prompts[0], cache_file)
        manifest["speakers"][speaker]["prompt_cache"] = "FRESH"
        print(f"    → cached to {cache_file.name}")

    # Extract reference x-vectors for voice verification
    def get_xvector(prompt_item):
        """Extract speaker embedding — field name varies across qwen_tts versions."""
        for attr in ('x_vector', 'ref_spk_embedding'):
            v = getattr(prompt_item, attr, None)
            if v is not None:
                return v
        available = [a for a in dir(prompt_item) if not a.startswith('_')]
        sys.exit(f"Cannot find x-vector on {type(prompt_item).__name__}. "
                 f"Available attrs: {available}")

    ref_xvecs = {}
    for speaker in speakers:
        ref_prompts = model.create_voice_clone_prompt(
            ref_audio=str(ref_paths[speaker]), x_vector_only_mode=True,
        )
        ref_xvec = get_xvector(ref_prompts[0])
        ref_xvecs[speaker] = ref_xvec / ref_xvec.norm()

    # Cross-similarity matrix: catch accidental voice duplicates
    speaker_list = sorted(ref_xvecs.keys())
    for i, a in enumerate(speaker_list):
        for b in speaker_list[i + 1:]:
            sim = torch.dot(ref_xvecs[a].flatten(),
                            ref_xvecs[b].flatten()).item()
            pair = f"{a}/{b}"
            manifest["cross_similarity"][pair] = round(sim, 3)
            if sim > 0.90:
                print(f"  WARNING: {a} and {b} sound very similar "
                      f"(sim={sim:.3f}). Intentional?")

    # Write pre-generation manifest — trace inputs BEFORE committing to the run
    import datetime
    manifest["status"] = "STARTED"
    manifest["total_lines"] = len([s for s, _ in segments if s != "BREAK"])
    manifest["timestamp_start"] = datetime.datetime.now().isoformat()
    manifest_path = output_dir / "voice-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"\nInput manifest: {manifest_path}")
    print("--- Review inputs above before generation proceeds ---\n")

    # Generate lines
    seq = 0
    generated = 0
    cached = 0
    verified_speakers = set()  # Smoke test: one check per speaker

    for speaker, text in segments:
        if speaker == "BREAK":
            continue

        seq += 10
        found = find_line_file(lines_dir, speaker, text, seq)

        if found:
            cached += 1
            if cached <= 5 or cached % 20 == 0:
                print(f"  [{seq:03d}] (cached) {speaker}: {text[:50]}...")
            continue

        out_path = lines_dir / line_filename(speaker, text, seq)
        voice_prompt = prompt_cache[speaker]
        wavs, sr = model.generate_voice_clone(
            text=text, language="English",
            voice_clone_prompt=[voice_prompt],
        )
        audio = trim_leading_silence(wavs[0], sr)
        sf.write(str(out_path), audio, sr)
        generated += 1
        duration = len(audio) / sr
        print(f"  [{seq:03d}] {speaker}: {text[:50]}... ({duration:.1f}s)")

        # Voice smoke test: verify first generated line per speaker
        if speaker not in verified_speakers:
            verified_speakers.add(speaker)
            gen_prompts = model.create_voice_clone_prompt(
                ref_audio=str(out_path), x_vector_only_mode=True,
            )
            gen_xvec = get_xvector(gen_prompts[0])
            gen_xvec = gen_xvec / gen_xvec.norm()
            sim = torch.dot(ref_xvecs[speaker].flatten(),
                            gen_xvec.flatten()).item()
            manifest["speakers"][speaker]["smoke_test"] = {
                "line": text[:80],
                "similarity": round(sim, 3),
                "file": out_path.name,
            }
            print(f"  VOICE CHECK [{speaker}]: similarity {sim:.3f}")
            if sim < 0.70:
                print(f"\n  VOICE MISMATCH: {speaker} generated audio "
                      f"does not match reference (sim={sim:.3f} < 0.70)")
                print(f"  Reference: {ref_paths[speaker]}")
                print(f"  Generated: {out_path}")
                print(f"  STOPPING. Delete prompt cache and check VOICE_MAP.")
                sys.exit(1)

        # Gate 3: Batch voiceprint after 5 generated lines
        # Quick pitch/family check before committing to the remaining run.
        if generated == 5:
            print("\n--- GATE 3: Batch voiceprint (5 lines) ---")
            from voiceprint import fingerprint_file as vp_fingerprint, load_db, identify
            try:
                vp_db = load_db()
                batch_ok = True
                for bp_speaker, bp_text in segments:
                    if bp_speaker == "BREAK":
                        continue
                    bp_file = find_line_file(lines_dir, bp_speaker, bp_text, 0)
                    if not bp_file:
                        continue
                    bp_fp = vp_fingerprint(bp_file)
                    bp_results = identify(bp_fp, vp_db)
                    bp_best, bp_sim = bp_results[0]
                    ref_entry = VOICE_MAP.get(bp_speaker, "?")
                    ref_stem = Path(ref_entry).stem
                    ref_family = str(Path(ref_entry).parent)
                    if ref_family == ".":
                        ref_family = ref_stem
                    # Pitch check
                    ref_fp_db = None
                    for vn, vfp in vp_db.items():
                        if ref_stem in vn:
                            ref_fp_db = vfp
                            break
                    pitch_ok = True
                    if ref_fp_db and ref_fp_db["f0_mean"] > 0 and bp_fp["f0_mean"] > 0:
                        ratio = bp_fp["f0_mean"] / ref_fp_db["f0_mean"]
                        if not (0.6 <= ratio <= 1.4):
                            pitch_ok = False
                    status = "OK" if pitch_ok else "PITCH_FAIL"
                    print(f"  [{bp_speaker:5s}] {status:10s} "
                          f"f0={bp_fp['f0_mean']:5.0f}Hz  "
                          f"best={bp_best}  "
                          f"{bp_text[:40]}...")
                    if not pitch_ok:
                        batch_ok = False
                if not batch_ok:
                    print("\n  BATCH VOICEPRINT FAILED. Pitch mismatch detected.")
                    print("  STOPPING before wasting more DGX time.")
                    print("  Check VOICE_MAP, prompt cache, and voice refs.")
                    manifest["status"] = "BATCH_VOICEPRINT_FAILED"
                    manifest_path.write_text(
                        json.dumps(manifest, indent=2) + "\n")
                    sys.exit(1)
                print("  Batch voiceprint: PASS\n")
            except Exception as e:
                print(f"  Batch voiceprint skipped (no DB): {e}\n")

        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        elif torch.backends.mps.is_available():
            torch.mps.empty_cache()

        if batch_size > 0 and generated >= batch_size:
            print(f"\nBatch limit ({batch_size}). {generated} generated, {cached} cached.")
            del model, prompt_cache
            gc.collect()
            return

    print(f"\nLines: {generated} generated, {cached} cached, {seq // 10} total")

    # Update manifest with results
    manifest["status"] = "COMPLETE"
    manifest["generated"] = generated
    manifest["cached"] = cached
    manifest["timestamp_end"] = datetime.datetime.now().isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Voice manifest updated: {manifest_path}")

    del model, prompt_cache
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    print("Model unloaded.")

    _assemble(segments, lines_dir, output_dir, episode_name)


DRY_MIX = False  # Set by --dry flag. Skips all effects.

def _process_line(speaker, text, audio, sr):
    """Apply per-line effects chain. Returns stereo array."""
    audio = trim_trailing_silence(audio, sr)
    audio = normalize(audio)

    scale = VOLUME_SCALE.get(speaker, 1.0)
    if scale != 1.0:
        audio = audio * scale

    if DRY_MIX:
        # Dry: just normalize, scale, and return stereo center
        audio = trim_trailing_silence(audio, sr)
        return pan_stereo(audio, 0.0)

    if '!' in text and speaker not in ('STAGE', 'JAMES'):
        audio = audio * EMPHASIS_BOOST

    if speaker in TELEPHONE_SPEAKERS:
        audio = telephone_filter(audio, sr)

    # Hype gets telephone-filtered when they demo the effect on her
    if 'frequency range' in text and speaker == 'HYPE':
        audio = telephone_filter(audio, sr)

    # Wall speaker filter for voices interrupting from the wall
    if speaker in WALL_SPEAKERS:
        audio = wall_speaker_filter(audio, sr)

    if 'You track it' in text:
        audio = horror_filter(audio, sr)
    else:
        audio = add_reverb(audio, sr)

    audio = trim_trailing_silence(audio, sr)

    pan = STEREO_PAN.get(speaker, 0.0)
    return pan_stereo(audio, pan)


def _mix_roll_call(roll_call_clips, sr):
    """Mix roll call clips with randomized overlap targeting ~2/3 sequential time.

    Each clip starts slightly before the previous one ends, with random
    variation. The total duration compresses to roughly 2/3 of what
    sequential playback would take.
    """
    if not roll_call_clips:
        return np.zeros((0, 2))

    # Calculate sequential total and target
    clip_lengths = [len(c) for c in roll_call_clips]
    sequential_total = sum(clip_lengths)
    target_total = int(sequential_total * 2 / 3)

    # Distribute overlap across clips: each clip overlaps with the next
    # by a random amount, totaling (sequential_total - target_total)
    n = len(roll_call_clips)
    total_overlap = sequential_total - target_total
    if n <= 1:
        return roll_call_clips[0] if roll_call_clips else np.zeros((0, 2))

    # Random overlap per gap, normalized to hit the target
    rng = np.random.default_rng(42)  # Deterministic for reproducibility
    raw = rng.random(n - 1)
    raw = raw / raw.sum() * total_overlap
    overlaps = raw.astype(int)

    # Compute onset positions
    onsets = [0]
    for i in range(n - 1):
        next_onset = onsets[-1] + clip_lengths[i] - overlaps[i]
        onsets.append(max(onsets[-1] + int(0.1 * sr), next_onset))  # min 100ms gap

    total_len = onsets[-1] + clip_lengths[-1]
    mixed = np.zeros((total_len, 2))

    for i, clip in enumerate(roll_call_clips):
        offset = onsets[i]
        mixed[offset:offset + len(clip)] += clip

    # Normalize the overlap mix
    peak = np.max(np.abs(mixed))
    if peak > PEAK_LIMIT:
        mixed = mixed * (PEAK_LIMIT / peak)

    seq_dur = sequential_total / sr
    mix_dur = total_len / sr
    print(f"    Sequential: {seq_dur:.1f}s → Overlapped: {mix_dur:.1f}s "
          f"({mix_dur/seq_dur*100:.0f}%)")

    return mixed


def _assemble(segments, lines_dir, output_dir, episode_name):
    """Assemble generated lines into a final stereo WAV with full mix."""
    print("\nAssembling (stereo mix)...")
    all_audio = []  # List of stereo arrays (N, 2)
    sr = None
    prev_speaker = None
    seq = 0
    roll_call_buffer = []  # Accumulate roll call clips for overlap

    for speaker, text in segments:
        if speaker == "BREAK":
            # Flush any pending roll call buffer
            if roll_call_buffer:
                mixed = _mix_roll_call(roll_call_buffer, sr)
                all_audio.append(mixed)
                print(f"  ROLL CALL: {len(roll_call_buffer)} voices overlapped")
                roll_call_buffer = []
            if sr:
                pause = np.zeros((int(sr * PAUSE_SECTION_BREAK), 2))
                pause += make_room_tone(pause.shape[0], sr)
                all_audio.append(pause)
            prev_speaker = None
            continue

        seq += 10
        found = find_line_file(lines_dir, speaker, text, seq)
        if not found:
            print(f"  WARNING: missing {line_filename(speaker, text, seq)}")
            continue
        out_path = found

        audio, sr = sf.read(str(out_path))
        stereo = _process_line(speaker, text, audio, sr)

        # Roll call: buffer for overlapping mix
        if speaker in ROLL_CALL_SPEAKERS:
            roll_call_buffer.append(stereo)
            continue

        # Flush any pending roll call buffer before non-roll-call line
        if roll_call_buffer:
            mixed = _mix_roll_call(roll_call_buffer, sr)
            all_audio.append(mixed)
            print(f"  ROLL CALL: {len(roll_call_buffer)} voices overlapped")
            roll_call_buffer = []
            # Pause after roll call
            pause = make_room_tone(int(sr * PAUSE_SPEAKER_CHANGE), sr)
            all_audio.append(pause)

        all_audio.append(stereo)

        # Pause with room tone
        if speaker == prev_speaker:
            pause_dur = PAUSE_SAME_SPEAKER
        else:
            pause_dur = PAUSE_SPEAKER_CHANGE

        # Short exclamations need an extra beat for the listener to process
        word_count = len(text.split())
        if '!' in text and word_count <= 5:
            pause_dur += 0.4

        pause_samples = int(sr * pause_dur)
        pause = make_room_tone(pause_samples, sr)
        all_audio.append(pause)
        prev_speaker = speaker

    # Flush any trailing roll call buffer
    if roll_call_buffer and sr:
        mixed = _mix_roll_call(roll_call_buffer, sr)
        all_audio.append(mixed)
        print(f"  ROLL CALL: {len(roll_call_buffer)} voices overlapped")
        roll_call_buffer = []

    if all_audio and sr:
        combined = np.concatenate(all_audio)

        # Fade in
        fade_in_samples = int(sr * FADE_IN)
        if fade_in_samples > 0 and len(combined) > fade_in_samples:
            ramp = np.linspace(0.0, 1.0, fade_in_samples).reshape(-1, 1)
            combined[:fade_in_samples] *= ramp

        # Fade out
        fade_out_samples = int(sr * FADE_OUT)
        if fade_out_samples > 0 and len(combined) > fade_out_samples:
            ramp = np.linspace(1.0, 0.0, fade_out_samples).reshape(-1, 1)
            combined[-fade_out_samples:] *= ramp

        # Final soft limit (per channel)
        peak = np.max(np.abs(combined))
        if peak > PEAK_LIMIT:
            combined = combined * (PEAK_LIMIT / peak)

        final_path = output_dir / f"{episode_name}.wav"
        sf.write(str(final_path), combined, sr)
        total_min = len(combined) / sr / 60
        print(f"\nOutput: {final_path}")
        print(f"Duration: {total_min:.1f} minutes")
        print(f"Size: {final_path.stat().st_size / (1024 ** 3):.2f} GB"
              if final_path.stat().st_size > 500_000_000 else
              f"Size: {final_path.stat().st_size / (1024 ** 2):.1f} MB")


def renumber_lines(script_path, cold_open_path=None):
    """Re-space all line files back to 10s. No regeneration needed."""
    episode_name = script_path.stem
    lines_dir = BASE_DIR / "output" / episode_name / "lines"

    segments = []
    if cold_open_path and cold_open_path.exists():
        segments.extend(parse_script(cold_open_path))
        segments.append(("BREAK", ""))
    segments.extend(parse_script(script_path))

    seq = 0
    renamed = 0
    for speaker, text in segments:
        if speaker == "BREAK":
            continue
        seq += 10
        slug = line_slug(speaker, text)
        target = lines_dir / f"{seq:03d}_{slug}.wav"

        if target.exists():
            continue

        # Find any file with this slug
        matches = list(lines_dir.glob(f"*_{slug}.wav"))
        # Also check bare slug (legacy)
        bare = lines_dir / f"{slug}.wav"
        if bare.exists():
            matches.append(bare)

        if matches:
            old = matches[0]
            old.rename(target)
            print(f"  {old.name} → {target.name}")
            renamed += 1
        else:
            print(f"  MISSING: {target.name}")

    print(f"\nRenumbered {renamed} files. Sequence: 010 to {seq:03d}.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate an episode from a markdown script")
    parser.add_argument("script", type=Path,
                        help="Script markdown file (e.g. vic-and-sam.md)")
    parser.add_argument("--cold-open", type=Path, default=None,
                        help="Cold open script to prepend (e.g. cold-open.md)")
    parser.add_argument("--batch", type=int, default=0,
                        help="Generate at most N lines then exit (0 = all)")
    parser.add_argument("--assemble-only", action="store_true",
                        help="Skip generation, just assemble from cached lines")
    parser.add_argument("--renumber", action="store_true",
                        help="Re-space sequence numbers back to 10s (no regeneration)")
    parser.add_argument("--draft", action="store_true",
                        help="Use local macOS TTS voices (no GPU/DGX needed)")
    parser.add_argument("--dry", action="store_true",
                        help="Dry mix: no reverb, no filters, no pan, no room tone")
    args = parser.parse_args()

    if args.dry:
        global DRY_MIX
        DRY_MIX = True

    script_path = args.script
    if not script_path.is_absolute():
        script_path = BASE_DIR / script_path

    cold_open = args.cold_open
    if cold_open and not cold_open.is_absolute():
        cold_open = BASE_DIR / cold_open

    if not script_path.exists():
        sys.exit(f"Script not found: {script_path}")

    if args.renumber:
        renumber_lines(script_path, cold_open)
    elif args.draft:
        generate_draft_episode(script_path, cold_open)
    else:
        generate_episode(script_path, cold_open, args.batch, args.assemble_only)


if __name__ == "__main__":
    main()
