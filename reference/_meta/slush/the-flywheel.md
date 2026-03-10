# The Flywheel

## The ratio

Fifteen minutes. That's how long it took to direct a working cribbage game into existence — complete with a visual peg board, full scoring, an AI opponent, and a training mode that shows expected value for every play.

Wall clock: two and a half hours. AI working time: about an hour. Human time: fifteen minutes across five or six interventions. The rest was ignoring it.

The fifteen minutes were the high-value part. "It's cribbage." "The dots on the board look wrong." "Did we miss a last card rule?" "I want a training mode." Five corrections. Each one took seconds to say and would have taken hours to figure out from the code side.

## The skill isn't building

A programmer could have built the same game. It would have taken days, maybe a week. They would have gotten the scoring right eventually, the state machine working, the pegging logic correct. But they wouldn't have caught "the dots look wrong" without playing cribbage for years. They wouldn't have known the last-card rule was missing without having argued about it at a kitchen table. They wouldn't have asked for training mode with expected value analysis because that's a request that comes from wanting to get *better at cribbage*, not better at code.

Domain expertise is the bottleneck now. Not technical skill. The person who's played 500 hands of cribbage will build a better cribbage game in 15 minutes of directing than a great programmer will in a week of coding.

## Two tracks

There are two kinds of people building things with AI, and they need different paths.

**Builders** want to understand the engine. They learn by writing code, reading code, understanding what a state machine is and why immutable updates matter. Their pace is slow and deliberate. Draw a shape. Place tiles on a grid. Build a simple game. Add polish. Build a second game and notice it's faster. The flywheel for builders is programming intuition — each project leaves you understanding more about how software works.

**Directors** want to drive the car. They learn by saying what they want, playing with the result, and correcting what's wrong. Their pace is fast. Say "cribbage." Play it. "The dots look wrong." "Add training mode." Done. Move on to the next game. The flywheel for directors is taste and judgment — each project sharpens your ability to notice what's wrong and know what to ask for next.

Both are valid. Both compound. But they compound different things.

## What compounds

The builder gets better at understanding code. Good. But the director gets better at something harder to teach:

1. **Describing clearly.** "It's cribbage, on a board" was four words and it was enough. Knowing what to say — and what to leave out — is a skill that improves with practice.

2. **Spotting wrongness.** The five corrections in the cribbage build were all visual or domain-level. The board looked wrong. A rule was missing. Animations overlapped. None of these required reading code. They required having eyes and knowing the game.

3. **Asking for the right next thing.** A training mode with expected value analysis is not an obvious request. It came from wanting to learn from the AI opponent — from thinking about the game as a player, not as a programmer. That instinct gets sharper every time you build something.

4. **Knowing when you're done.** The game worked. It looked right. The training mode was in. Stop. This is a skill. Most people over-build or under-build. Experience teaches you where "done" lives.

## The flywheel

Here's the Amazon insight applied to building: every engagement makes your tools stronger and the next engagement cheaper.

A consultant goes out to do a job. They come back with the deliverable *and* with better software. The next job uses that software. It takes less time. The savings compound. Eventually they're not selling hours — they're selling capability.

This is having your cake and eating it too. You do the work *and* you get better tools. Every project is simultaneously the deliverable and the training data for your next project.

But it only works if you start. Without a first turn of the flywheel, there's nothing to compound. Start small, start now.

The cribbage game was a first turn. The second game — whatever it is — will go faster. Not because the code transfers (though some might), but because the person directing it now knows what "done" looks like, what to check for, and what to ask for that they didn't know to ask for last time.

You're not spending your time working. You're investing it.

## The spiral

The flywheel isn't flat — it's a spiral. Each turn covers the same ground at a higher altitude.

**Wonder → Try → Break → Know.**

Ring 1: "Can AI even build a board game?" → "It's cribbage" → go bug, dots look wrong → "Oh, this actually works."

Ring 2: "What else could it build?" → Second game → Different friction points → "I know what to look for now."

Ring 3: "Can I make this process repeatable?" → Reference material, patterns, checklists → "The reference page should warn about state machine edge cases" → "Now anyone can do this."

Ring 4: "What does this change about how I work?" → You're not a programmer and you're not a non-programmer. You're something new. You direct. You taste-test. You invest fifteen minutes and get hours of output. → "This is just how I build things now."

Each ring is complete on its own. If you stop after Ring 1, you've built a game. If you stop after Ring 2, you've built a practice. Ring 3, you've built a system. Ring 4, you've changed.

## The director's curriculum

For people who don't want to learn programming — who want to build things by directing AI — the path looks like this:

**Ring 1: Say the thing.** Pick a well-known game. Say its name. Play it. Find what's wrong. Fix it with words, not code. You're done when you'd show it to someone.

**Ring 2: Say the next thing.** Pick a different game. Notice how much faster it goes. Notice what you check for now that you didn't check for last time. That's the flywheel.

**Ring 3: Say what's missing.** Add the thing that makes it *yours* — training mode, variants, custom rules, the thing no existing version does. This is where domain expertise becomes product instinct.

**Ring 4: Help someone else say it.** Write down what you learned. What to check for. What to ask for. What "done" looks like. Now you've built something that compounds for other people too.
