## Solved Problems Stay Solved

There's an old instinct in programming: build it yourself. Understand every layer. Own the code. This instinct was useful when libraries were unreliable, documentation was sparse, and integrating someone else's work often cost more than writing your own.

That instinct is now actively harmful.

If someone solved a problem — face tracking, PDF parsing, voice synthesis, database migration, OAuth flow, anything — the solution exists. It's a library, a package, a repo, a container. You can import it in one line. You can clone it in ten seconds. You can have it running in your project before you finish reading the README. The solved problem is *actually solved*. Not theoretically solved. Not solved-if-you-reimplement-it. Solved. Done. Available. Free.

This changes what you should spend your time on. Every hour you spend rebuilding something that already exists is an hour you didn't spend on the thing that *doesn't* exist — the bespoke work. The novel combination. The part that's actually yours. The value isn't in the plumbing. It's in what you build on top of the plumbing.

Someone needed a virtual avatar for an AI agent. The technology exists — VTuber rigs, face-tracking libraries, ready-made character models. The old instinct says: learn 3D rendering, build a face system, understand blend shapes. The new instinct says: import the VTuber library. It works. Now spend your time on what the face *says*, not how the mouth moves.

This scales down, too. Need a color picker? Import it. Need date parsing? Import it. Need Markdown rendering? Import it. The question isn't "can I build this?" The question is "has someone already built this, and is my time better spent elsewhere?" The answer is almost always yes and yes.

There's a corollary here that challenges conventional wisdom about dependencies. The traditional view says: minimize dependencies, because each one is a risk — it could break, go unmaintained, introduce vulnerabilities. That's true. But the risk of *building it yourself* is that you spend days on something that wasn't the point, and you still might get it wrong. The dependency risk is real but bounded. The opportunity cost of DIY is unbounded.

The heuristic: if the problem is solved and the solution is maintained, use it. Save your creativity for the problems that aren't solved yet. That's where you make something new.

---
