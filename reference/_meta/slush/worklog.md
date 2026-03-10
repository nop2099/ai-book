# Worklog

## Mar 7-8 — Repo hygiene
- Consolidated repos, added .gitignore for data/convo/repos
- PII audit on manuscript
- Crash Course Philosophy transcript research (AI personhood material)

## Mar 9 — Reference site + tooling (big session)

**~10am–2pm: Creative writing**
- Vic Michaelis improv screenplay with "wall of data" concept
- Opened in Chrome for review

**~2:50pm: Reference site started**
- Discussed hosting (Vercel, Cloudflare, DreamHost)
- Decided: static site, modular/a-la-carte reference pages
- Built scaffold: entry page with 9 project shapes, workspace/SSH/GitHub pages
- "Reimplement, don't import" principle from Theo

**~2:55pm: Memory Viewer (shelved)**
- Foveated retrieval from Postgres on octopus.mahi-tilapia.ts.net
- "Fibers of attention" — async context enrichment during conversation
- Put on hold: "until it becomes very useful in building the site"

**~4pm: Board game reference page**
- Built full staged guide (rules → architecture → UX → validation → deployment)
- Replaced [game name] with ShapeGame
- Network visibility as core multiplayer principle
- Tone sweep: will→may, most→some
- "See the same thing" (shared representations for human+AI verification)
- "Break it before you fix it" (reproduce-before-fix)
- Killed the word "metamer" — "no one knows the word metamer"

**~5:30pm: Cribbage + Bridge built (separate sessions)**
- ~/w9/boardgame (cribbage): created 5:33pm, done ~8:11pm
  - 2.5 hrs wall clock, ~1 hr AI work, ~15 min human attention
  - Full game: peg board, scoring, AI, training mode with EV analysis
  - TypeScript, Vite, Vitest, no framework
  - Corrections: go bug, board dots wrong, missing last-card rule, overlapping animations
- ~/w9/bridge: created 5:36pm, last touch 8:29pm
  - Python/FastAPI + vanilla JS frontend
  - Chicago scoring, bidding conventions (Stayman, Blackwood, Jacoby)
  - AI opponents + bidding advisor

**~6pm: Readability tooling**
- Built check-readability.py (textstat): grade level, jargon, long sentences, rhythm
- Built analyze-chapters.py: cross-chapter metrics → JSON
- Built chapter-dashboard.html: observatory-aesthetic arc visualization
- Fixed contrast: "dark is fine, but must be legible"
- Avg grade across book: 6.9. Study guide outlier at 8.8.

**~6:30pm: Book on website**
- Built build-book.py: 48 chapters → HTML with prev/next nav
- Source Serif 4 body text, dark theme, amber accents
- Added book + dashboard links to site index

**~7pm: Spiral curriculum + flywheel**
- Designed Wonder → Try → Break → Know cycle
- Builder track (learn to code) vs Director track (learn to direct)
- The 15-minute ratio: domain expertise > programming skill
- Two games in one afternoon = flywheel proof
- Wrote slush/the-flywheel.md

## Open threads

**Ready to run:**
- [ ] Integrate build-book.py into build.sh
- [ ] Verify book pages in browser (generated but not reviewed)

**Reference pages to write:**
- [ ] Terminal, package manager, Node, Python, VS Code
- [ ] Claude Code, Cursor, steering files
- [ ] Docker, API keys, hosting, AI defaults
- [ ] The Roster, reimplement-don't-import

**Project shape pages to write:**
- [ ] Octopus-in-a-box, report agent, health tracker
- [ ] Home automation, video creator, budget app, CLI tool

**Curriculum:**
- [ ] Design director track curriculum pages
- [ ] Design builder track curriculum pages
- [ ] Landing page with spiral visualization + track picker
- [ ] "Say cribbage and go" — one-prompt game builder workflow

**Book edits:**
- [ ] Integrate flywheel material from slush pile
- [ ] Study guide readability (Parts I+II at grade 10.7)
- [ ] Remaining readability warnings (workspace page ~grade 9)
- [ ] Add 3 missing shapes to 00-what-do-you-want-to-build.md

**On hold:**
- [ ] Memory Viewer — connect to real Octopus API
- [ ] Wall of data librarian
