## The Steering File

Every AI tool reads a set of instructions before it reads your prompt. The instructions tell it who it is, what it can do, what it shouldn't do, and how to behave. Most people never touch these files. The tools ship with defaults, and the defaults work well enough that it never occurs to anyone to change them.

The steering file is where you change them.

Different tools call it different things. Claude Code uses `CLAUDE.md`. Cursor uses `.cursorrules`. Codex uses `AGENTS.md`. The format varies but the function is the same: a text file that sits in your project directory and gets injected into every conversation the AI has about that project. Whatever you write in that file becomes part of the AI's context before you say a word.

The simplest steering file is one line. "Don't use /tmp." That's a real one. It exists because the AI kept dumping temporary files in a system directory, and the fix wasn't to correct it every time — the fix was to write the instruction once and never think about it again. One line, permanent behavior change. Every conversation in that project now respects the constraint without being asked.

The shape: a steering file is a conversation you have once that applies to every conversation after.

From there, it scales. A steering file for a home automation agent describes the house — which services run on which ports, how to restart them, where the logs live, what the TLS certificates are for. A steering file for a personal assistant describes the person — timezone, preferences, health tracking habits, what "good biking weather" means in specific numbers (no rain, wind under fifteen miles per hour, temperature between forty-five and eighty-five degrees). A steering file for a coding project describes the architecture — directory structure, build commands, which service runs on the host and which runs in containers, what to do when a package fails to build.

The more specific the steering file, the less you repeat yourself. Without one, every new conversation starts from zero. You explain the project structure, the preferences, the constraints, the things that went wrong last time. With a steering file, the AI arrives already briefed. It knows the codebase layout. It knows your naming conventions. It knows that you prefer fixing root causes over adding fallback paths. It knows that voice responses need to be under eighty characters because the text-to-speech engine is slow. All of this is context you'd otherwise burn conversation time re-establishing.

The best steering files evolve. They start small — a few preferences, a few constraints. Then something goes wrong and you add a line. The AI keeps making the same mistake, so you add a section explaining why it's wrong and what to do instead. A new service gets added to the project, so the port table gets updated. Over months, the steering file becomes a living document that captures everything you've learned about working with the AI on this specific project. It's institutional memory for a team of one.

There's also a self-knowledge benefit. Writing a steering file forces you to articulate things you know implicitly. You know your project's directory structure — but can you describe it clearly enough that a new team member would understand it in thirty seconds? You know your preferences — but have you ever written them down? The steering file is an exercise in making tacit knowledge explicit, and the process of writing it often reveals assumptions you didn't know you were making.

The daily maintenance pattern takes this further. Some steering files are auto-generated — rebuilt every night by a scheduled task that checks the current state of the system and updates the instructions accordingly. Which skills are available? Which services are running? What happened yesterday that the AI should know about today? The steering file becomes a daily briefing, not just a static document. The AI wakes up every morning with fresh context.

Most people will never write one. They'll use the AI with whatever defaults the tool provides, and it will be fine. But the gap between "fine" and "this thing knows exactly how I work" is a steering file. It's the difference between a new hire and a colleague who's been on the project for a year. The colleague doesn't need to be told where the logs are. They already know. That knowledge lives in a file you wrote once and update when things change.

Write the file. Update it when something goes wrong. Let it grow. The AI reads it every time, and every time, it starts a little closer to where you need it.

---
