# Episode: I Want a Podcast — Part Five: How It Was Made

The making-of and the TOGAF postscript. How one conversation became a curriculum, and what a senior architect sees when he looks at what Rich built. Dry mix.

## Voice Design Notes

### Cast

| Tag | Voice | Draft Voice | Why |
|---|---|---|---|
| JAMES | James Wilson (clone) | Daniel | Author. The making-of is James's voice. |
| RICH | — | Rishi | Returns for TOGAF bullets. |
| OCTOPUS | — | Tessa | Returns for TOGAF bullets. |
| CRAB | — | Moira | Returns for TOGAF bullets. |
| STAGE | Samantha | Samantha | Transitions. |

### Assembly overrides

- **Dry mix.** No effects.

## Script

> **Cold open**: Prepend `cold-open.md` before this script.

[JAMES]
This is I Want a Podcast, part five — how it was made. In parts one through four, Rich built a podcast, secured it, extended it, and explored extra credit. This part is the process behind the process. Here we go.

---
[STAGE]
And now, how this episode was made.

[JAMES]
I want to tell you how this episode got built, because the process is the point.

[JAMES]
A few days ago, I opened Claude Code in an empty folder and typed six words: "I want to make a podcast." No context. No steering file. No instructions. The agent started blind. It asked me questions. I answered. It suggested things. I corrected. It tried Ollama for the script — the output was garbage. It self-corrected and wrote the script itself. It tried macOS Samantha for the voice — I said "I hate that voice." It switched to Edge T-T-S. It served it locally — I said "I want it on my phone." It suggested hosting — I said "make it free." It put a password on it — I said "the filename is in the source." Six words to a working system in one conversation.

[JAMES]
That entire conversation was a blind taste test. I started the agent with no context and let the conversation reveal what I actually cared about. Every correction exposed a preference the agent couldn't have guessed. Free, not paid. Phone, not desktop. Secure, not just passworded. The corrections became a steering file. The steering file became a skill. The skill became repeatable — next time I say "make me a podcast" it already knows how.

[JAMES]
Then I looked at that conversation and thought: Rich could do this. Rich, who listened to my audiobook and wrote back saying "the correction being the conversation changed how I work today." Rich, who doesn't know what edge T-T-S is and doesn't need to. Rich, who has the instinct to push back — he challenged the AI to prove where it was getting information on day one.

[JAMES]
So I took my blind taste test — the raw, messy, unplanned conversation — and I refined it into this workbook. I gave the corrections a shape. I named the sip tests — those moments where you taste an option and react without knowing the menu. I added the parrot so people without a command line could see themselves in the story. I added the security thread as the spine because that's the one part nobody should skip. And I turned it into a podcast using the same pipeline I built during that blind taste test.

[JAMES]
The tool that made this episode is the tool the episode teaches you to build. That's the strange loop. The work is now part of the work.

[JAMES]
Even making this episode was a sip test. These voices are macOS text-to-speech. Daniel, Rishi, Tessa, Karen, Moira, Samantha, Fred. Free. Built into the operating system. I used to have voice cloning — a G.P.U. on a remote server, forty-five minutes per episode, voices that sounded like real people. I stopped using it. Not because it was bad. Because the built-in voices render in two minutes. I can listen, correct the script, re-render, listen again — ten iterations in the time one cloned episode takes. The "worse" voices produce better episodes because I can afford to keep tasting. Speed changes the process. Faster iteration means more corrections. More corrections means better output. The best voice is the one that lets you iterate. And some words sounded wrong. "Co-Work" came out as "cah-work." "f-f-mpeg" came out garbled. So I ran the audio through Whisper — that's a speech-to-text tool — to see what it heard. If Whisper can't understand the word, the listener won't either. Then the agent built me a pronunciation audition page — thirty-three audio samples, every problem word spelled three different ways, with a "pick" button next to each one. I listened. I clicked. I screenshotted the picks and sent them back. The agent read the screenshot, saw my choices, and updated the script. Co-Work with a hyphen. f-f-mpeg with dashes. A.E.S. with dots. H.T.M.L. with dots. But MP3 was fine as-is — Daniel says that one right.

[JAMES]
That's a sip test for pronunciation. Same pattern as the voice selection, same pattern as the security model. Taste, react, the system improves. The tool for making this episode used the same method this episode teaches.

[JAMES]
One more thing about the making. While building this episode, I needed a quote from a friend — Aaron fed my site to ChatGPT and ChatGPT said "that is one of the least stupid public explanations of agent safety I've seen." I knew the quote was in my text messages, archived on my wall. I asked the crab to find it. The crab hit the wall directory — outside its sandbox — and stopped. "I don't see a wall directory." I said "check permission." It tried again, failed again. I switched to the octopus. One grep command. Found it in seconds. The data was right there. The crab wasn't wrong that it couldn't see it. It was wrong to stop trying to help me see it. That's the crab's blind spot — it tells you what it can't do, not how to change what it can do. A wall is sometimes just a door you haven't opened yet.

[JAMES]
And then I had the octopus write a fix for the encryption, and it said "done, fixed, redeploying." I almost moved on. But then I thought — did it test it? Did it try the wrong password? Did it check the source? It hadn't. It assumed. So I said "prove it works." And it did — wrong password shows nothing, right password plays audio, source shows gibberish. Only then did I believe it. Most agents skip the test. The conductor's job is to say "play the passage again. Let me hear it."

[JAMES]
And then we fact-checked. I had the agent read both scripts and verify every claim — technical claims, quotes from real people, the timeline of how the original podcast conversation went. It found four things. I said "four words" when I actually typed six. I said "twenty minutes" when the conversation took two and a half hours. I said "no subscriptions" in the intro and then Rich says he has a Claude subscription two lines later. And a quote I attributed to Rich was paraphrased, not verbatim — he said "I suspect will change" and I wrote "changed." Four catches. All fixed. And the fact-check wasn't something I thought to do. It's built into the deploy skill — a checklist the agent runs before anything goes public. P-I-I scan, security review, link check, and fact-check. The agent won't publish until the checklist passes. I didn't have to remember to verify. The skill remembered for me. That's what a skill does — it encodes the lesson so you don't have to re-learn it every time.

[JAMES]
One more thing about the timeline. Every technology in this podcast is old. T-T-S has existed for decades. f-f-mpeg is from the year 2000. H.T.M.L. is from 1993. A.E.S. encryption is from 2001. Static web hosting has been free since the mid twenty-tens. None of the parts are new. What's new is who can assemble them.

[JAMES]
Five years ago — 2021 — a computer-savvy novice who wanted to go from zero to a podcast on their phone would need to learn a programming language, learn a web framework, learn command-line tools, learn how encryption works, learn how to deploy a website. Weeks of tutorials. Months to feel comfortable. The knowledge barrier was the bottleneck, not the technology.

[JAMES]
Two years ago — 2024 — ChatGPT existed. GPT-4 could write every line of code in this project. The parrot was smart. You could say "write me a podcast generator with encrypted filenames" and get working code in the chat window. But you still had to carry every file. Copy the code. Save it. Run it. Debug it by pasting errors back. Find hosting. Deploy manually. A weekend project for someone comfortable with a terminal. Still out of reach for someone who's never opened one.

[JAMES]
One year ago — 2025 — Claude Code launched. The octopus got arms. For the first time, the agent could touch your files, run your commands, and deploy your site. The same project went from a weekend to an evening. But you needed the C-L-I. You needed to be comfortable in a terminal.

[JAMES]
Today — the crab exists. Co-Work. Desktop app. Rich opens it in a folder, says "I want a podcast," and the crab writes the files, writes the scripts, connects to Gmail, schedules the task. Rich runs one command the crab wrote for him. The terminal is optional. The knowledge barrier dropped from "learn to code" to "learn to push back when something tastes wrong." The technology is thirty years old. The ability to assemble it with a conversation is six months old.

[JAMES]
Two patterns. The blind taste test — start with no context, let the corrections reveal what matters, capture them into a steering file. The sip test — taste options, react, the agent swaps the part. The blind taste test is the frame. The sip tests are the beats inside it. Together they turn a conversation into a system and a stranger into someone who can explain why their podcast is secure.

---

[STAGE]
No parrots, octopuses, crabs, or childhood dogs were harmed in this production. The sip test was conducted ethically. The encryption was real. The parrot would like you to know she can do everything the octopus can do — it just takes more trips. The crab would like you to know she can do ninety percent of what the octopus can do — she just can't reach the top shelf. Or the external drive.

[JAMES]
That's I Want a Podcast. Say it to whatever agent you have. Push back when something feels thin. Explain why it's secure when you're done. Teach someone else with one sentence.

[JAMES]
And if you like how Rich and I think about things, but your AI is a little different — show it this page. Ask it what it thinks. Then talk about your projects. Or just describe your understanding of the story to it and see what it says back. The page works both ways — human-readable and agent-parseable. Read the book and let's build.

---

[STAGE]
No pronunciation pages, fact-checkers, or blind taste tests were harmed in this production.

[JAMES]
That's part five — how it was made. In part six: what a senior enterprise architect sees when he looks at what Rich built. Thanks for listening.
