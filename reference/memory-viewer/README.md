# Memory Viewer

A static prototype of the Octopus foveated memory system's visual frontend.

## What is this?

The Memory Viewer is a single-page dashboard that visualizes memories organized by facets (entity, source, topic, detail level) and projects a "chalkboard" — a summary of current world state synthesized from all memories.

This serves as both a working prototype and a reference example for the *Shapes of Intelligence* companion site.

## How to run

Open `index.html` directly, or serve it locally (needed for JSON fetch):

```
cd reference/memory-viewer
python3 -m http.server 8080
# open http://localhost:8080
```

## Features

- **Chalkboard panel** — current-state projection rendered from memory
- **Entity sidebar** — filter by people, projects, tools
- **Source sidebar** — filter by data source (claude, chatgpt, kai-diary, apple-health)
- **LOD toggle** — switch detail level 0 (headlines) through 3 (full detail)
- **Search** — client-side text filtering across content and tags
- **Timeline** — reverse-chronological memory cards with source badges and entity/topic tags

## How it connects to Octopus

The sample data mirrors the Octopus API shape (`POST /memories` payload). In a connected version:

- `GET /memories?entity=X&lod=N` would replace the static JSON
- `GET /chalkboard` would supply the chalkboard panel
- `POST /chalkboard/rebuild` would let the user re-focus the projection
- An agentic librarian chat interface would sit alongside the viewer

## Next steps

1. Connect to the real Octopus API (Bun + Hono + SQLite backend)
2. Add the agentic librarian — a chat panel that can query and annotate memories
3. Chalkboard diff view (compare versions side by side)
4. Memory ingestion UI — paste a conversation or note, have it faceted automatically
5. Graph view — entity relationship visualization
