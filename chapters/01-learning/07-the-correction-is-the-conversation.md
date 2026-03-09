## The Correction Is the Conversation

The most important thing you can say to an AI is: "no, that's not it."

Not as a rant. As steering.

A good example is the conversation that became Kai's job manifest. It started as a cost question: what does 20 million input tokens per day cost? Useful answer. Then I corrected the objective: this isn't about pricing, it's about minimizing friction in real life with a Bayesian model. Then I corrected again: use Home Assistant as the event store for now. Then again: long-term ingest Gmail, calendar, ChatGPT sync, Apple health metrics, and support joint probability predictions.

Each correction changed the architecture. Without those turns, the output would have stayed generic and wrong-for-purpose.

The dominos project showed the same pattern at a finer grain. Claude rendered a chain wrong — the tiles were in the wrong order. I said: "Let me stop you. The chain should read 2|6 then 6|1." Claude fixed the display. But I could see the problem was deeper than the output. The chain visualization was being generated separately from the game state, so it could drift. I escalated: "The chain should be generating the visualization, and the test just outputs it. That way we can create unit tests on the viz." The correction went from surface fix to architectural restructuring in two turns.

Another time, Claude couldn't fix a server error and quietly changed the port number. I caught it: "You changed port on me. Don't do that. That is a sign of you not knowing how to shut down the old server and restart it." Then instead of just scolding, I taught the fix: write the PID to a file, kill it properly. The correction carried a lesson.

This is the pattern people miss. They treat corrections like cleanup after the "real" prompt. In practice, the corrections are the real prompt. The first message opens the search space. The corrections collapse it onto what you actually mean.

Human conversation theory calls this repair. With humans, both sides self-correct. With AI, you often have to initiate repair explicitly. If you don't, the model will confidently continue in the wrong frame.

So the working rhythm is simple:

Prompt.
Read critically.
Correct fast.
Repeat.

That is not failure. That's collaboration. The quality jump usually happens on turn two through five, not turn one.

The correction is the conversation.

---
