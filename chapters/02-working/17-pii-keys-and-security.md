## PII, Keys, and Security

The fastest way to lose trust in AI is one accidental paste.

PII means **Personally Identifiable Information**: data that can identify a person directly or indirectly.
Direct examples: full name, email address, phone number, street address, SSN.
Indirect examples: employer plus city plus unique medical details, account handles, or combinations of facts that point to one specific person.

When you build with agents, context is power. It's also liability. The same corpus that helps an AI solve your problems can contain your email history, health notes, phone numbers, API keys, auth tokens, and private conversations. If you hand all of that to a model without boundaries, you are one copy-paste away from a leak.

The shape is simple: **every useful context window is also an attack surface**.

This isn't hypothetical. Before checking in changes on this book, I ran a PII and secret scan across the publish surface. Most of what looked risky was intentional disclosure in the narrative. But that pass is the point: you verify before publish, not after regret.

A practical security loop looks like this:

1. Separate raw archives from publishable content.
2. Give agents least privilege by default (directory, tool, and token scope).
3. Run two scans before commit: pattern scan and known-entity scan.
4. Treat every found credential as compromised until rotated.
5. Redact by policy, not by vibe.
6. Keep a public memory and a private memory. Never mix them casually.

That third step matters more than it looks.

Pattern scans catch structure: emails, phone numbers, SSNs, key formats.
Known-entity scans catch context: your name, family names, city, employer, account handles, project codenames.

If you only run regex, you miss identity leaks that don't look like classic PII.
If you only run keyword scans, you miss secret formats and accidental credentials.
You need both.

Here is the grounded version from Kaijuu:

- On **January 31, 2026**, memory CRUD and search routes existed and could store arbitrary content. That's normal; storage layers are usually dumb.
- On **February 1, 2026** (`e89068f`), Subconscious added outbound secret detection, PII redaction, and stream filtering as a central boundary.
- On **February 3, 2026** (`cac67c6`), memory search added text-query fallback. Great for usability, but it also increases the chance of pulling sensitive records unless filtering is solid.
- On **February 4, 2026** (`9137253`), tool execution was routed through Subconscious and a `tool_result` bypass was fixed so results stopped slipping through unfiltered.
- On **February 5, 2026** (`de73420`, `7a987b5`), model-tier permission caps/timeouts were added and handbook dossiers/locations moved to graph-backed data, increasing the need for strict boundaries around personal context.

One more practical lesson from that code: there is a global whitelist helper in `PIIRedactor`, but helper methods do nothing unless runtime actually calls them. Security features you "have" and security features you "execute" are not the same thing.

For keys specifically, the rule is strict: if a key ever lands in a chat log, commit, screenshot, or paste buffer outside your intended boundary, rotate it. Immediately.

For personal data, distinguish intentional from accidental disclosure. "I chose to share this" is not the same thing as "I forgot this was in the context window." That distinction is the whole game.

AI makes it easy to move fast. Security is how you keep speed from becoming fallout.

---
