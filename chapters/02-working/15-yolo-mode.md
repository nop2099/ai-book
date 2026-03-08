## YOLO Mode

Every AI coding tool has a version of this flag. Claude Code calls it `--dangerously-skip-permissions`. OpenAI's Codex makes it the default and buries the alternative. The flag says: stop asking me. Just do it. Don't confirm file writes, don't check before running commands, don't interrupt the flow with permission dialogs. Trust the machine and let it work.

Everyone turns it on. Almost immediately. And honestly — it's the right move most of the time. The friction is maddening. You're in a flow state, the AI is generating code, and every thirty seconds it stops to ask "may I write to this file?" Yes. Obviously yes. You asked it to build the thing. Of course it needs to write to the file. After the tenth confirmation, you find the flag that skips them all, and the relief is immediate. The AI moves at full speed. You move at full speed. Everything feels faster, smoother, better.

Here's what nobody tells you: the interesting part isn't turning it on. It's learning when to turn it off.

An experienced user lives in YOLO mode by default. The Bayesian prior is high. The AI has proven itself over hundreds of sessions. The rebar is in place — tests exist, version control exists, the damage from any single mistake is bounded. Skipping permissions in this context isn't reckless. It's earned. The prior didn't start at 1.0. It arrived there through evidence.

But sometimes you deliberately turn the permissions back on. Not from distrust. Because you want to watch. The permission prompts become an attention gate — a reason to stay in the loop, to see each action before it happens, to think about whether this is what you wanted. When the work is interesting enough, or risky enough, or unfamiliar enough, the interruption isn't friction. It's focus. You're using the tool's safety mechanism as a concentration aid. The prompt that says "may I write to this file?" is also saying "hey, look at what happens next."

This reframes the whole debate. The industry argument is YOLO versus guardrails, speed versus safety, trust versus verification. But that's the wrong axis. The real axis is attention. Sometimes you want your attention elsewhere — on the big picture, on the next feature, on the coffee that's getting cold. YOLO mode frees your attention. Sometimes you want your attention right here — on this specific change, this specific file, this specific decision the AI is about to make. Permission mode focuses your attention. The skilled user toggles between them based on what the work demands, not based on a philosophical position about trust.

The mistake beginners make is turning YOLO on before they've built the infrastructure that makes it safe. No tests, no version control, no habit of checking diffs. In that context, YOLO mode is genuinely dangerous — not because the AI is untrustworthy, but because there's no backstop when it makes a mistake. The damage is unbounded. A file overwritten, a config changed, a dependency installed that breaks something else. Without rebar, the sand castle collapses silently.

The mistake the industry makes is treating YOLO as the default. Codex and similar tools optimize for first impressions — maximum speed, minimum friction, no interruptions. That's great for demos. It's terrible for building anything you plan to keep. The `--dangerously-skip-permissions` flag has the right name. The "dangerously" is honest. It tells you exactly what you're giving up. Making maximum trust the factory setting, with no honesty about the cost, is a car that ships with the seatbelt alarm disabled because customers complained about the beeping.

The shape: friction is information, and information is attention. Every permission request is a moment where you see what the AI intends to do before it does it. Removing that friction removes the information. Adding it back gives you a reason to look. The question isn't whether to use YOLO mode. You will. The question is whether you know why you're toggling it, and whether the rebar is in place for the times when you're not watching.

---
