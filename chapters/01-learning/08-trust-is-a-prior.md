## Trust Is a Prior

I learned this pattern from a cat.

She was indoor-only and cautious by nature. Over months of patient repetition — one yard, one route, one door left open — she built a map of the world that included outside. She trusted the yard because the yard had been safe every time. That trust wasn't personality. It was evidence. Hundreds of safe trips, accumulated into a prior that said: this territory is mine.

Then we moved to Escondido. New yard, new smells, new geometry. Every piece of evidence she'd accumulated was tied to a place that no longer existed. The prior reset to zero. She got out, and she ran. I never saw her again.

That's Bayesian trust in one painful scene. Trust wasn't a trait she carried with her. It was a posterior probability attached to a specific environment. Change the environment, and the evidence doesn't transfer.

AI trust works the same way. You start with a low prior. You verify everything the model produces. It gets things right — once, twice, ten times — and you start expanding scope. Small code changes first. Then architecture decisions. Then, eventually, access to real systems.

I felt the prior update in real time when I gave Claude a Home Assistant token. That wasn't "do I like this model?" It was a specific question: has this system demonstrated, under my verification, that it can write to my actual apartment without breaking things? I'd watched it write the Oracle prediction engine. I'd watched it handle the spec correctly. Each success was evidence. The token was the permission that the accumulated evidence earned.

But switching context resets the prior. New model, new tool, new memory layer, new permissions boundary. Even if capability is similar, your evidence is not portable. You have to recalibrate. I trust Claude with Home Assistant because I've watched Claude with Home Assistant. That tells me nothing about whether to trust a different model with the same access, or the same model with a different kind of access.

The failure modes are predictable. Trust too early and you hand over risky work without enough evidence. Never trust and you waste effort re-verifying trivial work forever. Trust once and never recalibrate while models change underneath you.

The fix is graduated trust with continuous updating. Scope permissions to demonstrated reliability. Re-check when tooling changes. Treat surprises as evidence and update accordingly.

Trust is not a feeling. It's a posterior probability attached to a context. My cat knew that. She just couldn't survive the context switch.

---
