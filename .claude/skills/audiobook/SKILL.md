# Audiobook

Build and generate custom audiobooks using Qwen3-TTS voice cloning. Also known as: podcast, audio, TTS, voice, narration.

## When To Use

- Writing or editing an audiobook script
- Mapping voices to roles
- Generating audio from a script
- Casting new voices (requires GPU)
- Assembling, mixing, or applying effects
- Reviewing or testing a script before generation
- Verifying voice identity after generation

## Architecture

Two generators:

1. **`audiobook/generate.py`** — Episode 1 (Shapes for Rich). Original single-episode generator. Narrator + Shape voices.
2. **`audiobook/generate_episode.py`** — Multi-episode generator. Handles any script with `[SPEAKER]` tags. Shared `VOICE_MAP` across all episodes. This is the active one.

### Sequenced Content-Addressed Line Cache

Line WAVs use **sequenced content-addressed filenames**: `{seq:03d}_{speaker}_{sha256(text)[:12]}.wav`. Sequence numbers count by 10s (Apple II style) for easy insertion. The hash is authoritative for cache; the sequence is for human readability.

```
010_james_fd0c49bd3b50.wav    ← cold open
020_james_372d5582ad1b.wav    ← intro
030_stage_df04e6c292e2.wav    ← first stage direction
...
590_vic_b0240f5c9f4c.wav      ← "I stay hydrated"
600_stage_0eb6656ff443.wav    ← disclaimer
610_james_49c92fed4f29.wav    ← outro
```

- Inserting a line between 020 and 030? It becomes `025_vic_{hash}.wav`. No renumbering.
- Run `--renumber` to re-space everything back to 10s when gaps get ugly.
- `find_line_file()` looks up by hash, tolerates sequence changes, renames on match.

### Assembly-Time Effects (Sound Board)

All effects run in numpy during `_assemble()`. No regeneration needed to change the mix.

**Volume hierarchy:**
- `VOLUME_SCALE` — per-speaker: `STAGE: 0.7`, `SAM: 0.85`
- `EMPHASIS_BOOST` — lines with `!` get 1.3x lift (excludes STAGE, JAMES)

**Effects chain (per line):**
1. RMS normalization (target 0.045, peak limit 0.95)
2. Per-speaker volume scaling
3. Emphasis boost for `!` lines
4. Telephone bandpass filter for `TELEPHONE_SPEAKERS` (FFT brick-wall, 300-3400 Hz)
5. Horror filter for specific lines (growl + overdrive + pitch drop, time-crossfaded)
6. Reverb (decaying delay taps: decay=0.3, delay=40ms, 6 taps)
7. Stereo pan (`VIC: -0.30 left`, `SAM: 0.30 right`, others center)
8. Room tone (pink noise in pauses, level 0.003)
9. Fade in (50ms anti-click) / Fade out (2.0s)

**Horror filter (special — "No! You track it!" line):**
- 0-0.8s: Full blast — telephone + drive=5 overdrive + 8% pitch drop + tight reverb
- 0.8-1.3s: Crossfade blast to medium grit
- 1.3-4.1s: Grit fading to dry (clean by the word "exists")
- 4.1s+: Fully dry
- Triggered by `'You track it' in text`

**To add new effects:** Add a filter function, apply it in the `_assemble()` loop based on speaker tag or text content. Future: `[SPEAKER!EFFECT]` syntax in scripts.

## Phase 1: Script

### Pre-production verification

Run this checklist before generating audio. Every step runs; none are optional. If a step fails, fix it before proceeding to generation. Once audio is generated, dialogue fixes cost GPU hours.

**Parse integrity** — verify the script parses cleanly:
- All speaker tags match `[UPPERCASE-NAME]` and are known in `VOICE_MAP`
- No orphaned text (lines outside any speaker tag)
- No empty voice lines (speaker tag with no text before next tag or break)
- No double section breaks (`---` followed immediately by `---`)
- Section breaks have voiced content on both sides

**Line lengths** — TTS quality degrades on long runs:
- Hard limit: 120 words per line. Fail the check if exceeded.
- Warn at 60 words. Lines over 60 words should be reviewed — consider splitting at a natural breath point.
- Character voices (VIC-EXPLORER, VIC-COMPLIANCE, VIC-STEWARD, HYPE, etc.) should be shorter — under 40 words. These voices can't sustain long passages.

**Speaker balance** — verify the episode's dynamics:
- Count lines and words per speaker
- The lead voice should carry the majority
- Supporting voices should have enough lines to establish character but not dominate
- Warn if any speaker has only 1 line (except HYPE or cold-open JAMES, which are cameos)

**Voice map coverage** — every speaker in the script must have a mapping in `VOICE_MAP` in `generate_episode.py`. Report any unmapped speakers as a hard stop.

**Word count and duration estimate** — sanity-check episode length:
- Dialogue episodes: estimate at ~150 wpm (faster than narration)
- Narration episodes: estimate at ~130 wpm
- Add section breaks × 2s for pause time
- Flag if under 5 minutes (too short) or over 20 minutes (long for a podcast episode)

**PII scan** — scan the script markdown for:
- Email addresses, phone numbers, real full names that shouldn't be in the audio
- Internal hostnames, IPs, file paths with real usernames
- API keys, tokens, secrets (even in dialogue — they'll be spoken aloud)
- Known acceptable: the words "secrets," "email," "PII" used in dialogue *about* privacy are fine

**Fact-check against source material** — for scripts that reference book chapters:
- Verify specific numbers (chapter counts, test scores, percentages) against the actual chapters in `chapters/`
- Verify named people, anecdotes, and quotes appear in the cited chapter
- Verify structural claims (part names, chapter titles) against the directory structure
- Flag claims that appear only in the script and not in any chapter — these may be audiobook-original (fine) or hallucinated (not fine)

**Editorial review** — read for production readiness:
- **Voice consistency**: Does each character sound like themselves across lines? Compare against previous episodes if this is a returning cast.
- **Tone**: Flag lines that break character into marketing copy, feature explanations, or voiceover mode. Dialogue should sound like people talking, not a pitch deck.
- **Character voice splits**: Verify that lines tagged with a character voice (e.g., VIC-STEWARD) contain *only* that character's dialogue. If the speaker breaks character mid-line, it needs to be split into two segments with separate tags.
- **Stage directions**: Should add texture or comedy, not just describe blocking. Compare against the episode's tone.

**Sample generation** — write a `{episode}-sample.md` with one line per voice. All speakers, representative lines. Generate this first (cheap) to verify all voices resolve and sound right before the full run.

### Script format

Scripts live in `audiobook/` as markdown files. Format:

```markdown
## Script

[NARRATOR]
Spoken text here.

[VOICE-NAME]
More spoken text.

---
```

Rules:
- Speaker tags are `[UPPERCASE-NAME]` on their own line
- `---` marks section breaks (rendered as pauses)
- Everything before `## Script` is metadata (voice design notes, etc.)
- Lines starting with `>` are directives (skipped by parser)
- Lines starting with `#` are headers (skipped by parser)

### Cold opens

Reusable disclaimers prepended to episodes via `--cold-open`:

```bash
python3 generate_episode.py vic-and-sam.md --cold-open cold-open.md
```

The cold open is parsed and prepended as segments before the main script, with a BREAK between them.

### Current scripts

| File | Episode | Voices | Status |
|---|---|---|---|
| `rich.md` | Ep 1: Shapes for Rich | NARRATOR, SHAPE, SHAPE-CLOSE, SHAPE-WARN | Generated (Dorian recast complete) |
| `vic-and-sam.md` | Ep 3: Vic and Sam | VIC, SAM, STAGE, JAMES, HYPE | Generated, full stereo mix |
| `wall-of-data.md` | Ep 2: The Lightweight Wall | 11 voices | Script written, not generated |
| `vic-and-sam-2.md` | Ep 4: The File That Knows You | VIC, VIC-EXPLORER, VIC-COMPLIANCE, VIC-STEWARD, SAM, SAM-HYPE, STAGE, JAMES, HYPE | Generated, full stereo mix, webpage published |
| `cold-open.md` | Reusable disclaimer | JAMES | Generated |

## Phase 2: Voices

### Voice Map

All voices live in `VOICE_MAP` in `generate_episode.py`:

```python
VOICE_MAP = {
    "NARRATOR":    "dorian-moreau.wav",
    "SHAPE":       "cast/old_ben_kenobi_conversation.wav",
    "VIC":         "wells-bttf/dorian-moreau.wav",
    "SAM":         "cast/old_ben_kenobi_conversation.wav",
    "STAGE":       "smithers_clone.wav",
    "HYPE":        "cast/lady_leia_commanding.wav",
    "JAMES":       "james_reference.wav",
    # ... more in the file
}
```

Voice resolution searches multiple paths:
1. `~/voices/` (DGX)
2. `~/w9/wall/` (local wall)
3. `audiobook/voices/` (project)
4. `audiobook/voices/harvest/` (harvested refs)
5. Flat filename variants of all the above

### Voice prompt caching (keyed by voice ref hash)

Prompt cache filenames include a hash of the voice reference WAV: `{speaker}_{refhash}.pt`. If the reference file changes (different voice, updated recording), the cache auto-invalidates. Stale caches from old refs are deleted automatically. No more silent wrong-voice generation.

### Three gates before committing to a full run

A voice recast failed **twice** — 143 lines generated with the wrong voice, 45 minutes of DGX time wasted each time. The system declared success both times. The fix is three verification gates that catch the problem before it costs you the full run.

**Gate 1: Input manifest** (before any generation)
- Writes `voice-manifest.json` with status `STARTED` listing every speaker's voice ref path, file hash, VOICE_MAP entry, and prompt cache status (HIT/FRESH/LOAD_FAILED).
- Cross-similarity matrix flags accidental voice duplicates (sim > 0.90 warns).
- Every fallback logs when it fires — resolve_voice path #3, file renamed, cache load failure.
- **Review the manifest before generation proceeds.** If the refs are wrong, stop here.

**Gate 2: Smoke test** (after first generated line per speaker)
- Extracts x-vector from the generated audio.
- Computes cosine similarity to the reference x-vector.
- If similarity < 0.70: **hard stop**. No fallback, no continuation.
- Cost: 1 line per speaker. Catches wrong prompt cache, wrong voice ref, wrong VOICE_MAP entry.

**Gate 3: Batch voiceprint** (after 5 generated lines)
- Runs `voiceprint.py` pitch and family check on the first batch.
- Compares f0 of each generated line to the reference voice. If pitch is off by > 40%: **hard stop**.
- Requires `voice-db.json` on the machine (run `python3 voiceprint.py --build-db` once).
- Cost: 5 lines. Catches subtler drift that the x-vector smoke test might miss.

**Only after all 3 gates pass does the full run proceed.**

```bash
# Safe workflow for a recast or new episode:
python3 voiceprint.py --build-db                    # Once: build voice fingerprint DB
python3 generate_episode.py script.md --batch 5     # Generate 5 lines, hits all 3 gates
# Review output, listen to the 5 lines
python3 voiceprint.py identify output/ep/lines/*.wav  # Spot-check voice identity
python3 generate_episode.py script.md               # Full run (gates already passed)
```

### Critical lesson: Trace fallbacks tip to tail

Every fallback, every default, every cached value is a place where a disconnection can hide. The system should crash on a mismatch, not produce 143 lines with the wrong voice and declare success. All fallbacks now log when they fire. The input manifest is written before generation, not after — it's a pre-flight checklist, not an autopsy report.

**Known API drift:** The `qwen_tts` library renamed `x_vector` to `ref_spk_embedding` between versions. The `get_xvector()` helper in `generate_episode.py` tries both field names and crashes with a clear message if neither exists. If the DGX qwen_tts version changes again, this is the first thing to check.

## Phase 3: Generate

### Multi-episode generator

```bash
python3 generate_episode.py vic-and-sam.md                    # Generate all
python3 generate_episode.py vic-and-sam.md --batch 20         # Generate 20 lines
python3 generate_episode.py vic-and-sam.md --cold-open cold-open.md  # With disclaimer
python3 generate_episode.py vic-and-sam.md --assemble-only    # Just remix
python3 generate_episode.py vic-and-sam.md --renumber          # Re-space to 10s
```

Assembly-only requires only `numpy` and `soundfile` (no torch). Generation requires torch + qwen_tts.

### Draft mode (local TTS)

Render full episodes locally using macOS `say` and `espeak-ng` instead of Qwen3-TTS on the DGX. No GPU required — entire episodes render in ~1-2 minutes.

```bash
python3 generate_episode.py script.md --draft
```

**How it works:**
- `DRAFT_VOICE_MAP` in `generate_episode.py` maps each speaker to a `(voice_spec, engine)` tuple, where engine is `"say"` (macOS TTS) or `"espeak"` (espeak-ng)
- Output goes to `output/{episode}-draft/`, separate from real renders
- Uses the same content-addressed line cache as production — re-runs skip cached lines
- Same assembly pipeline with all effects (reverb, pan, telephone filter, horror filter, etc.)

**Voice casting philosophy:**
- 6 macOS natural voices (Daniel, Karen, Moira, Rishi, Samantha, Tessa) cover the main cast
- espeak-ng robot voices (Fred, etc.) cover error voices, roll call, and one-off characters
- Draft voices are the preferred production voices — they render in 2 minutes vs 45 minutes for cloned voices. Faster iteration means more corrections means better output. The "worse" voice produces better episodes because you can afford to re-render ten times.
- The best voice is the one that lets you iterate.

**Dry mix mode:**
- `--dry` flag skips all effects: no reverb, no telephone filter, no stereo pan, no room tone, no emphasis boost
- Just normalized voices, silence between lines, fade in/out
- Use for scripts where the voices carry the show without effects (workbook-style episodes, dramatizations)

**TTS pronunciation guide:**
- Use sip test pronunciation pages to audition spellings (see `output/pronunciation/`)
- Known winners from testing: Co-Work (hyphenated), f-f-mpeg (dashes), A.E.S. (dots), H.T.M.L. (dots), T-T-S (dashes), C.L.I. (dots)
- MP3 and MP4 are fine as-is — Daniel says them correctly in context
- URL is fine as-is
- Netlify, Homebrew, Xcode, Ollama, ChatGPT all pronounce correctly without modification
- Build a pronunciation audition page when unsure — generate multiple spellings, listen, pick
- Future: add "copy state" button to pronunciation pages that puts picks in clipboard

**Multi-voice dramatization format:**
- For workbook/dramatization episodes, use character voices in first person (RICH, OCTOPUS, PARROT, CRAB, ERROR)
- STAGE as connective tissue — transitions between chapters, reflective commentary, knows how the story ends
- Headlines can be folded into STAGE: "Now let's talk about security. Making it secure." instead of a separate HEADLINE voice
- Each character should introduce themselves with their macOS voice name at the top
- The ERROR voice (Fred) introduces itself with a sample error and another character reacts

**Current workbook cast (I Want a Podcast):**

| Speaker | macOS Voice | Role |
|---|---|---|
| JAMES | Daniel | Author |
| RICH | Rishi | The user |
| OCTOPUS | Tessa | Claude Code CLI |
| PARROT | Karen | ChatGPT free web (near-sighted) |
| CRAB | Moira | Claude Co-Work / sandboxed (in a shell) |
| STAGE | Samantha | Transitions, reflections, omniscient |
| ERROR | Fred | Error messages, robot |

**Hybrid real/draft rendering:**
- `DRAFT_USE_REAL` lists speakers whose real Qwen3-TTS renders already exist. Those lines get copied from the real output dir instead of re-rendering with draft voices (currently: CHARLOTTE).

**Render speed:**
- espeak-ng: 0.003-0.007x realtime
- macOS say: 0.012-0.068x realtime

**Purpose:** iterate on scripts locally without DGX access. Hear the full mix, timing, and effects with placeholder voices before committing GPU time.

### Local venv

`audiobook/.venv` has numpy, soundfile, and scipy for local assembly and voice analysis. Torch is only on DGX.

## Phase 4: Verify

### Dead air check

TTS sometimes generates silence gaps or spurious pops/clicks after the voice stops. These compound in the mix — a 3s dead tail on one line plus a 2s section break = 5s of nothing. Check both individual lines and the assembled mix.

**Per-line check (run on all generated WAVs):**

```bash
cd audiobook && .venv/bin/python3 -c "
import soundfile as sf
import numpy as np
import os, sys

lines_dir = sys.argv[1]
for f in sorted(os.listdir(lines_dir)):
    if not f.endswith('.wav'): continue
    audio, sr = sf.read(os.path.join(lines_dir, f))
    total = len(audio) / sr
    # Windowed RMS scan (0.25s windows)
    window = int(0.25 * sr)
    last_signal = 0
    for start in range(0, len(audio) - window + 1, window):
        rms = np.sqrt(np.mean(audio[start:start+window]**2))
        if rms >= 0.005:
            last_signal = (start + window) / sr
    dead = total - last_signal
    if dead > 0.5:
        print(f'DEAD AIR: {f} — {dead:.1f}s silence at end (total {total:.1f}s, voice ends ~{last_signal:.1f}s)')
" output/EPISODE/lines/
```

**Assembled mix check (find silence gaps > 1s):**

```bash
cd audiobook && .venv/bin/python3 -c "
import soundfile as sf
import numpy as np
import sys

audio, sr = sf.read(sys.argv[1])
mono = audio.mean(axis=1) if audio.ndim > 1 else audio
window = int(0.5 * sr)
in_silence = False
silence_start = 0
for start in range(0, len(mono) - window + 1, window):
    rms = np.sqrt(np.mean(mono[start:start+window]**2))
    if rms < 0.003:
        if not in_silence:
            silence_start = start / sr
            in_silence = True
    else:
        if in_silence:
            dur = start / sr - silence_start
            if dur > 1.5:
                print(f'GAP: {silence_start:.1f}s - {start/sr:.1f}s ({dur:.1f}s)')
            in_silence = False
if in_silence:
    dur = len(mono)/sr - silence_start
    if dur > 1.5:
        print(f'GAP: {silence_start:.1f}s - {len(mono)/sr:.1f}s ({dur:.1f}s)')
" output/EPISODE/EPISODE.wav
```

Expected section breaks are 2.0s — anything over 3s is suspect. Dead air in lines is handled automatically by `trim_trailing_silence()` in the assembly, but always verify.

**Root cause:** TTS models sometimes generate silence gaps or pops after the voice content ends. The `trim_trailing_silence()` function in `generate_episode.py` detects the longest silence gap in the back half of each line and trims there. It uses windowed RMS (not per-sample peaks) to ignore isolated clicks.

### Whisper transcription check

Whisper with word timestamps is the clearest way to find dead air — it maps silence gaps to transcript gaps. A line where the last word ends at 9.5s but the WAV runs to 12.8s is immediately visible.

```bash
whisper output/EPISODE/lines/040_vic_*.wav --model tiny --language en --output_format json --word_timestamps True
```

Look for: large gaps between the last word's `end` timestamp and the file duration. Also catches garbled or missing words.

For the assembled mix:

```bash
whisper output/EPISODE/EPISODE.wav --model tiny --language en --output_format json --word_timestamps True
```

Short lines ("Correct.", "A shape.", "Did you —") may show as PARTIAL/MISSING due to matching threshold — verify by listening. The telephone filter on stage directions makes whisper transcription rougher but the content is present.

### Voice fingerprinting (`voiceprint.py`)

Acoustic voice identification without torch. Uses MFCCs + pitch (f0) + spectral centroid extracted with numpy/scipy. No model loading, runs locally in seconds.

```bash
# Build fingerprint database from all voice refs on the wall
python3 voiceprint.py --build-db

# Identify which voice a WAV sounds like
python3 voiceprint.py identify output/vic-and-sam/lines/050_vic_f6c1472e9afb.wav

# Compare two files
python3 voiceprint.py compare fileA.wav fileB.wav

# Check all lines in an episode against expected voices
python3 voiceprint.py check vic-and-sam.md --cold-open cold-open.md
```

**How it works:**

1. **Fingerprint** = MFCCs (timbre) + f0 mean/std/median (pitch) + spectral centroid (brightness)
2. **Database** (`voice-db.json`) = fingerprints of all ~32 voice refs from `~/w9/wall/`
3. **Identification** = weighted euclidean distance. Pitch weighted 5x, brightness 3x.
4. **Episode check** runs two tests per line:
   - **Pitch check**: Is f0 within 40% of the reference? Catches wrong-voice errors. Aubrey (209Hz) vs Dorian (133Hz) would fail immediately.
   - **Family check**: Is the top match in the same voice family (same directory)? Voice cloning doesn't produce exact copies — it produces voices in the same neighborhood. So we check family, not exact file.

**Known limitations:**
- Short lines (< 2s) produce unreliable pitch estimates. "A shape." or "That's —" may show false pitch failures.
- Telephone-filtered lines (STAGE) have no pitch reference in the DB since smithers_clone isn't on the wall. STAGE always shows `pitch=?` and family mismatch — this is expected.
- Voice cloning output matches the voice *family* (e.g. wells-bttf) more than the exact reference file. This is expected — the model produces a voice in the same neighborhood, not a copy.
- JAMES family matches vary (james_test_intro, james_meet_c, wells-bttf/arthur) because all James refs are the same person. These are not failures.
- Cross-similarity warnings fire heavily when an episode has 9+ voices from a small cast pool (e.g. Vic and Sam 2 fires 30+ warnings). These are all intentional — the cast voices are related by design. Review the manifest but don't block on similarity warnings for known casts.

**Key acoustic stats for the current cast:**

| Voice | f0 (Hz) | Brightness (Hz) | Family |
|---|---|---|---|
| Dorian Moreau (VIC) | 133 | 1320 | wells-bttf |
| Old Ben Kenobi (SAM) | 93 | 1292 | cast |
| Lady Leia (HYPE) | 373 | 2758 | cast |
| James | 202 | 1381 | james |
| Aubrey (old narrator) | 209 | 1735 | standalone |

## Infrastructure

### DGX (all generation and casting)

```bash
~/bin/dgx
# or: ssh nop@dgx.mahi-tilapia.ts.net
```

- User: `nop`
- NVIDIA GB10 GPU (CUDA capability 12.1, PyTorch warns but works)
- Python venv: `~/tts_env`
- Voice refs: `~/audiobook/voices/`, `~/voices/`
- SoX not installed (warning appears, doesn't block generation)
- Aaron's llama server uses ~71 GB VRAM — check with `nvidia-smi` before loading models

**Remote generation workflow:**

```bash
# Sync script changes
rsync -avz audiobook/ nop@dgx.mahi-tilapia.ts.net:~/audiobook/

# Generate (background)
ssh nop@dgx.mahi-tilapia.ts.net 'source ~/tts_env/bin/activate && cd ~/audiobook && nohup python3 generate_episode.py script.md > output/gen.log 2>&1 & echo $!'

# Monitor
ssh nop@dgx.mahi-tilapia.ts.net 'tail -f ~/audiobook/output/gen.log'

# Pull results
rsync -avz nop@dgx.mahi-tilapia.ts.net:~/audiobook/output/ audiobook/output/
```

### MacBook (assembly, listening, script editing, voice analysis)

- 16 GB RAM, Apple Silicon MPS
- `audiobook/.venv` — numpy + soundfile + scipy for assembly and voiceprint analysis
- Assembly-only works locally (torch import is lazy/optional)
- Player page: `audiobook/output/player-v2.html` (open in Chrome)

## Player Page

`audiobook/output/player-v2.html` — dark theme, episodes at top, test slices in collapsible Sound Lab sections.

## Phase 5: Publish

### Web page

Each episode gets a standalone HTML page in `reference/_meta/static/`. The page uses the same CSS as the first Vic and Sam episode (`vic-and-sam.css`) and follows the graphic-novel-script format:

- **Orientation block** at top (teal-bordered, fast summary for humans and bots, book links)
- **Audio player** with MP3 (convert from WAV: `ffmpeg -i episode.wav -codec:a libmp3lame -b:a 192k episode.mp3`)
- **Script as dialogue** using `.line.vic`, `.line.sam`, `.stage` CSS classes
- **Page breaks** between sections (`<div class="page-break">Page N</div>`)
- **Book cross-links** inline where the dialogue references chapters
- **Episode navigation** at top and bottom linking to adjacent episodes
- **Disclaimer** in the style of the episode (ep 1: comedians, ep 2: octopuses)

For character voices (Vic doing impressions, Sam attempting enthusiasm), use inline `<style>` for episode-specific CSS classes rather than modifying the shared stylesheet.

**Cross-linking checklist:**
- Add forward link from previous episode to new one
- Add backward link from new episode to previous one
- Link chapter references in dialogue to `book/chapter-slug`
- Update the orientation block's "Best next pages" to point to relevant chapters

### Public episodes

- WAV → MP3 at 192k for the site
- **MP3s and HTML pages go in `reference/_meta/static/`, NOT `reference/site/`**. The build script wipes `reference/site/` and rebuilds from `_meta/static/` + markdown sources. Anything placed directly in `reference/site/` will be deleted on the next build.
- Public pages go directly in `reference/site/` (e.g. `i-want-a-podcast.html`)
- Add to site index (`reference/site/index.html`) with a card in the appropriate section
- Deploy: `rsync -avz --delete --exclude='rich/' --exclude='alex/' reference/site/ shapes.exe.xyz:/var/www/html/`
- **IMPORTANT**: `--delete` will wipe private portal dirs unless excluded

### Private portals (mentoring episodes)

- Private episodes deploy to their own path: `/rich/`, `/alex/`, etc.
- Each portal is in `audiobook/output/{name}-portal/` with its own `index.html`, MP3s, and viewer pages
- Protected by nginx basic auth (htpasswd file in the portal dir)
- Deploy separately: `rsync -avz audiobook/output/rich-portal/ shapes.exe.xyz:/var/www/html/rich/`
- Rich portal: username `rich`, password `supernatural`
- Portal landing page: LCARS-themed, reverse chronological, download buttons, transcript links, sidebar with public episode links
- Always add new private paths to the public deploy `--exclude` list and to the MEMORY.md deploy notes

### Viewer pages

- Two styles: LCARS-themed (private portals) or site-themed (public)
- Audio player at top, full transcript below
- Color-coded by speaker with CSS classes matching the cast
- Include download button for the MP3
- Private viewers: no password gate (nginx handles auth for the whole path)

## Voice Casting Wall

All unique voices at `~/w9/wall/`. Browse: `open ~/w9/wall/voice-casting-wall.html`

Key directories:
- `~/w9/wall/` — harvest refs
- `~/w9/wall/cast/` — 15 SW-medieval cast clips
- `~/w9/wall/wells-bttf/` — 7 Wells-BTTF cast clips

## Audio Analysis Tools

### Voice Fingerprinting (`voiceprint.py`)

See the [Voice fingerprinting section](#voice-fingerprinting-voiceprintpy) above for full usage and acoustic stats. The voice fingerprint database and scatter visualization are also rendered on the wall of voices page at `reference/_meta/static/wall-of-voices.html`.

### Adding a New Voice to the Wall

- Obtain a reference clip: 10-30 seconds of clean speech, mono, 16-48kHz WAV
- Place the WAV in the appropriate wall directory:
  - `~/w9/wall/cast/` for character voices (named `{character}_{register}.wav`)
  - `~/w9/wall/wells-bttf/` for Wells-BTTF session voices
  - `~/w9/wall/` for standalone/harvest voices
- Run `python3 voiceprint.py --build-db` to add to the fingerprint database (`voice-db.json`)
- Add the speaker tag and WAV path to `VOICE_MAP` in `generate_episode.py`
- Add to `VOLUME_SCALE` in `generate_episode.py` if non-default volume needed
- Generate a test line: `python3 generate_episode.py sample.md --batch 1`
- Verify with `python3 voiceprint.py identify output/sample/lines/*.wav`
- Update the wall of voices page at `reference/_meta/static/wall-of-voices.html`

### Wall of Voices Page

The complete voice catalog lives at `reference/_meta/static/wall-of-voices.html`. It includes:
- Scatter chart of all voices (pitch vs brightness, color-coded by family)
- Voice cards with acoustic stats (f0, spectral centroid, RMS, duration)
- Role mappings (which podcast character uses which voice)
- Duplicate detection results
- New voice entry process documentation

### Current Voice Inventory (33 voices)

**Families:**
- **Star Wars medieval** (`cast/`): 15 registers across 4 characters — Old Ben Kenobi, Lady Leia, Ser Vaydar, Hann of Soloh, Luc Skywalden, Charlotte
- **Wells-BTTF** (`wells-bttf/`): 7 voices — Dorian Moreau, Arthur, Dean Griffin, Eliza, Narrator, The Traveller, Young Herbert
- **James**: 5 variants — reference (90s composite), 3 Meet segments, test intro
- **Standalone**: Aubrey, harvest clips, meet sample

**Known duplicates:**
- `ser_vaydar_whisper_harvest` == `cast/ser_vaydar_whisper` (identical file)
- `aubrey` exists in both `~/w9/wall/` and `audiobook/voices/` (synced copy, not a problem)
