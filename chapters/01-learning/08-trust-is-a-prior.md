## Trust Is a Prior

There was a cat who had never been outside. Indoor cat, whole life. One day someone carried her into the backyard, set her down in the grass, and sat nearby. She froze. Crouched low, ears back, scanning for threats. After ten minutes she took a step. After twenty she sniffed something. After an hour she was cautiously exploring a three-foot radius. The next day, same thing — but the freeze was shorter, the radius wider. After a week she was trotting around the yard, rolling in patches of sun, occasionally glancing back to make sure the door was still open.

That's Bayesian trust. A prior that starts near zero — I have no evidence this is safe — and updates incrementally with each positive observation. The cat doesn't decide to trust the backyard. She accumulates evidence that the backyard is trustworthy. Every trip outside without a threat nudges the prior upward. Every calm return to the house confirms: this is a place I can be.

Then the move happened. New house, new yard, new smells, unfamiliar geometry. The prior reset. All that accumulated evidence — the sunny patch, the specific fence line, the distance to the door — was invalidated. And the cat, faced with a brand new environment and a reset prior, ran.

Trust in AI works the same way.

You start with a tool and you don't trust it. You verify every output. You check the code it wrote. You read the email before you send it. You fact-check its claims. This is correct behavior — your prior is low and you don't have evidence yet. Each time the tool gets something right, and you verify that it got it right, the prior updates. You start checking less. You let it handle a whole paragraph instead of a sentence. You let it refactor a file without reading every line. You're not being careless. You're being Bayesian. The evidence supports expanding the boundary.

But switch models and the prior resets. Switch tools and it resets. Switch from a system where you can see the memory to a system where you can't, and it resets hard — because the thing that made the evidence accumulate was your ability to verify. A transparent system builds trust because every output is checkable. A black box can be just as capable, but the evidence never accumulates because you can't see the work. You're back to the frozen cat, crouching in unfamiliar grass.

This is why readable memory matters more than sophisticated memory. A system that stores its knowledge in files you can open, grep, and verify builds trust faster than a system that stores knowledge in embeddings you can't inspect. The file isn't just a memory format — it's evidence. Every time you open the worklog and confirm that yes, the AI recorded what actually happened, your prior on the system's reliability nudges upward. Every time you can't see what the system knows, the prior stalls.

The practical pattern: give the AI a small task. Verify the output. Give it a slightly larger task. Verify again. Expand the boundary each time the evidence supports it. This isn't micromanagement — it's calibration. And the calibration is per-tool, per-model, per-domain. Trust built with one model in one context doesn't transfer automatically to a different model in a different context. The cat trusted *that* yard. Not yards in general.

The failure mode is skipping the verification. People either trust too early — handing over complex tasks before they've built evidence that the tool handles complexity well — or they never trust at all, verifying every comma forever because they never internalized the positive evidence. Both are miscalibrated priors. The first ignores the base rate of AI errors. The second ignores the accumulated evidence of AI competence.

The cat story has one more lesson. She ran not because the new yard was dangerous, but because the context changed faster than the trust could transfer. That's what happens when you upgrade tools, switch platforms, or adopt a new architecture. The capability might be identical or better. But the trust infrastructure — the accumulated evidence, the verification habits, the known boundaries — doesn't migrate. You have to rebuild it. Not from zero, because you've learned what to check and how to check it. But the prior on *this specific system in this specific context* starts fresh.

Trust is not a feeling. It's a posterior probability, updated by evidence, specific to context, and reset by change.

---
