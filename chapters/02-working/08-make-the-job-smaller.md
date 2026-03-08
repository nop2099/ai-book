## Make the Job Smaller

The single most reliable way to get better output from AI is to give it less to do at once.

This sounds obvious. It isn't. The natural instinct when working with a powerful tool is to hand it the whole problem. "Here's ten thousand messages — find the FAQ entries." "Here's my codebase — refactor the authentication." "Here's my life — make a plan." The models are smart enough to attempt it. They're not smart enough to do it well. The result is a confident-looking output that's mediocre across every dimension because attention was spread too thin.

The fix is decomposition, and it works the same way in AI as it does in every other engineering discipline: break the big job into small jobs that each get full attention.

Someone needed to extract FAQ entries from a massive corpus of support messages. The brute-force approach — "read all of these and pull out the FAQs" — produces mush. Too many topics, too many edge cases, too many signals competing for attention. The decomposed approach: first, run named entity detection across the entire corpus. Identify the distinct topics. Then, for each topic, process only the messages about *that topic* and extract the relevant FAQ entries. Same data. Same model. Radically better results. Because each step gets the model's full attention on a smaller, clearer problem.

This is the eternal tension: context versus focus. More context means the model knows more. More context also means the model attends to more, which means it attends to each thing *less*. A 200,000-token context window doesn't mean you should fill it. It means you *can* fill it, but the quality of attention degrades as the window fills, just like it does for humans. The model version of "I have too many tabs open" is real.

The pattern shows up everywhere once you start looking. Iterative development loops — where an AI works on a task, checks its results, and refines — outperform single-shot attempts not because the model gets smarter between iterations, but because each iteration focuses on a smaller problem: "what's still broken?" instead of "build the whole thing." The loop doesn't add intelligence. It adds focus.

There's a practical corollary that matters for daily work: AI tools often truncate or hide their own output to save context space. They'll pipe to `tail -20` or summarize their results instead of showing you everything. This is the model optimizing for its own context budget, and it means you're losing information. The countermove is simple: tee the output to a file. `command | tee /tmp/output.log | tail -20` gives you the summary *and* preserves the full output for later inspection. Yes, this leaves temp files around. That's fine. Disk is cheap. Lost output is expensive.

The general heuristic: when AI output quality drops, your first instinct should be "is this job too big?" before "is this model too dumb?" Decompose the problem. Run it in stages. Give each stage full attention and minimal distraction. The same model that produces mediocre results on a big job will produce excellent results on each piece of that job, if you structure the pieces right.

Making the job smaller makes the job get done better. That's the whole shape.

---
