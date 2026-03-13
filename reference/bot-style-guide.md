---
title: Bot Style Guide
summary: How to write pages that keep their voice for humans while staying easy for agents to parse, summarize, and act on.
platforms: []
---

This site has two jobs at once:

1. A human should be able to read it and feel a point of view.
2. An agent should be able to read it and recover the structure without guessing.

The mistake is to pick one. The better pattern is: **voice in the body, structure at the edges.**

## The main rule

Do not flatten a distinctive page into SEO paste just to make it machine-readable.

Instead:

- Put the page's clearest one-sentence promise near the top.
- Add a short visible summary block that says what the page is, what it is not, and where to go next.
- Keep the expressive writing in the body.

That preserves the reason a human would care while giving an agent a stable spine to hold onto.

## For overview pages

Overview pages are for orientation, not execution. They should answer:

- What is this page for?
- What are the 2-4 strongest claims?
- What are the best next links?

Use a visible summary block near the top. Prefer plain language over clever labels. If the body is stylized, the summary should be the straight version.

## For guide pages

Guide pages tell an agent what to do. They need tighter structure:

- State the goal before the steps.
- Use clear stages with approval gates.
- Tell the agent what files to read or write.
- Tell the agent what to verify before moving on.
- Make refusals and trust boundaries explicit.

If the page contains agent instructions, they should be visible in the page. Hidden comments are acceptable as a mirror, not as the only place the instructions live.

## What agents struggle with

These are the patterns that make pages harder to read with `rg`, extract, or summarize:

- Large inline CSS blocks before the content
- Relative links that change meaning depending on the entry path
- Numbered or opaque URLs that require out-of-band knowledge
- Critical instructions hidden only in HTML comments
- Pages that do not say whether they are an essay, a guide, a checklist, or a landing page
- "Start here" pages with no explicit next step

## Good defaults

- Extract shared CSS so the HTML is mostly structure and words.
- Use stable, guessable URLs.
- Prefer visible summaries over hidden prompt tricks.
- Put the important nouns in headings and links.
- Make the next click obvious.
- If a page is not executable, say so.

## A good page skeleton

For a public page on this site, the default shape is:

1. Title
2. One-sentence promise
3. Visible summary or handoff block
4. Main body
5. Related links / next steps

That is enough for both a human skim and an agent skim.

## Trust model

Telling an agent to read a page is close to giving it code.

That means:

- The visible page should be enough to understand what the agent is being asked to do.
- The page should not depend on hidden instructions to be safe.
- The more executable the page is, the more explicit the trust boundary should be.

## The standard

A page passes if:

- A human can skim the top and know what it is.
- An agent can summarize the page without inventing the point.
- The next step is obvious.
- The voice survives.
