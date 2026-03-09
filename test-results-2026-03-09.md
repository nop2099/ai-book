# Book Test Suite — Promise Tests — 2026-03-09

## Summary
- Chapters tested: 44
- Tests per chapter: 7 (P1-P7)
- Total assertions: 308 + 8 whole-book = 316
- PASS: 214 | WARN: 89 | FAIL: 3
- Pass rate: 68%

## Top-Line Findings

### The Redundancy Problem (P1)
The book has a REDUNDANCY PROBLEM that the folded shapes hide. When you compress to the Vic script or color map, each idea appears once. In the raw text, the same stories get mined repeatedly.

| Element | Chapters | Count | Verdict |
|---------|----------|-------|---------|
| Alex "barrier to the universe" quote | Curiosity, Song, Mentor's Mirror, Loose Prompt | 4 | **CUT to 1.** Keep in Song (where it lands hardest). Remove from the other three. |
| Alex as character (general) | Mirror, Teaching, Every Hat, Conductor, Loose Prompt, Curiosity | 6 | **Reduce to 3.** Keep in Curiosity (first intro), Teaching (his own arc), Conductor (his mind-blown moment). Cut from Mirror, Every Hat, Loose Prompt. |
| Dominos project | Curiosity, Pair Prog, Correction, Tests, Every Hat | 5 | **Keep 3, differentiate.** Curiosity (spiral), Correction (chain fix = architecture), Tests (metamer/Rosetta). Cut from Pair Prog and Every Hat — replace with different examples. |
| Kai job manifest correction sequence | Loose Prompt, Correction, Talking to Duck | 3 | **Keep in Correction** (the promised chapter). Brief reference in Duck. Remove from Loose Prompt. |
| Sensor/HealthKit/event pipeline | Bathroom Light, Everything Is Event, Your Data, Body Keeps Log, Don't Ask Me, Shape of Day | 6 | **Keep 3.** Bathroom Light (origin), Everything Is Event (architecture), Don't Ask Me (the rant). Reference-only in others. |
| Steward app | Body Keeps Log, Don't Ask Me, Your Data | 3 | **Keep in Don't Ask Me.** Brief reference in Body Keeps Log. Cut from Your Data. |
| Foveated memory term | Memory Care, Don't Ask Me, Shape of Day | 3 | **Keep in Memory Care** (where it's defined). Reference-only elsewhere. |
| Mentoring/teaching-sharpens-you | Mentor's Mirror, Teaching the Next Person | 2 | **MERGE these chapters.** They teach the same shape. |
| Body Keeps a Log ↔ Don't Ask Me to Track It | Both chapters | 2 | **MERGE or sharply differentiate.** Both diagnose the same problem (memory loss in health context) and propose the same fix (sensor pipeline). |

### Vic Script Promise Ledger (W7)

| Vic Promises | Delivering Chapter | Status |
|---|---|---|
| Correction is collaboration, turns 2-5 | The Correction Is the Conversation | **DELIVERED** |
| Folder is the interface | The Folder Is the Interface | **DELIVERED** |
| Memory is files | Memory Is Files | **DELIVERED** |
| "Don't ask me to track it" (spreadsheet rant) | Don't Ask Me to Track It | **DELIVERED** |
| Data wall / context gold mine | Context Gold Mine + Your Data | **DELIVERED** |
| Recursive structure (book proves its own thesis) | Context Gold Mine + The Gap | **DELIVERED** (implicit) |
| Kai / Aaron built an agent | We All Invented Calculus | **PARTIAL** — chapter focuses on convergent invention, not the build itself |
| Philosophy not coding | When AI Does Philosophy | **PARTIAL** — argues philosophy matters but doesn't show how it changes practice |
| Trust is Bayesian (cat story) | Trust Is a Prior | **DELIVERED** |
| The gap | The Gap | **DELIVERED** |
| Curiosity spiral (dominos, VTuber) | AI Rewards Curiosity | **DELIVERED** |

### Chapters That Don't Appear in Any Folded Shape (W7 orphans)

These chapters aren't referenced by the Vic script OR the color map summary cards. They either need to earn their place or be absorbed:

- **Learn by Building** — overlaps with Curiosity and Song. Merge into Curiosity?
- **The Kitchen** — charming but thin. Could be a paragraph in another chapter.
- **The Body** (Part 1) — overlaps with Body Keeps a Log. Merge.
- **Agents as Teammates** — practical but no story. Needs a scene.
- **PII, Keys, Security** — important but reads as checklist. Needs a failure story.
- **Sand Castles and Rebar** — good metaphor but no personal story. Generic.
- **The Portable Brain** — states the idea but doesn't show it. Needs Kai export or migration story.

### Sherpa Readiness (W8)

Chapters that work as **consulting diagnostic tools**:
- Fix Your Papercuts (audit: what are your daily frictions?)
- Busyness vs Business (diagnostic: what's the one fire?)
- Make the Job Smaller (intervention: decompose the client's big ask)
- The Folder Is the Interface (setup: reorganize project structure)
- The Steering File (setup: write the first instructions file)
- Don't Ask Me to Track It (infrastructure: build the sensor pipeline)
- The Correction Is the Conversation (coaching: teach the client to correct)

Chapters that are **philosophy only** (reader benefit, not client-facing):
- When AI Does Philosophy, You Named Her, The Gap, We All Invented Calculus, Octopus in the Box

## Prioritized Fixes

### P0 — Do Now (redundancy kills, broken promises, merges)

1. **Kill the Alex quote.** Keep "barrier to the end of the universe" in Song ONLY. Remove from Curiosity, Mirror, Loose Prompt. Replace each with chapter-specific Alex moment or cut Alex reference entirely.

2. **Merge Mentor's Mirror + Teaching the Next Person.** Same shape (teaching sharpens the teacher). Keep the best scene from each, make one chapter called "The Mentor's Mirror."

3. **Sharply differentiate Body Keeps a Log vs Don't Ask Me to Track It.** Body = the PROBLEM (memory loss in health context, why it's dangerous). Don't Ask Me = the SOLUTION (sensor pipeline architecture, the rant). Right now both chapters tell both sides. Split cleanly: Body is Blue (seeing the problem), Don't Ask is Red (building the fix).

4. **Reduce dominos appearances.** Keep in Curiosity (spiral), Correction (architecture fix), Tests (Rosetta Stone). In Pair Programming, replace dominos with a different solo-AI session. In Every Hat, replace dominos role list with a different project.

5. **Fix the "philosophy not coding" promise.** The Philosophy chapter argues philosophy matters but doesn't show a reader how. Add one concrete example: "When Claude hallucinated a function that didn't exist, the fix wasn't debugging — it was asking 'what do you think this function does?' That's theory of mind, not engineering."

6. **Develop Agents as Teammates.** Needs a scene — the 2pm quota wall, switching to Gemini mid-task, the feeling of managing a shift roster. Currently reads as a listicle.

### P1 — Do Next (flow, CTA, underdeveloped chapters)

7. **Tighten The Conductor.** Too short, feels underdeveloped. Add the actual Alex session — what he saw, what surprised him, the specific moment he said "this changes everything." Show the wrong note the conductor caught.

8. **Fix Memory Care ending.** Currently ends with a filter question instead of a call to action. Add: "The first step is the same as Kai's: what does this person need to know right now, and what can wait?"

9. **Tighten The Kitchen.** Either expand with a second example (someone else using AI for real-time coaching in a different domain) or absorb the key insight into Curiosity as a paragraph about "improvisation as the graduation from compliance."

10. **Fix Sand Castles and Rebar.** Needs a personal story — the first time a sand castle collapsed, what it cost, what the rebar was. Currently reads like a blog post.

11. **Fix Portable Brain.** Needs a migration scene — moving context from one tool to another, what survived and what didn't. Currently states the thesis but doesn't show it.

12. **Fix Your Data Is Already Yours ending.** "The only step left is actually going and getting it" is soft. Replace with: "Start tonight. Google Takeout takes ten minutes. Your iMessage database is already on your laptop. The Netflix export takes 48 hours. By Wednesday you'll have a folder that contains more of your own thinking than you remember producing."

### P2 — Polish (POV, internal repetition)

13. **Folder Is the Interface internal repetition.** The title idea is restated 3+ times. Trust the reader to get it after the first clear statement.

14. **We All Invented Calculus ending.** "The benchmark was always us" is motivational but abstract. Ground it in the specific feeling of watching OpenAI ship the thing you already built.

15. **Octopus in the Box applicability.** Add a concrete "try this" — a specific CLI agent setup or a first octopus-in-a-box experiment the reader can run.

16. **Bathroom Light Bayesian explanation.** The "prior times likelihood, normalized" section is dense. It works for technical readers but could lose Alex. Add a one-sentence plain-English version before the formula.
