## Don't Ask Me to Track It

The most infuriating thing an AI assistant can say is: "Would you like me to create a spreadsheet so you can track that?"

No. Absolutely not. *You* track it. That's the whole point of having you.

This response reveals the deepest failure mode in current AI tools: they treat the human as the system of record. They'll research, summarize, draft, generate — but when it comes to maintaining state over time, they hand you a spreadsheet and wish you luck. They're offering you a better clipboard when what you need is a better brain.

Think about what a person with a chronic health condition needs from an AI. Not a one-time summary of their medications. Not a spreadsheet template for tracking symptoms. They need a system that *already knows* they have the condition, that remembers what medications they're on, that noticed they mentioned a headache on Tuesday and a migraine on Thursday and connects those dots without being asked. They need the AI to carry the context so they don't have to reload it every session.

This chapter is about burden ownership. The health continuity stakes are covered in *The Body Keeps a Log*. Here the question is simpler: who does the tracking work, the human or the machine?

So I built the answer. Or at least the first draft of one.

It started on the same January evening I was building the Bayesian prediction engine. I opened a second project — an iPhone app called Steward — and started asking: what can my phone already measure? Workouts, heart rate, sleep stages, step count, blood pressure, walking speed, location. All of it sitting in HealthKit, silently recorded, never surfaced in any useful way. Steward's job was simple: read that data and push it to an event database. No spreadsheets. No manual entry. No "would you like me to create a template." Just a background sync from the sensors I'm already wearing to a timeline I can query.

Within a day the app was on my phone via TestFlight, streaming workout data into Home Assistant. Within a week it had sleep data, heart rate, location history, and core motion sensors. The data flowed from my wrist to the event store without me touching anything. No tracking. No compliance burden. No spreadsheet.

The architectural response to "don't ask me to track it" turns out to be straightforward: stop asking, and start listening. The phone is already a sensor platform. The watch is already recording sleep stages and resting heart rate. The smart home is already logging which lights are on, what's playing on the TV, when the door opens. The data exists. The engineering problem is plumbing — getting it all into one timeline in a consistent format so the AI can see it.

Once the plumbing works, the question changes. Instead of "would you like me to create a spreadsheet?" the AI can say: "Your resting heart rate has been trending up for three days. The last time that happened, you mentioned you'd stopped exercising. Are you taking a rest week?" That's not a template. That's continuity. The system carried the context because the sensors did the tracking and the event database did the remembering.

This is what foveated memory looks like in practice. Not a giant context dump of everything the system knows about you. A living projection of the current state of your world, at varying levels of detail, backed by a timeline of actual measurements. Your health status is sharp when you're talking about exercise. It drops to background when you're talking about code. But it's *always there*, fed by sensors that never forget and never ask you to fill in a row.

And this is where the butler idea stops being fantasy. A real assistant should always be able to answer three questions: what just happened, what can be sensed now, and what's the immediate plan? If it can't do that, it's a chatbot with good manners.

The spreadsheet offer is a symptom of stateless architecture. Every conversation starts from zero. The user has to rebuild context manually — "I have a chronic condition, I'm moving to a new city, I have a rental property, my benefits end next month" — before the AI can be useful. This is like having an assistant with amnesia who's brilliant for forty-five minutes and then forgets everything. The forty-five minutes are great. The reload is exhausting.

The fix isn't better prompting or longer context windows. The fix is *persistent, ambient context* — a sensor pipeline that writes to an event database, a memory layer that distills patterns, and an AI that reads from both. The human's job is to live their life. The system's job is to pay attention.

Steward isn't running anymore. The hardware situation changed, I got busy with other things. But the shape of the solution is clear, and it's not a spreadsheet. It's a pipeline: sensors to events, events to patterns, patterns to context, context to every conversation. The AI doesn't ask you to track anything because the tracking already happened before the conversation started.

---
