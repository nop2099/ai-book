## Sand Castles and Rebar

There's a kind of software that looks finished on the first afternoon. The AI built it. The demo works. The features are there, the layout is clean, the happy path runs without errors. It looks like a building. It's a sand castle.

Sand castles are beautiful and they collapse the moment you push on them. Add a feature, and an existing feature breaks. Fix the fix, and something else shifts. Rename a function, and three files that depended on the old name silently fail. The structure was never structure — it was coincidence. Everything happened to work because nothing had been tested against change. The first refactor is a wrecking ball.

This is vibe coding. The term is new but the pattern isn't. It's what happens when you build by feel — when the code looks right, when it runs once, and when nobody goes back to verify that the parts are actually connected the way they appear to be. AI makes vibe coding faster than it's ever been. You can generate an entire application in an afternoon. You can also generate an entire sand castle in an afternoon. Speed doesn't distinguish between the two.

The difference between a sand castle and a building is rebar. Tests are the rebar. They give the software internal structure — rigid connections between components that hold their shape when something pushes against them. Without tests, every part of the system is loosely packed sand: it stays in place when nothing moves and falls apart the moment you touch it. With tests, you can push on one wall and know the others are still standing because the rebar runs through all of them.

But rebar alone makes a skeleton, not a building. The cement is understanding. Not understanding every line of code — that's neither possible nor necessary when AI writes most of it. Understanding the shape: what this module does, why these components connect, what invariant holds the system together. When you understand the shape, you notice when something doesn't fit, even without a test for it. You catch the problem that the tests didn't anticipate because you know what the system is *supposed* to be, not just what it *currently does*.

Here's the thing about working with AI: the more detail you pour into one area, the fuzzier everything else gets. You spend a day refining the scoring engine and the placement logic drifts. You add a new feature to the front end and the back end develops an inconsistency nobody notices for a week. The AI is working on what you're pointing at. Everything outside the beam of your attention is decaying. Sand doesn't hold its shape in the dark.

Rebar stops this. If the scoring engine has tests, it doesn't drift when you're not watching. If the placement logic has tests, the AI can't quietly break it while adding something else. Tests are the mechanism by which software gets bigger without getting fragile. They let you look away from a part of the system and trust that it's still there when you look back.

The temptation with AI is to skip the rebar because the sand castle looks so good. It assembled itself in an hour. It runs. The demo impressed everyone. Why slow down to write tests for something that already works? Because "already works" is a snapshot, not a guarantee. The sand castle works *right now*. The building works *next month*, after you've added three features, refactored the database code, and changed the API. The difference isn't visible on day one. It's visible on day thirty.

The practical version: when the AI builds something and it works on the first try, that's the most dangerous moment. That's when the sand looks most like stone. That's when you should slow down and add the rebar — not because it's broken, but because it will be, and you want the skeleton in place before the wind picks up.

Vibe coding is fine for prototypes, experiments, throwaway scripts. Some things are meant to be sand castles. But anything you plan to live in needs rebar. And the rebar is easy now — the AI writes tests as fast as it writes features. The only cost is the decision to ask for them.

---
