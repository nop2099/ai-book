## The Intern Who Improves

There's a framing that circulates among developers: AI is like an intern. It's useful but you have to check its work. That was true. The mistake is using the present tense.

The models are not static. The intern you hired in January is not the intern sitting in front of you in June. If you're still checking every line of output the same way you did six months ago, you're wasting your time. If you stopped checking entirely because it was fine last month, you're going to miss the new category of mistake that comes with new capabilities. The skill isn't "how much do I trust AI." The skill is *recalibration* — adjusting your level of oversight to match the system's current ability, which is a moving target.

This is a genuinely new problem. Most tools don't change between uses. A hammer doesn't get better at hammering while you sleep. A spreadsheet doesn't learn new functions overnight. But these models do. You go to bed with a system that can't do multi-step reasoning reliably, you wake up and it can. Your calibration from yesterday is wrong today. And it will be wrong again tomorrow, in a direction you can't predict.

The developers who work with AI every day figured this out first. They talk about it in practical terms: this model is good at boilerplate but hallucates API calls, that model handles refactors well but loses context in long files. They're constantly recalibrating. Not because they're paranoid — because they noticed the ground shifting under them and adapted.

The pattern generalizes far beyond code. Anyone relying on AI output — for research, for writing, for analysis, for decision support — needs the same skill. You need a mental model of what the system is good at *right now*, and you need the habit of updating that model regularly. Not on a schedule. On evidence. When it surprises you — in either direction — that's data. Adjust.

The three failure modes are predictable. First: over-trust. You had a good run, everything checked out, so you stop checking. This is when errors compound silently. Second: under-trust. You got burned once, so you verify everything manually, which defeats the purpose of having the tool. Third, and most common: stale trust. You calibrated once, months ago, and never updated. You're managing an intern who no longer exists.

The heuristic is simple. Check aggressively when you start, when the model changes, or when you enter a new domain. Check less as you accumulate evidence of reliability in a specific context. And never stop spot-checking entirely, because the system will develop new capabilities and new failure modes simultaneously.

The intern is improving. Your job is to notice.

---
