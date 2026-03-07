## Don't Ask Me to Track It

The most infuriating thing an AI assistant can say is: "Would you like me to create a spreadsheet so you can track that?"

No. Absolutely not. *You* track it. That's the whole point of having you.

This response reveals the deepest failure mode in current AI tools: they treat the human as the system of record. They'll research, summarize, draft, generate — but when it comes to maintaining state over time, they hand you a spreadsheet and wish you luck. They're offering you a better clipboard when what you need is a better brain.

Think about what a person with a chronic health condition needs from an AI. Not a one-time summary of their medications. Not a spreadsheet template for tracking symptoms. They need a system that *already knows* they have the condition, that remembers what medications they're on, that noticed they mentioned a headache on Tuesday and a migraine on Thursday and connects those dots without being asked. They need the AI to carry the context so they don't have to reload it every session.

This is what people mean when they say they want AI to "know them." They don't mean personality. They don't mean warmth. They mean: stop asking me to re-explain what is already known. My health history, my financial picture, my projects, my relationships, my preferences — this information exists. I've told it to you, or to a system adjacent to you. The fact that you can't access it is an engineering failure, not a feature request.

The architectural response to this problem has a name: foveated memory. Like human vision — sharp in the center, blurry at the edges, but nothing lost. A system that maintains a living projection of the current state of your world, at varying levels of detail, and injects the relevant parts into every AI interaction. Your health status is LOD 2 when you're talking about exercise. It drops to LOD 0 when you're talking about code. But it's *always there*, ready to expand when needed.

Some people build this with prediction models — engines that watch signals and infer what's likely to happen next. Some build it with health bridges — systems that pull data from wearables and medical records and surface it when relevant. Some build it as a memory service that watches every conversation and distills facts into a persistent knowledge base. The specific architecture matters less than the principle: the system should carry the context, not the human.

The spreadsheet offer is a symptom of a deeper problem. Current AI tools are stateless by default. Every conversation starts from zero. The user has to rebuild context manually — "I have a chronic condition, I'm moving to a new city, I have a rental property, my benefits end next month" — before the AI can be useful. This is like having an assistant with amnesia who's brilliant for forty-five minutes and then forgets everything. The forty-five minutes are great. The reload is exhausting.

The fix isn't better prompting or longer context windows. The fix is *persistent, ambient context* — memory that lives outside any single conversation and flows into all of them. The AI shouldn't ask you what you need to track. It should already know what you're tracking, because it's been paying attention all along.

Context is expensive. That's the engineering constraint. Every token of memory is a token you can't use for reasoning. Every fact you inject is a fact that displaces something else. This is real, and it means you can't just dump everything into the context window and hope for the best. You need *foveation* — intelligent compression that keeps the important things sharp and lets the background blur. You need a system that knows what matters *right now* and can shift focus instantly when the conversation changes.

But expensive doesn't mean impossible. It means it's an engineering problem, and engineering problems get solved. The question isn't whether AI will eventually maintain persistent context. It will. The question is whether you're building toward that future or accepting spreadsheets in the meantime.

---
