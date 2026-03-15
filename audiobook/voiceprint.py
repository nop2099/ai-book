#!/usr/bin/env python3
"""Voice fingerprinting and identification. No torch, no model — just acoustic math.

Extracts MFCCs + pitch stats from a WAV file to build a speaker fingerprint.
Compare fingerprints to identify which voice from a library is speaking.

Usage:
    # Build fingerprint database from all voice refs
    python3 voiceprint.py --build-db

    # Identify a voice
    python3 voiceprint.py identify output/vic-and-sam/lines/050_vic_f6c1472e9afb.wav

    # Compare two files
    python3 voiceprint.py compare fileA.wav fileB.wav

    # Check all lines in an episode against expected voices
    python3 voiceprint.py check vic-and-sam.md --cold-open cold-open.md
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "voice-db.json"

# ── Acoustic feature extraction (numpy + basic FFT) ─────────────

def _mel_filterbank(n_filters, n_fft, sr):
    """Build a mel-scale filterbank matrix."""
    def hz_to_mel(hz):
        return 2595.0 * np.log10(1.0 + hz / 700.0)

    def mel_to_hz(mel):
        return 700.0 * (10.0 ** (mel / 2595.0) - 1.0)

    low_mel = hz_to_mel(80)
    high_mel = hz_to_mel(sr / 2)
    mel_points = np.linspace(low_mel, high_mel, n_filters + 2)
    hz_points = mel_to_hz(mel_points)
    bins = np.floor((n_fft + 1) * hz_points / sr).astype(int)

    fb = np.zeros((n_filters, n_fft // 2 + 1))
    for i in range(n_filters):
        for j in range(bins[i], bins[i + 1]):
            fb[i, j] = (j - bins[i]) / max(bins[i + 1] - bins[i], 1)
        for j in range(bins[i + 1], bins[i + 2]):
            fb[i, j] = (bins[i + 2] - j) / max(bins[i + 2] - bins[i + 1], 1)
    return fb


def extract_mfccs(audio, sr, n_mfcc=13, n_fft=1024, hop=512, n_mels=40):
    """Extract MFCCs from audio. Pure numpy, no librosa."""
    # Pre-emphasis
    audio = np.append(audio[0], audio[1:] - 0.97 * audio[:-1])

    # Frame the signal
    n_frames = 1 + (len(audio) - n_fft) // hop
    if n_frames < 1:
        return np.zeros((1, n_mfcc))

    frames = np.stack([
        audio[i * hop:i * hop + n_fft] * np.hanning(n_fft)
        for i in range(n_frames)
    ])

    # Power spectrum
    spec = np.abs(np.fft.rfft(frames, n_fft)) ** 2
    spec = np.maximum(spec, 1e-10)

    # Mel filterbank
    fb = _mel_filterbank(n_mels, n_fft, sr)
    mel_spec = spec @ fb.T
    mel_spec = np.maximum(mel_spec, 1e-10)
    log_mel = np.log(mel_spec)

    # DCT (type-II) to get MFCCs
    n = log_mel.shape[1]
    dct_matrix = np.zeros((n_mfcc, n))
    for k in range(n_mfcc):
        dct_matrix[k] = np.cos(np.pi * k * (2 * np.arange(n) + 1) / (2 * n))
    mfccs = log_mel @ dct_matrix.T

    return mfccs


def estimate_f0(audio, sr, frame_len=2048, hop=512, fmin=60, fmax=500):
    """Estimate fundamental frequency using autocorrelation. Returns array of f0 per frame."""
    min_lag = int(sr / fmax)
    max_lag = int(sr / fmin)
    n_frames = 1 + (len(audio) - frame_len) // hop
    if n_frames < 1:
        return np.array([0.0])

    f0s = []
    for i in range(n_frames):
        frame = audio[i * hop:i * hop + frame_len]
        frame = frame - np.mean(frame)
        if np.max(np.abs(frame)) < 0.01:
            f0s.append(0.0)
            continue

        # Autocorrelation
        corr = np.correlate(frame, frame, mode='full')
        corr = corr[len(corr) // 2:]

        # Search for peak in valid lag range
        if max_lag >= len(corr):
            max_lag_safe = len(corr) - 1
        else:
            max_lag_safe = max_lag

        if min_lag >= max_lag_safe:
            f0s.append(0.0)
            continue

        search = corr[min_lag:max_lag_safe + 1]
        if len(search) == 0 or np.max(search) < 0.3 * corr[0]:
            f0s.append(0.0)
            continue

        peak = np.argmax(search) + min_lag
        f0s.append(sr / peak)

    return np.array(f0s)


def spectral_centroid(audio, sr, n_fft=1024, hop=512):
    """Mean spectral centroid — brightness measure."""
    n_frames = 1 + (len(audio) - n_fft) // hop
    if n_frames < 1:
        return 0.0

    centroids = []
    freqs = np.fft.rfftfreq(n_fft, 1.0 / sr)
    for i in range(n_frames):
        frame = audio[i * hop:i * hop + n_fft] * np.hanning(n_fft)
        mag = np.abs(np.fft.rfft(frame))
        total = np.sum(mag)
        if total > 0:
            centroids.append(np.sum(freqs * mag) / total)

    return float(np.mean(centroids)) if centroids else 0.0


# ── Fingerprint: a small dict of stats ──────────────────────────

def fingerprint(audio, sr):
    """Extract a voice fingerprint: MFCC stats + pitch stats + brightness."""
    # Mono
    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    # Resample to 16kHz if needed (simple decimation for consistency)
    if sr != 16000:
        ratio = 16000 / sr
        new_len = int(len(audio) * ratio)
        audio = np.interp(np.linspace(0, len(audio) - 1, new_len),
                          np.arange(len(audio)), audio)
        sr = 16000

    mfccs = extract_mfccs(audio, sr)
    f0 = estimate_f0(audio, sr)
    voiced_f0 = f0[f0 > 0]

    fp = {
        "mfcc_mean": mfccs.mean(axis=0).tolist(),
        "mfcc_std": mfccs.std(axis=0).tolist(),
        "f0_mean": float(np.mean(voiced_f0)) if len(voiced_f0) > 0 else 0.0,
        "f0_std": float(np.std(voiced_f0)) if len(voiced_f0) > 0 else 0.0,
        "f0_median": float(np.median(voiced_f0)) if len(voiced_f0) > 0 else 0.0,
        "spectral_centroid": spectral_centroid(audio, sr),
        "rms": float(np.sqrt(np.mean(audio ** 2))),
        "duration": len(audio) / sr,
    }
    return fp


def fingerprint_file(path):
    """Extract fingerprint from a WAV file."""
    audio, sr = sf.read(str(path))
    return fingerprint(audio, sr)


# ── Comparison ──────────────────────────────────────────────────

def fp_vector(fp):
    """Convert fingerprint dict to a comparison vector.

    Weights pitch and brightness heavily — those are the features humans
    use to distinguish voices. MFCCs capture timbre but are too similar
    across all speech to discriminate well on cosine alone.
    """
    v = []
    # MFCCs (timbre) — 13 dims each, weight 1x
    v.extend(fp["mfcc_mean"])
    v.extend(fp["mfcc_std"])
    # Pitch — weight 5x (pitch is the strongest voice discriminator)
    pitch_weight = 5.0
    v.append(fp["f0_mean"] / 300 * pitch_weight)
    v.append(fp["f0_std"] / 100 * pitch_weight)
    v.append(fp["f0_median"] / 300 * pitch_weight)
    # Brightness — weight 3x
    v.append(fp["spectral_centroid"] / 4000 * 3.0)
    return np.array(v)


def compare(fp_a, fp_b):
    """Similarity between two fingerprints.

    Uses negative euclidean distance converted to a 0-1 similarity score.
    Euclidean penalizes large per-dimension gaps (like a 80Hz pitch difference)
    harder than cosine, which only cares about direction.
    """
    a = fp_vector(fp_a)
    b = fp_vector(fp_b)
    dist = np.linalg.norm(a - b)
    # Convert to similarity: 1.0 = identical, 0.0 = very far
    return float(1.0 / (1.0 + dist))


def identify(fp, db):
    """Find the best matching voice in the database. Returns (name, similarity) pairs sorted."""
    results = []
    for name, ref_fp in db.items():
        sim = compare(fp, ref_fp)
        results.append((name, sim))
    results.sort(key=lambda x: -x[1])
    return results


# ── Database ────────────────────────────────────────────────────

def build_db():
    """Build fingerprint database from all voice refs on the wall."""
    voice_dirs = [
        Path.home() / "w9" / "wall",
        Path.home() / "w9" / "wall" / "cast",
        Path.home() / "w9" / "wall" / "wells-bttf",
        BASE_DIR / "voices",
    ]

    db = {}
    for d in voice_dirs:
        if not d.exists():
            continue
        for wav in sorted(d.glob("*.wav")):
            if wav.name.startswith("._"):
                continue
            # Use relative-ish name for readability
            if "cast/" in str(wav):
                name = f"cast/{wav.stem}"
            elif "wells-bttf/" in str(wav):
                name = f"wells-bttf/{wav.stem}"
            else:
                name = wav.stem

            try:
                fp = fingerprint_file(wav)
                db[name] = fp
                print(f"  {name:40s}  f0={fp['f0_mean']:5.0f}Hz  "
                      f"bright={fp['spectral_centroid']:5.0f}Hz  "
                      f"dur={fp['duration']:.1f}s")
            except Exception as e:
                print(f"  {name}: FAILED ({e})")

    DB_PATH.write_text(json.dumps(db, indent=2) + "\n")
    print(f"\nDatabase: {len(db)} voices → {DB_PATH}")
    return db


def load_db():
    """Load the fingerprint database."""
    if not DB_PATH.exists():
        print("No voice database. Run: python3 voiceprint.py --build-db")
        sys.exit(1)
    return json.loads(DB_PATH.read_text())


# ── Episode check ───────────────────────────────────────────────

def check_episode(script_path, cold_open_path=None):
    """Check all generated lines against expected voices.

    Two checks per line:
    1. Pitch check: is f0 within 40% of the reference voice? Catches wrong-voice errors.
    2. Family check: is the top match in the same voice family? Catches subtler drift.

    Voice cloning doesn't produce exact copies — it produces voices in the same
    neighborhood. So we check family membership, not exact file match.
    """
    sys.path.insert(0, str(BASE_DIR))
    from generate_episode import parse_script, find_line_file, VOICE_MAP

    db = load_db()

    # Build reference fingerprints for each speaker's voice ref
    ref_fps = {}
    for speaker, ref_path in VOICE_MAP.items():
        # Find the ref in the DB by stem match
        stem = Path(ref_path).stem
        for name, fp in db.items():
            if stem in name:
                ref_fps[speaker] = fp
                break

    segments = []
    if cold_open_path and cold_open_path.exists():
        segments.extend(parse_script(cold_open_path))
        segments.append(("BREAK", ""))
    segments.extend(parse_script(script_path))

    episode_name = script_path.stem
    lines_dir = BASE_DIR / "output" / episode_name / "lines"

    seq = 0
    pitch_fails = []
    family_fails = []
    for speaker, text in segments:
        if speaker == "BREAK":
            continue
        seq += 10

        found = find_line_file(lines_dir, speaker, text, seq)
        if not found:
            print(f"  {seq:03d} [{speaker:5s}] MISSING")
            continue

        fp = fingerprint_file(found)
        results = identify(fp, db)
        top_name, top_sim = results[0]

        # Voice family: the directory the reference lives in
        expected_ref = VOICE_MAP.get(speaker, "?")
        ref_family = str(Path(expected_ref).parent)  # e.g. "wells-bttf", "cast", "."
        if ref_family == ".":
            ref_family = Path(expected_ref).stem  # e.g. "james_reference" → match "james"

        # Check 1: Pitch — is f0 within 40% of reference?
        ref_fp = ref_fps.get(speaker)
        pitch_status = "?"
        if ref_fp and ref_fp["f0_mean"] > 0 and fp["f0_mean"] > 0:
            ratio = fp["f0_mean"] / ref_fp["f0_mean"]
            if 0.6 <= ratio <= 1.4:
                pitch_status = "OK"
            else:
                pitch_status = f"PITCH({fp['f0_mean']:.0f}vs{ref_fp['f0_mean']:.0f})"
                pitch_fails.append((seq, speaker, fp["f0_mean"], ref_fp["f0_mean"]))
        elif fp["f0_mean"] == 0:
            pitch_status = "no-f0"  # Too short to estimate pitch

        # Check 2: Family — is top match in the same family?
        top_family = str(Path(top_name).parent) if "/" in top_name else top_name
        if ref_family in top_name or top_family == ref_family:
            family_status = "OK"
        elif any(ref_family in name for name, _ in results[:3]):
            family_status = "ok"  # In top 3 but not #1
        else:
            family_status = f"FAM({top_name})"
            family_fails.append((seq, speaker, top_name))

        preview = text[:40] + "..." if len(text) > 40 else text
        print(f"  {seq:03d} [{speaker:5s}] pitch={pitch_status:12s} "
              f"family={family_status:12s} "
              f"f0={fp['f0_mean']:5.0f}Hz  {preview}")

    print(f"\nResults: {seq // 10} lines checked")
    if pitch_fails:
        print(f"\n  PITCH FAILURES ({len(pitch_fails)}):")
        for s, spk, got, expected in pitch_fails:
            print(f"    {s:03d} [{spk}] got {got:.0f}Hz, expected ~{expected:.0f}Hz")
    else:
        print(f"  Pitch: all OK")

    if family_fails:
        print(f"\n  FAMILY MISMATCHES ({len(family_fails)}):")
        for s, spk, got in family_fails:
            print(f"    {s:03d} [{spk}] sounds like {got}")
    else:
        print(f"  Family: all OK")


# ── Scan: chunk a file and emit a voice trace ───────────────────

def scan_file(path, top_n=3, chunk_seconds=5.0):
    """Chunk a WAV into pieces, fingerprint each, and emit a character trace.

    Each chunk gets a letter representing the closest voice from the database.
    Silent chunks get '.'. The result is a readable string showing who's
    speaking when — like a genome sequence for the audio.
    """
    db = load_db()
    audio, sr = sf.read(str(path))
    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    chunk_samples = int(chunk_seconds * sr)
    n_chunks = max(1, len(audio) // chunk_samples)
    total_dur = len(audio) / sr

    # Assign a letter to each voice in the DB (by first appearance)
    voice_names = sorted(db.keys())
    voice_letter = {}
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    for i, name in enumerate(voice_names):
        voice_letter[name] = alphabet[i % len(alphabet)]

    print(f"Scanning {path.name}: {total_dur:.0f}s, {n_chunks} chunks @ {chunk_seconds}s\n")

    # Header: pitch scale
    print(f"  Pitch guide: Dorian ~133Hz | James ~200Hz | Aubrey ~209Hz | Leia ~373Hz\n")

    trace = []
    chunks_data = []

    for i in range(n_chunks):
        start = i * chunk_samples
        end = min(start + chunk_samples, len(audio))
        chunk = audio[start:end]

        # Skip silence
        rms = float(np.sqrt(np.mean(chunk ** 2)))
        if rms < 0.005:
            trace.append(".")
            chunks_data.append(None)
            continue

        fp = fingerprint(chunk, sr)
        results = identify(fp, db)
        best_name, best_sim = results[0]
        letter = voice_letter[best_name]
        trace.append(letter)
        chunks_data.append({
            "time": f"{start/sr:.0f}-{end/sr:.0f}s",
            "f0": fp["f0_mean"],
            "bright": fp["spectral_centroid"],
            "best": best_name,
            "sim": best_sim,
        })

    # Print the trace
    trace_str = "".join(trace)

    # Print in rows of 60 with time markers
    print("  Voice trace (each char = one chunk):\n")
    for row_start in range(0, len(trace_str), 60):
        row = trace_str[row_start:row_start + 60]
        time_start = row_start * chunk_seconds
        time_end = min((row_start + 60) * chunk_seconds, total_dur)
        print(f"  {time_start:6.0f}s |{row}| {time_end:.0f}s")

    # Legend: which letters appeared and what they mean
    used_letters = set(trace) - {"."}
    letter_to_name = {v: k for k, v in voice_letter.items()}
    print(f"\n  Legend:")
    for letter in sorted(used_letters):
        name = letter_to_name.get(letter, "?")
        # Find the ref f0 from the DB
        ref_fp = db.get(name, {})
        ref_f0 = ref_fp.get("f0_mean", 0)
        print(f"    {letter} = {name} (ref f0={ref_f0:.0f}Hz)")
    print(f"    . = silence")

    # Print pitch trace — f0 values mapped to 0-9
    f0_values = []
    for cd in chunks_data:
        if cd is None:
            f0_values.append(None)
        else:
            f0_values.append(cd["f0"])

    # Map f0 to digits: 0=60Hz, 9=400Hz (log scale)
    def f0_to_digit(f0):
        if f0 <= 0:
            return "."
        import math
        low, high = math.log(60), math.log(400)
        val = (math.log(f0) - low) / (high - low)
        digit = int(val * 9.5)
        return str(max(0, min(9, digit)))

    pitch_trace = "".join(
        "." if v is None else f0_to_digit(v) for v in f0_values
    )

    print(f"\n  Pitch trace (0=60Hz ... 9=400Hz):\n")
    for row_start in range(0, len(pitch_trace), 60):
        row = pitch_trace[row_start:row_start + 60]
        time_start = row_start * chunk_seconds
        print(f"  {time_start:6.0f}s |{row}|")
    print(f"\n    0-3 = deep (Dorian/Ben territory)")
    print(f"    4-6 = mid (James/Aubrey territory)")
    print(f"    7-9 = high (Leia/Hype territory)")




def main():
    parser = argparse.ArgumentParser(description="Voice fingerprinting")
    parser.add_argument("command", nargs="?",
                        choices=["identify", "compare", "check", "scan"],
                        help="Command to run")
    parser.add_argument("files", nargs="*", help="WAV files")
    parser.add_argument("--build-db", action="store_true",
                        help="Build fingerprint database from voice refs")
    parser.add_argument("--cold-open", type=Path, default=None)
    parser.add_argument("--top", type=int, default=5,
                        help="Number of top matches to show")
    args = parser.parse_args()

    if args.build_db:
        build_db()
        return

    if args.command == "identify":
        if not args.files:
            sys.exit("Usage: voiceprint.py identify <file.wav>")
        db = load_db()
        for f in args.files:
            fp = fingerprint_file(Path(f))
            results = identify(fp, db)
            print(f"\n{Path(f).name}:")
            print(f"  f0={fp['f0_mean']:.0f}Hz  bright={fp['spectral_centroid']:.0f}Hz")
            for name, sim in results[:args.top]:
                print(f"  {sim:.3f}  {name}")

    elif args.command == "compare":
        if len(args.files) != 2:
            sys.exit("Usage: voiceprint.py compare <a.wav> <b.wav>")
        fp_a = fingerprint_file(Path(args.files[0]))
        fp_b = fingerprint_file(Path(args.files[1]))
        sim = compare(fp_a, fp_b)
        print(f"Similarity: {sim:.3f}")
        print(f"  A: f0={fp_a['f0_mean']:.0f}Hz  bright={fp_a['spectral_centroid']:.0f}Hz")
        print(f"  B: f0={fp_b['f0_mean']:.0f}Hz  bright={fp_b['spectral_centroid']:.0f}Hz")

    elif args.command == "check":
        if not args.files:
            sys.exit("Usage: voiceprint.py check <script.md> [--cold-open cold-open.md]")
        script = Path(args.files[0])
        if not script.is_absolute():
            script = BASE_DIR / script
        cold_open = args.cold_open
        if cold_open and not cold_open.is_absolute():
            cold_open = BASE_DIR / cold_open
        check_episode(script, cold_open)

    elif args.command == "scan":
        if not args.files:
            sys.exit("Usage: voiceprint.py scan <file.wav>")
        scan_file(Path(args.files[0]), args.top)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
