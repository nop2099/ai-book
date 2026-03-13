---
name: slush
description: Add an idea to the slush pile, or review and triage existing entries. Also known as: backlog, icebox, someday-maybe, parking lot, idea bin, seed bank, compost heap, wish list, junk drawer.
---

# Slush

The slush pile is where ideas live before they're ready. Every project has one. The shape has many names — each implies a different relationship to urgency and decay, but the underlying pattern is always the same: low-friction capture, no commitment to act, graduation when ready.

1. **Backlog** — scrum/agile standard. Implies a queue with priority.
2. **Slush pile** — publishing term. Unsolicited manuscripts piled on the editor's desk.
3. **Icebox** — frozen backlog. Explicitly not now, but don't lose it.
4. **Parking lot** — meeting facilitation. "Great point, let's park that."
5. **Someday/maybe** — GTD term. David Allen's bucket for things not actionable now.
6. **Seed bank** — seeds stored for planting later, under the right conditions.
7. **Compost heap** — ideas decompose and recombine. Some become soil. Some rot. That's fine.
8. **Idea bin** — no metaphor, no pretension. It's a bin.
9. **Wish list** — things you want but haven't committed to building.
10. **Junk drawer** — batteries, tape, keys to unknown locks, and a menu from 2019.

## Adding an entry

When the user says "slush this," "add to slush," "park this idea," or anything that smells like "I want to remember this but not do it now":

1. **Identify which slush pile.** This project has two:
   - **Book slush**: `reference/_meta/static/slush-pile.html` — ideas for the book, reference pages, and site. These are HTML note cards.
   - **Wall slush**: `~/w9/wall/slush.md` — ideas for the wall of data infrastructure. These are markdown sections.

2. **Write the entry.** Each entry needs:
   - A short, specific title (not "misc idea")
   - The observation or idea in 1-3 paragraphs
   - Why it matters or what it connects to
   - Open questions if any

3. **Don't over-polish.** Slush entries are raw thinking. They graduate into chapters, reference pages, or tasks when they're ready. The slush pile is not the place to write the final version.

4. **Check for duplicates.** Read the existing slush pile first. If the idea is already there, update the existing entry instead of adding a new one.

## For the book slush (HTML)

Add a new `<div class="note">` block in the appropriate section (Notes & Patterns, Slush Pitches, or Open Threads). Follow the existing card format:

```html
<div class="note">
  <div class="note-title">Title here</div>
  <p>First paragraph.</p>
  <p>Second paragraph if needed.</p>
</div>
```

## For the wall slush (markdown)

Add a new `##` section. Follow the existing format:

```markdown
## Title Here

**Noticed**: YYYY-MM-DD. What you observed.

**Idea**: What to do about it.

**Open questions:**
- Question one
- Question two
```

## Graduating entries

When a slush entry has been fully covered by a published page, chapter, or reference guide:

1. Move the entry to `reference/_meta/static/slush-archive.html`
2. Add a note saying where it graduated to, with a link
3. Remove it from the active slush pile
4. Update the slush pile's agentic summary if the graduation changes the overall picture

## Reviewing the slush pile

When asked to review or triage the slush:

1. Read both slush piles
2. Flag entries that have already been covered by published content (candidates for archive)
3. Flag entries that connect to current work (candidates for promotion)
4. Flag entries that are stale or no longer relevant (candidates for removal)
5. Update the agentic summary at the top of each page
