## Fix Your Papercuts

There's a famous chart that calculates how long you can work on automating a task before you've spent more time than you'll ever save. It cross-references how often you do the task (daily, weekly, yearly) with how much time you shave off (1 second, 5 minutes, 1 hour). The math is correct. The chart is surprisingly hard to read. And the conclusion it implies — that most small optimizations aren't worth the time — used to be right.

It's not right anymore. The cost of fixing things just dropped by an order of magnitude.

A papercut is any small friction you encounter repeatedly. Here's one: macOS screenshots land on your Desktop with names like `Screenshot 2026-03-07 at 2.51.42 PM.png`. Spaces everywhere. AI agents choke on spaces in file paths. If you're using agents and screenshots together — which, if you're working with AI visually, you are — every single screenshot is a broken path. Fourteen lines of bash fixes it permanently: grab the latest screenshot, strip the spaces, rename it `screen.png`, move it to your working directory. The script took five minutes to write. It's been rewritten three times as the need evolved. It was never checked into a repo because it's not a project. It's a fix. And it gets used dozens of times a day.

That's the new math. The old version of this fix — learning the macOS screenshot naming convention, writing the bash, handling edge cases for `.heic` vs `.png`, adding collision avoidance, testing it — might have taken an hour. The chart would say: at fifty uses a day, saving five seconds each, you can justify up to twelve hours on the fix. An hour is well within budget. But most people wouldn't have spent that hour, because the friction felt too small to stop and fix. Now the fix takes five minutes. There's no excuse not to.

The automation cost dropped from hours to minutes, which means the chart's thresholds all shifted left. Tasks that used to be in the "not worth automating" zone are now firmly in "fix it immediately."

This isn't just about scripts. It's about the general principle that small frictions compound. A two-second annoyance that happens fifty times a day is almost three minutes of daily friction. Over a year, that's sixteen hours. Over five years, that's eighty hours — two full work weeks — spent on a thing that annoyed you every single time. The chart shows this math, but the chart also assumed the fix would take an hour. If the fix takes thirty seconds, the payoff starts on day one.

The deeper lesson: most people have trained themselves to tolerate papercuts because the cost of fixing them was historically too high. They don't even *notice* the friction anymore. It's background noise. But background noise is still noise, and it still costs attention — the non-renewable resource. Every time you context-switch to do something manually that could be automated, you lose a little bit of the flow state you were in.

The new habit to build: when you feel friction, stop and fix it. Right then. Not later. Not "when I have time." Now, while the annoyance is fresh and the fix is cheap. Because the chart's math hasn't changed — what changed is the cost column. And when fixing things is nearly free, you should fix everything.

---
