## The Bathroom Light Is a Bayesian Signal

New Year's Day, I was pricing out how much it would cost to run Kai at twenty million input tokens a day. A practical question. Boring, even. Three thousand dollars a month for input alone. I closed the laptop and went about my day.

Two days later I came back to the same conversation, but I wasn't thinking about costs anymore. I'd been watching a talk — a neuroscientist named Jeff Beck on the Machine Learning Street Talk podcast, explaining how the brain does inference. His argument was that the brain is fundamentally Bayesian: it maintains beliefs about the world, updates them with evidence, and the whole point of perception is to figure out where you can *intervene*. Not just what's true. Where you can push.

The line that stuck: the more tightly linked your actions are to the things that causally impact the world, the more effective those actions are. They point directly to where you should intervene.

I'd been thinking about Kai's job — minimize friction in my life — and suddenly I had the frame for it. I typed: "I want a Bayesian system. That uses joint probabilities. I want it to focus on the data that supports its affordances." And I pasted the link to the talk.

What followed was four hours of me talking through the architecture. Not writing code. Talking. Working backwards from a single question: will I leave the house?

I know my own mornings. I know that if YouTube is playing on the TV at 8:30am, I'm not leaving anytime soon. I know that the bathroom light coming on means I'm getting ready. I know that the TV going off is the departure sequence starting. These aren't correlations I read in a dataset. They're facts about my life that I've lived a thousand times.

So I said: leaving the house is the keystone metric. Everything else exists to predict that. Time of day and day of week give you a baseline — on Tuesdays at 9am, historically, there's maybe a 12% chance I leave in the next fifteen minutes. Then you layer in what's actually happening. YouTube is on? Multiply by 0.5 — I'm anchored. Bathroom light came on? Multiply by 1.2 — the routine has started. Each signal adjusts the probability based on how causally linked it is to the outcome.

This is Bayes' theorem. In plain English: start with your best guess, then adjust it every time you learn something new. The math version is "prior times likelihood, normalized" — your starting probability, multiplied by how much each new piece of evidence should change it, scaled so the numbers still add up. I didn't call it that in the conversation. I said things like "we predict the supporting modifiers first, then the primary outcome" and "what's the probability I'd leave if I was watching YouTube fifteen minutes prior." ChatGPT wrote the math. I described the world.

The spec kept growing. The dashboard should be the primary actuator — Kai doesn't act on the world directly, it acts on the dashboard. Chill is a KPI — track interventions per day, average dashboard intensity, days with zero interventions. It could even predict its own intervention level, I said. If I'm a stubborn boy who's always late, the system should know that about me and plan accordingly. That's not just funny, ChatGPT said. That's correct.

By the end of the afternoon I had a five-hundred-line specification. Not pseudocode. Not a feature list. A document that described, precisely, the causal structure of my morning routine and the Bayesian machinery for reasoning about it.

Then I opened a terminal. Gave Claude the spec and a Home Assistant token. Four hours later it was running — a live prediction engine on a fifteen-minute loop, pulling sensor data from my apartment, computing baseline priors by day-of-week and time bucket, multiplying in likelihood ratios for every signal, and displaying the result on a dark-mode dashboard with an explanation panel showing which evidence was pushing the probability up or down.

I didn't write the prediction engine. I couldn't have. I don't remember how to multiply matrices or normalize probability distributions or implement Laplace smoothing for sparse data. But I didn't need to. The hard part wasn't the math. The hard part was knowing that the bathroom light *means something* and YouTube *means something else* and that those meanings are causal, not just correlative.

Beck spent an hour explaining why this matters. He was talking about the brain, but he was also talking about something more general: the difference between a model that predicts accurately and a model that tells you where to intervene. A black-box predictor might guess that I'm 15% likely to leave the house right now. A causal model tells you *why* — YouTube is anchoring me, the lights are off, I'm settled — and that legibility is what makes intervention possible. You can't nudge someone if you don't know what's holding them in place.

Oracle's code reads exactly like this. There's a dictionary called LIKELIHOOD_RATIOS that maps each observable signal to its causal impact on departure. TV on: 0.8, predicts staying. TV off: 1.5, predicts leaving. YouTube active: 0.5, strongly predicts staying. Lights on: 1.2, maybe getting ready. Each one is Beck's "affordance tightly linked to something that causally impacts the world." And the prediction function just walks through them, multiplying each ratio into the running odds, tracking every contribution so the dashboard can show its work.

An AI wrote that function. But the numbers — the 0.8 and the 1.5 and the 0.5 — those encode *my* knowledge of *my* life. The model of the world was mine. The math was the machine's.

I think this is what actually changes when AI gets good enough. Not that you can do things you couldn't do before — that's obvious and everyone says it. What changes is the *kind* of knowledge that becomes actionable. I've always known that the bathroom light means I'm getting ready to leave. I've known it for years. But that knowledge was trapped — it was intuition, lived experience, the kind of thing you can't put in a spreadsheet. Now I can. I can say "the bathroom light coming on is a 1.2x signal for departure" and a machine can take that seriously, fold it into a formal model, and compute the consequences. My common sense became mathematics. Not because I learned math, but because the gap between knowing something and computing with it closed.

It's not running anymore. The Home Assistant token expired, I got busy with other things, the hardware situation changed. That's fine. Oracle was never the point. The point was the afternoon — the four hours where I went from watching a talk about how brains do inference to having a working system that did inference about my own life. The spec, the conversation, the build. From Beck's insight to a running Bayesian engine in one bright January day.

The spec is still there. The code is still there. The knowledge — which signals are causal, which are noise, where to intervene in a stubborn man's morning routine — that was always there. It just needed a way to become math.

---
