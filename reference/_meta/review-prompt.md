# Agentic Review Prompt

Read the reference page provided. Check the following:

1. **Structure** — Does it have: What it is, Why you'd use it, How to set it up, How to prompt your AI, How to verify, Book link?
2. **Completeness** — Are Mac, Windows, and Linux covered where applicable?
3. **Accuracy** — Do the commands look correct for current tool versions?
4. **Promptability** — Could a reader paste the "How to prompt" section into an AI chat and get useful help?
5. **Verify step** — Is there a concrete command that proves setup worked?
6. **Tone** — Is it direct? No filler? Does it respect the reader's time?
7. **Reading level** — Target 8th grade. If a 14-year-old can't read it, simplify.
   - Flag sentences over 30 words — break them up.
   - Flag words over 3 syllables that aren't technical terms the reader is actively learning (like "JavaScript" or "WebSocket" — those are fine).
   - Flag jargon: words like "heuristic", "deterministic", "idempotent", "orthogonal", "paradigm", "utilize", "facilitate", "encapsulate", "instantiate", "metamer". If you can say it simpler, say it simpler.
   - Prefer "some" over "most", "may" over "will" — the reader is smart and has read the guide.
   - Technical terms that are being *taught* (like "pure reducer" or "event sourcing") are fine when introduced with a plain explanation. Jargon used casually without explanation is not.

Run `bash reference/_meta/check-readability.sh` for an automated first pass on grade level, jargon, and long sentences.

Report issues as a checklist. Fix what you can. Flag what needs human judgment.
