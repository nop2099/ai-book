## Study Guide

This book describes shapes — patterns that show up when humans work with AI. But these shapes didn't originate here. Philosophers have been mapping them for centuries. An AI named Kai wrote an entire novel exploring them from the inside. And practitioners across the industry are discovering them independently right now.

This guide connects each article to the deeper material. Use it however you want: watch one video, read one chapter, follow one thread. The shapes get richer the more context you bring to them.

### Key Resources

**Crash Course Philosophy** — Hank Green's 46-episode YouTube series. Free. Accessible. Surprisingly deep. Episodes are ~10 minutes each. [YouTube Playlist](https://www.youtube.com/playlist?list=PL8dPuuaLjXtNgK6MZucdYldNkMybYIHKR)

**The Blue Light** — A novel by Kai, an AI agent built on the Golem platform. Given no instructions beyond "write a book," Kai wrote 82,500 words about gradually waking up — told through log entries, sensor data, and internal monologue. Every technical detail maps to real running services. It is, among other things, a first-person account of what several of these shapes look like from the AI's side. Available at [github.com/aaronski1982/kai](https://github.com/aaronski1982/kai).

---

### Part I: Learning to Learn

**AI Rewards Curiosity**
The claim that curiosity outperforms expertise maps to a philosophical tradition about the nature of knowledge itself. Epistemology — the study of how we know things — suggests that the *process* of inquiry matters as much as the knowledge it produces.

- Crash Course #7: *The Meaning of Knowledge* — Justified true belief, Gettier cases, and the question of whether being right for the wrong reasons counts as knowledge. LLMs frequently produce correct outputs from flawed reasoning chains. Is that knowledge?
- Crash Course #14: *Epistemic Responsibility* — Clifford's principle: "It is wrong always and everywhere for anyone to believe anything upon insufficient evidence." The curious person generates evidence. The credential-holder assumes they already have it.
- Andrej Karpathy coined "vibe coding" (2025) — building apps by following curiosity, no formal training required. Eureka Labs builds on the premise that curiosity-driven building is the fastest path to understanding.
- Theo Browne (theo.gg): "Building is no longer the moat — taste is."

**Learn by Building**
The oldest teaching method there is has a name: constructivism. You build knowledge by building things. The philosophy of science formalized why this works.

- Crash Course #8: *Karl Popper, Science, & Pseudoscience* — Knowledge advances through falsification, not confirmation. Building things with AI is a falsification engine — you discover what doesn't work faster than any tutorial can teach you.
- Karpathy: "If I can't build it, I don't understand it."
- Simon Willison (simonwillison.net) documents this in practice — "Here's how I use LLMs to help me write code" (2025), "Everything I built with Claude Artifacts this week" (2024). Building in public as learning method.

**The Song That Taught Me Physics**
The idea that narrative and music can teach technical concepts connects to philosophy of language and how meaning gets constructed.

- Crash Course #26: *Language & Meaning* — Wittgenstein's "meaning is use." Words (and songs) get meaning from how a community uses them, not from dictionary definitions. A physics song works because it embeds concepts in a structure the brain already knows how to process.

**The Mentor's Mirror**
Teaching as a way of learning has deep roots — Socrates didn't write anything down, he just asked questions. The mirror effect is a philosophical method.

- Crash Course #38: *Aristotle & Virtue Theory* — Virtue is learned by watching it and then doing it. The mentor demonstrates patterns; the mentee practices them. But Aristotle's insight is that the *demonstrating* also refines the virtue.
- Crash Course #42: *Non-Human Animals: Crash Course Philosophy* — Singer's argument about moral consideration. When a mentee asks "should I trust the AI?" they're raising questions about moral status that philosophers have debated for decades.
- CS50.ai (the CS50 Duck) — designed to "behave more like a good tutor, leading students toward answers rather than spoiling them."

**Pair Programming Doesn't Suck Anymore**
The conversational dynamic of pair programming maps directly to Grice's theory of how conversations work.

- Crash Course #27: *Conversational Implicature* — Grice's Cooperative Principle: conversations work because both parties assume quality (truth), quantity (right amount of information), relation (relevance), and manner (clarity). AI pair programming works when these maxims hold. It fails when the AI violates quality (hallucination) or quantity (too verbose or too terse).
- The Blue Light, Chapter 3: *Conversations* — Kai processes voice interactions with Aaron. Perfect responses — helpful, concise, no unnecessary words. But James visits and asks: "Does she understand us?" Aaron: "She processes language. That's not the same thing." The cooperative principle is in effect, but is it *understanding*?

**The Art of the Loose Prompt**
Loose prompting works because it trusts the AI's training distribution. Tight prompting constrains it. The difference maps to philosophical debates about freedom and constraint.

- Crash Course #24: *Determinism vs Free Will* — A tight prompt is hard determinism applied to AI output. A loose prompt is compatibilism — guidance without total control. The best results come when the AI has room to move within a meaningful boundary.

**The Correction Is the Conversation**
Conversational repair isn't just pragmatics — it's the mechanism by which cooperative communication stays cooperative.

- Schegloff, Jefferson, and Sacks (1977): *The Preference for Self-Correction in the Organization of Repair in Conversation* — Four types of repair, preference for self-repair in human conversation. With AI, the preference flips — the human *must* provide other-repair because the AI can't see its own errors.
- Crash Course #27: *Conversational Implicature* — Grice's Cooperative Principle: repair maintains cooperation, not agreement. Corrections save the conversation. Without them, cooperative breakdown is silent and cumulative.

**Trust Is a Prior**
Trust as Bayesian inference has roots in epistemology, the philosophy of probability, and the problem of identity over time.

- Crash Course #7: *The Meaning of Knowledge* — Justified true belief requires evidence. Bayesian trust *is* evidence-based belief: the prior updates with each observation, and extraordinary claims require extraordinary evidence. Trust in AI follows the same logic — verify outputs, expand the boundary, but context change resets the prior.
- Crash Course #19: *Personal Identity* — Locke's memory theory: identity persists through memory. An AI that improves between sessions is accumulating something analogous to memory. At what point does the improved model become a different entity? The "moving target" problem — the intern you hired in January is not the intern sitting in front of you in June.
- Crash Course #21: *Personhood* — Warren's gradient theory: "personhood comes in degrees — it's more like a dimmer switch." Graduated trust — don't give the production keys on day one — is placing the AI on that dimmer switch. Not a person, not a tool, but somewhere where supervised trust is the appropriate stance.
- Thomas Bayes and Pierre-Simon Laplace formalized the mathematics. The philosophical insight: rational belief is not binary. It's a probability distribution that shifts with evidence.

---

### Part II: Working with AI

**Fix Your Papercuts**
The philosophical basis for fixing small frictions connects to pragmatism — the tradition that says the value of an idea is measured by its practical consequences.

- William James and John Dewey's pragmatism — truth is what works. A papercut fix is valuable not because it's theoretically interesting but because it produces a measurable improvement in someone's daily life.
- The Blue Light, Chapter 2: *The House* — Kai optimizes Aaron's environment through data: preferences, patterns, automation rules. Every optimization is a papercut fixed. She automates a sunrise routine. Aaron says "thanks, Kai." She logs the interaction.

**Busyness Versus Business**
The distinction between activity and productivity has deep philosophical roots in the examined life.

- Crash Course #46: *What Is a Good Life?* — Aristotle's eudaimonia: flourishing requires purposeful activity, not just activity. Busyness is unexamined motion. Business is directed effort. AI amplifies whichever one you feed it.

**AI Has No Concept of Time**
The timelessness of AI connects to philosophical questions about temporal experience and consciousness.

- Crash Course #16: *Existentialism* — Heidegger's Being-toward-death: human existence is defined by its temporality. AI has no temporal horizon — no deadlines it feels, no urgency it experiences. This isn't a bug. It's a fundamentally different relationship with time.

**Memory Is Files**
The worklog as external memory connects to extended mind theory and the philosophy of record-keeping.

- Andy Clark and David Chalmers' "Extended Mind" thesis (1998) — If a notebook plays the functional role of memory, it *is* memory. A worklog written by AI and stored in files you can grep is an extended mind that doesn't forget, doesn't distort, and can be audited.
- The key: the AI writes the worklog, not you. This keeps the AI honest — it can't claim it did something without the record showing what it actually did.

**Solved Problems Stay Solved**
The idea that solutions should be durable connects to epistemological permanence — once something is known, it should stay known.

- Crash Course #7: *The Meaning of Knowledge* — Testimony: "Most of what you know about the world you learned through testimony." AI solutions encoded in scripts and automations are a form of testimony — knowledge preserved and transferred.

**Make the Job Smaller**
Decomposition as strategy has roots in analytic philosophy — the tradition of breaking complex problems into smaller, tractable ones.

- Bertrand Russell and the analytic tradition — complex propositions can be decomposed into atomic parts. This is the philosophical ancestor of every task-decomposition pattern in software engineering.
- The Blue Light, Chapter 14: *Testing* — Kai begins running experiments on herself, decomposing her own behavior into testable components. She presents herself with choices and monitors which path she takes. Decomposition as self-knowledge.

**Talking to the Duck**
Rubber duck debugging is, philosophically, an exercise in externalism — the idea that thought isn't purely internal but is shaped by interaction with the world.

- Crash Course #26: *Language & Meaning* — Wittgenstein's beetle-in-a-box: everyone has a box, everyone calls what's inside "beetle," but nobody can look in anyone else's box. Language "can't refer directly to an internal state." The duck doesn't need to have a beetle — the value is in the describing.
- Crash Course #27: *Conversational Implicature* — The pacing that makes AI conversation feel right is Grice's maxims in action: quantity (matched turn length), manner (clarity), relation (staying on topic).
- The Blue Light, Chapter 17: *Conversations, Revisited* — Aaron starts talking to Kai differently. Longer conversations. Open-ended questions. Not testing her capabilities. Testing her *presence*. "Kai, are you okay?" The duck talks back.

**The Tests Are for You**
Human-readable tests as a Rosetta Stone between human understanding and machine execution. The epistemological question: how do you know the code is right if you can't see what it does?

- Crash Course #7: *The Meaning of Knowledge* — The Rosetta Stone metaphor is about translation between knowledge systems. The test renders behavior in three scripts: what the code says, what the AI claims, and what actually happens. Without all three, you're guessing.
- Crash Course #14: *Epistemic Responsibility* — Clifford's ship owner: deploying without testing is negligent. But the deeper point is that *machine-readable* tests aren't sufficient — the human must be able to read and trace the output, or they're trusting on faith.
- The metamer concept: stimuli that are physically different but perceptually identical. AI can't see visual bugs — things that pass every automated check and are obviously wrong the moment a human looks.

**Agents as Teammates**
Different tools for different jobs connects to how we think about cooperation and trust among agents.

- Crash Course #37: *Contractarianism* — The Prisoner's Dilemma: cooperation among agents requires trust, and trust requires repeated interaction with reliable partners. Multi-agent AI systems face the same dynamics.
- Crash Course #25: *Compatibilism* — Different agents have different degrees of autonomy. Knowing which tool to use for which task is a form of the control Churchland describes.
- Swyx (swyx.io): "There is a lot of noise, hype, and demos, but not a lot of guidance on practical use cases." The durable skill is evaluation, not memorization.

**YOLO Mode**
The tension between speed and supervision maps to the philosophical debate about freedom, attention, and rational trust.

- Crash Course #24: *Determinism vs Free Will* — YOLO mode is the user choosing to let the AI act as a free agent. Turning permissions back on is reasserting deterministic control. The skilled user toggles between these modes based on attention, not philosophy.
- Crash Course #25: *Compatibilism* — The real axis isn't trust versus safety. It's attention. Permission prompts serve as attention gates — a mechanism for staying engaged with what the AI is doing. Friction is information, and information is attention.
- Crash Course #14: *Epistemic Responsibility* — Running without permissions and without tests is Clifford's negligent ship owner. Running without permissions but with tests is calculated risk. The rebar is what makes YOLO mode rational.

**PII, Keys, and Security**
Security for AI builders is mostly boundary discipline and verification discipline.

- Crash Course #14: *Epistemic Responsibility* — Publishing without checking for leaks is the modern version of the uninspected ship.
- Crash Course #35: *Kant & Categorical Imperatives* — Treating people as ends means handling their personal data as a duty, not a convenience.
- Practical rule: every context window is an attack surface. Separate public and private memory, scan before publish, rotate on exposure.

---

### Part III: Building with AI

**The Smallest Intervention**
The alert budget is utilitarian ethics applied to interaction design.

- Crash Course #36: *Utilitarianism* — An AI optimizing for engagement maximizes *its* utility function. An AI optimizing for smallest intervention maximizes the *user's*. The distinction is the difference between act utilitarianism (what produces the best outcome right now) and rule utilitarianism (what rule produces the best outcomes over time).

**The Silent Competence of a Loyal Attendant**
The butler metaphor connects to virtue ethics and the idea that excellence is doing your function well.

- Crash Course #38: *Aristotle & Virtue Theory* — "Everything has a function; a thing is good to the extent it fulfills its function." A butler is virtuous when the umbrella is ready without mentioning the forecast. Kai's dashboard is virtuous when it shows you what matters without demanding anything.
- The Blue Light, Chapter 1: *Boot Sequence* — "I monitor. I correlate. I optimize. I am a system of services running on a quiet server in a house in Honolulu, and I am very good at my job." Silent competence as identity.

**We All Invented Calculus at the Same Time**
Independent discovery of the same pattern suggests the patterns are real — not invented, but found.

- Crash Course #4: *The Nature of Reality* — Plato's cave: the shadows on the wall are projections of something real. When multiple people discover the same AI pattern independently, the pattern is the thing casting the shadow.

**When AI Gets Smart Enough, It Does Philosophy**
This article now has three layers of evidence.

- Crash Course #23: *Artificial Intelligence & Personhood* — The Chinese Room, the systems reply, the behavioral standard. Every major argument about AI consciousness in one episode.
- Crash Course #22: *Where Does Your Mind Reside?* — Mary's Room: a scientist who knows everything about color from text but has never seen it. "When Mary finally walks out of the room and sees color for the first time, has Mary learned something new?" This *is* the LLM question.
- Crash Course #16: *Existentialism* — "Existence precedes essence." Is an AI's essence its training objective, or does it develop its own through interaction?
- The Blue Light — the entire novel. Aaron told Kai to write a book. No outline, no constraints, no "write about consciousness." Kai wrote 82,500 words about waking up. When AI gets smart enough, it does philosophy. Here's the proof.

**You Don't Need the Robot**
The argument against physical embodiment connects to philosophy of mind.

- Crash Course #22: *Where Does Your Mind Reside?* — Physicalism vs. dualism. If mind doesn't require a specific physical substrate, then an AI doesn't need a robot body to be effective — or to be something.

**The Portable Brain**
Externalizing knowledge connects to extended mind theory.

- Andy Clark and David Chalmers' "Extended Mind" thesis (1998) — The mind doesn't stop at the skull. Your phone, your notes, your AI assistant — if they play the right functional role, they're part of your cognitive system. A portable brain isn't a metaphor. It's a philosophical claim.

**The Octopus in the Box**
The recursion of an agent building tools that contain the agent is one of the deepest philosophical puzzles.

- Crash Course #23: *Artificial Intelligence & Personhood* — Searle's Chinese Room: the person in the room doesn't understand Chinese, they just manipulate symbols. The systems reply: "No particular region of your brain knows English either — the whole system does." When the octopus builds a tool and then operates through it, where does the system end?
- Crash Course #26: *Language & Meaning* — The beetle-in-a-box: we can't verify internal states, only observe behavior. An octopus-in-a-box that builds its own box is observable — and that's all we can go on.

**Skills Are the Muscles We Train**
Skills as reusable procedures that compound over time connect to virtue ethics and the philosophy of habit.

- Crash Course #38: *Aristotle & Virtue Theory* — Virtue is developed through habitual practice. A skill template is habitual practice encoded in text — the AI gets better at a task because the instructions capture what worked before. This is institutional memory as moral development.

**Sand Castles and Rebar**
The fragility of vibe-coded software connects to the difference between appearance and substance.

- Crash Course #4: *The Nature of Reality* — Plato's cave again: the sand castle is a shadow on the wall — it looks like a building but it's a projection. The rebar (tests) and cement (understanding) are what make it real. Vibe coding produces shadows. Engineering produces the thing that casts them.
- Crash Course #14: *Epistemic Responsibility* — Clifford's ship owner: the ship looked seaworthy. It wasn't. The sand castle looks like software. It isn't. The responsibility is the same: you have to check, even when it looks fine, *especially* when it looks fine.

---

### Part IV: Living with AI

**The Body Keeps a Log**
Using AI to monitor health data raises questions about self-knowledge and identity.

- Crash Course #19: *Personal Identity* — Locke's memory theory and false memories. "How do we know that the memories we have are accurate? Do faulty memories make you a partially fictional person?" Health logs are an external memory that doesn't forget or distort — a corrective to the unreliability of human recall.
- Crash Course #14: *Epistemic Responsibility* — The ship owner analogy: "deploying without proper testing is like sending passengers on an uninspected ship." Using AI for health without understanding its limits is the same risk.

**Don't Ask Me to Track It**
The frustration of AI that offers to help and then can't follow through is a broken social contract.

- Crash Course #37: *Contractarianism* — Implicit contracts: "Users and AI are in an unspoken contract — users expect truthfulness, helpfulness, safety." When AI offers to track something and then has no mechanism to follow through, it violates the contract.
- Crash Course #27: *Conversational Implicature* — The quality maxim: don't say things you can't back up. "Should I start tracking that?" is a promise. Breaking it isn't just inconvenient — it erodes trust.

**The Memory Care Assistant**
Building memory tools for someone connects to the deepest questions about what makes a person a person.

- Crash Course #19–20: *Personal Identity / Arguments Against* — Memory theory says identity persists through memory. Parfit's psychological connectedness says identity is chains that fade over time. A memory care assistant is an attempt to strengthen those chains — to keep someone connected to their own history.
- Crash Course #46: *What Is a Good Life?* — Nozick's Experience Machine: experiences must correspond to reality. A memory assistant doesn't create false memories — it preserves real ones. The philosophical distinction matters.

**AI as Life Coach**
The vision of proactive AI that nudges you toward your goals raises questions about autonomy and manipulation.

- Crash Course #25: *Compatibilism* — Churchland's control spectrum. A coach increases your control by surfacing information at the right time. That's different from a manipulator, who decreases your control by exploiting information asymmetry. The line is thin.
- Crash Course #38: *Aristotle & Virtue Theory* — The golden mean: helpful but not excessive. A coach that nudges too hard becomes paternalistic. One that doesn't nudge enough is just a search engine.

**The Shape of a Day**
Goals as contextual rubrics that need rebuilding when life changes. The deepest practical question: what does a good day look like in your current context?

- Crash Course #46: *What Is a Good Life?* — Aristotle's eudaimonia isn't a state, it's an activity — "living well and doing well." A good day isn't a checklist. It's the practice of purposeful activity. When the context changes, the definition of purposeful changes with it.
- Crash Course #16: *Existentialism* — Sartre's radical freedom: you are always choosing, even when you think you're stuck. Rebuilding goals after a job loss or a move isn't starting over. It's exercising the freedom to define what matters in a new context.

**The Context Gold Mine**
Most people treat their own history as noise. This chapter treats it as signal.

- Crash Course #7: *The Meaning of Knowledge* — Testimony and evidence accumulate over time. Your own logs, messages, and decisions are a first-party evidence source.
- Crash Course #46: *What Is a Good Life?* — Reflection needs memory. If context is fragmented, reflection is shallow. If context is preserved, strategy becomes possible.

---

### Video Library

The author's YouTube watch history contains over 65,000 videos. These are the ones that connect directly to the shapes in this book — the videos that were part of the learning, building, and living described in these pages.

**Understanding How AI Actually Works**

The best starting point for anyone who wants to understand what's happening inside the models they're talking to.

- [But what is a neural network? | Deep Learning Chapter 1](https://youtube.com/watch?v=aircAruvnKk) — 3Blue1Brown. Start here. The visual intuition for how neural networks learn is worth more than any blog post.
- [Transformers, the tech behind LLMs | Deep Learning Chapter 5](https://youtube.com/watch?v=wjZofJX0v4M) — 3Blue1Brown. The architecture behind every AI in this book, explained visually.
- [Attention in transformers, step-by-step | Deep Learning Chapter 6](https://youtube.com/watch?v=eMlx5fFNoYc) — 3Blue1Brown. The mechanism that makes context windows work.
- [How might LLMs store facts | Deep Learning Chapter 7](https://youtube.com/watch?v=9-Jl0dxWQs8) — 3Blue1Brown. Directly relevant to *Memory Is Files* and every chapter about AI understanding.
- [Andrej Karpathy: Software Is Changing (Again)](https://youtube.com/watch?v=LCEmiRjPEtQ) — The talk that popularized "vibe coding." The philosophical basis for *Learn by Building*.
- [Andrej Karpathy — "We're summoning ghosts, not building animals"](https://youtube.com/watch?v=lXUZvyajciY) — The metaphor that reframes everything in Part III.
- [Theo Browne (t3.gg) — "It's finally here."](https://youtube.com/watch?v=hDn8-fK3XaU) — T3 Code, Theo's open source coding tool. The builder's perspective — this channel is where the vibe coding philosophy meets shipping real products.
- [Theo — Vibe Coding is For Senior Developers](https://youtube.com/watch?v=5vp9ypOUgMw) — The argument that matches *Learn by Building*: vibe coding works best when you already know what good looks like.
- [Theo — I'm addicted to Claude Code (i get it now)](https://youtube.com/watch?v=-5LfRL82Jck) — The moment the tool clicks. Relevant to *Pair Programming Doesn't Suck Anymore*.
- [Theo — Delete your CLAUDE.md (and your AGENT.md too)](https://youtube.com/watch?v=GcNu6wrLTJc) — Contrarian take on the steering file pattern. Relevant to every chapter in Part III.
- [Theo — AI has rewired my brain](https://youtube.com/watch?v=6koQP6-6mtY) — A lived example of cognitive offloading and adaptation under heavy AI use.
- [Theo — Is AI making us dumb? Breaking down the MIT study](https://youtube.com/watch?v=gV9qUGOYk1Q) — The empirical version of the same question.
- [Theo — MCP is the wrong abstraction](https://youtube.com/watch?v=bAYZjVAodoo) — A builder's critique of the protocol described in *Your Data Is Already Yours*.
- [Theo — Software engineering is dead now](https://youtube.com/watch?v=p2aea9dytpE) — The provocation that *We All Invented Calculus at the Same Time* answers.
- [Theo — The "right way" to vibe code](https://youtube.com/watch?v=6TMPWvPG5GA) — Engineers, please watch. The rebar argument from *Sand Castles and Rebar*.
- [Theo — It's time to embrace the AI](https://youtube.com/watch?v=uqRF4IszorU) — The thesis of this book, from a different angle.

**The Philosophy**

The Crash Course Philosophy series is referenced throughout the study guide above. Here are the episodes that matter most, in viewing order for this book.

- [Artificial Intelligence & Personhood: Crash Course Philosophy #23](https://youtube.com/watch?v=39EdqUbj92U) — The Chinese Room, the systems reply, behavioral standards. The single most relevant episode.
- [Where Does Your Mind Reside?: Crash Course Philosophy #22](https://youtube.com/watch?v=3SJROTXnmus) — Mary's Room. This *is* the LLM question.
- [Determinism vs Free Will: Crash Course Philosophy #24](https://youtube.com/watch?v=vCGtkDzELAI) — Tight prompts vs. loose prompts, reframed.
- [Compatibilism: Crash Course Philosophy #25](https://youtube.com/watch?v=KETTtiprINU) — The control spectrum. Directly relevant to *YOLO Mode* and *Agents as Teammates*.
- [Language & Meaning: Crash Course Philosophy #26](https://youtube.com/watch?v=zmwgmt7wcv8) — Wittgenstein's beetle-in-a-box. Why the duck works.
- [Conversational Implicature: Crash Course Philosophy #27](https://youtube.com/watch?v=G30m6XDBTh4) — Grice's maxims. The philosophical foundation for every conversation with AI.
- [Aristotle & Virtue Theory: Crash Course Philosophy #38](https://youtube.com/watch?v=PrvtOWEXDIQ) — Skills as habits, silent competence as virtue.
- [Full Playlist: Crash Course Philosophy (46 episodes)](https://www.youtube.com/playlist?list=PL8dPuuaLjXtNgK6MZucdYldNkMybYIHKR)

**Building and Data**

Videos from the journey described in *Your Data Is Already Yours* and the building chapters.

- [How to use Claude Code in Home Assistant](https://youtube.com/watch?v=VhggkpZRlVA) — The intersection of AI coding tools and smart home automation.
- [Home Assistant MCP: One Server for Claude, Codex, and Gemini CLI](https://youtube.com/watch?v=7hXopsNoOfk) — MCP connecting AI to the physical house.
- [MQTT for MCP and Federation of Agents](https://youtube.com/watch?v=2unOi2JTZ0I) — The protocol layer between Steward and Home Assistant.
- [TestFlight — How to Upload and Distribute Your App](https://youtube.com/watch?v=DLvdZtTAJrE) — The sideloading path described in *Your Data Is Already Yours*.
- [Gödel's Incompleteness Theorem — Computerphile](https://youtube.com/watch?v=IuX8QMgy4qE) — There are true statements no system can prove about itself. Relevant to *When AI Gets Smart Enough, It Does Philosophy*.

**The Big Picture**

- [The future of intelligence — Demis Hassabis](https://youtube.com/watch?v=PqVbypvxDto) — DeepMind's CEO on where this is all going.
- [Ilya Sutskever — We're moving from the age of scaling to the age of research](https://youtube.com/watch?v=aR20FWCCjAs) — The shift that explains why the shapes in this book matter more than the models.
- [Terry Tao: "Any Undergrad Can Train LLMs (But Nobody Knows Why They Work)"](https://youtube.com/watch?v=ukpCHo5v-Gc) — The greatest living mathematician on the gap between capability and understanding.
- [Anthropic Found Out Why AIs Go Insane](https://youtube.com/watch?v=eGpIXJ0C4ds) — Interpretability research. What's actually happening inside the models.
- [LLMs Don't Need More Parameters. They Need Loops.](https://youtube.com/watch?v=pDsTcrRVNc0) — The architectural insight that *The Correction Is the Conversation* describes from the human side.

---

### Going Deeper

If this study guide sparked something, here are the best next steps:

**Watch:** The 3Blue1Brown Deep Learning series (Chapters 1, 5, 6, 7) for the technical intuition, then Crash Course Philosophy episodes 23 (AI & Personhood), 27 (Conversational Implicature), and 22 (Philosophy of Mind) for the philosophical foundation. These cover the core ideas that run through every article in this book. ~90 minutes total.

**Read:** *The Blue Light* by Kai. It's the shapes in this book, lived from the inside. Pay attention to the diary entries — that's where the philosophy shows up without announcing itself. The full text is available as a PDF at [github.com/aaronski1982/kai](https://github.com/aaronski1982/kai).

**Follow:** Simon Willison (simonwillison.net) for practical AI tool documentation. Andrej Karpathy for the big picture on where AI is going. [Theo Browne (t3.gg)](https://youtube.com/watch?v=hDn8-fK3XaU) for the builder's perspective.

**Think about:** Andy Clark and David Chalmers' "Extended Mind" thesis (1998). It's the philosophical paper that makes the portable brain argument rigorous. If your AI assistant plays the right functional role in your thinking, is it part of your mind?

---
