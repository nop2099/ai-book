---
title: Board Game
book_chapter: 03-building/07-correction
summary: The full lifecycle of turning a physical board game into a digital one — from rules to AI opponents to deployment.
platforms: [mac, windows, linux]
---

# Board Game

> Make a system that will learn, but don't make it guess — tell it what you know.

## What this shape is

You have a board game your family plays. You know the rules — maybe better than anyone, because your family has house rules the official rulebook doesn't cover. You want a digital version.

This is one of the best first projects because you are the domain expert. You know when the AI gets it wrong. You know the edge cases. You don't need to learn a new domain — you already have one.

What follows is the full lifecycle. You don't build all of this at once. Each stage is its own project, its own set of prompts, its own corrections. Start at Stage 1 and stop wherever you're satisfied.

---

## Quick start: prompt generator

Pick your options below — the prompt updates live. Hit "Roll d20" to randomize everything, or choose your own and copy.

Your choices determine the complexity. Multiplayer Settlers of Catan with expansions is bigger than Mille Bornes — you don't need a label to tell you that.

<div id="generator" style="background:#16213e;border:1px solid #30363d;border-radius:8px;padding:1.25rem;margin:1rem 0;">
<style>
  #generator select, #generator label {
    font-family: inherit; font-size: 0.88rem; color: #e0e0e0;
  }
  #generator select {
    background: #0d1117; border: 1px solid #30363d; color: #e0e0e0;
    padding: 0.35rem 0.5rem; border-radius: 4px; width: 100%; margin: 0.25rem 0 0.75rem;
  }
  #generator .field-label {
    color: #8888aa; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;
  }
  #generator .checkbox-group { margin: 0.25rem 0 0.75rem; }
  #generator .checkbox-group label {
    display: block; padding: 0.2rem 0; cursor: pointer; font-size: 0.85rem;
  }
  #generator .checkbox-group input { margin-right: 0.5rem; accent-color: #e94560; }
  #generator .game-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 0; margin: 0.25rem 0 0.5rem; }
  #generator .game-grid label {
    display: flex; align-items: center; padding: 0.25rem 0; cursor: pointer; font-size: 0.85rem;
  }
  #generator .game-grid input { margin-right: 0.4rem; accent-color: #e94560; }
  #generator .game-grid label.active { background: #1a2744; border-radius: 4px; }
  #generator details { margin: 0.25rem 0 0.75rem; }
  #generator summary {
    cursor: pointer; color: #8888aa; font-size: 0.78rem; text-transform: uppercase;
    letter-spacing: 0.05em; list-style: none; display: flex; align-items: center; gap: 0.4rem;
    user-select: none;
  }
  #generator summary::-webkit-details-marker { display: none; }
  #generator summary::before { content: '\25B8'; font-size: 0.7rem; transition: transform 0.15s; }
  #generator details[open] summary::before { transform: rotate(90deg); }
  #generator .game-name-input {
    background: #0d1117; border: 1px solid #30363d; color: #e0e0e0;
    padding: 0.35rem 0.5rem; border-radius: 4px; width: 100%; margin: 0.25rem 0 0.5rem;
    font-family: inherit; font-size: 0.88rem;
  }
  #generator .game-name-input::placeholder { color: #555; }
  #generator .btn-row { display: flex; gap: 0.75rem; margin: 1rem 0 0.5rem; }
  #generator button {
    font-family: inherit; font-size: 0.88rem; padding: 0.5rem 1rem;
    border-radius: 6px; cursor: pointer; border: none; letter-spacing: 0.02em;
  }
  #generator .btn-roll { background: #e94560; color: #fff; }
  #generator .btn-roll:hover { background: #d63851; }
  #generator .btn-build { background: #30363d; color: #e0e0e0; }
  #generator .btn-build:hover { background: #3d444d; }
  #generator .btn-copy { background: #0f3460; color: #58a6ff; }
  #generator .btn-copy:hover { background: #163d6f; }
  #generator .btn-copy.copied { color: #e94560; }
  #generator pre {
    margin: 0.75rem 0 0; white-space: pre-wrap; font-size: 0.82rem;
    background: #0d1117; border: 1px solid #30363d; border-radius: 6px;
    padding: 1rem; line-height: 1.5; position: relative;
  }
</style>

<div class="field-label">Game</div>
<input type="text" id="gen-game" class="game-name-input" placeholder="Type a game not in the list, or pick one below...">
<details>
  <summary>Games I know <span id="known-count" style="color:#e94560;font-size:0.75rem;"></span></summary>
  <p style="color:#8888aa;font-size:0.78rem;margin:0.4rem 0 0.5rem;">Check the ones you know — they're remembered. Click a name to build it.</p>
  <div class="game-grid" id="game-picker">
    <label><input type="checkbox" class="know-check" value="Cribbage"> Cribbage</label>
    <label><input type="checkbox" class="know-check" value="Hearts"> Hearts</label>
    <label><input type="checkbox" class="know-check" value="Bridge"> Bridge</label>
    <label><input type="checkbox" class="know-check" value="Spades"> Spades</label>
    <label><input type="checkbox" class="know-check" value="Gin Rummy"> Gin Rummy</label>
    <label><input type="checkbox" class="know-check" value="Uno"> Uno</label>
    <label><input type="checkbox" class="know-check" value="Dominoes"> Dominoes</label>
    <label><input type="checkbox" class="know-check" value="Mexican Train"> Mexican Train</label>
    <label><input type="checkbox" class="know-check" value="Scrabble"> Scrabble</label>
    <label><input type="checkbox" class="know-check" value="Mahjong"> Mahjong</label>
    <label><input type="checkbox" class="know-check" value="Chess"> Chess</label>
    <label><input type="checkbox" class="know-check" value="Checkers"> Checkers</label>
    <label><input type="checkbox" class="know-check" value="Othello"> Othello</label>
    <label><input type="checkbox" class="know-check" value="Connect Four"> Connect Four</label>
    <label><input type="checkbox" class="know-check" value="Backgammon"> Backgammon</label>
    <label><input type="checkbox" class="know-check" value="Mancala"> Mancala</label>
    <label><input type="checkbox" class="know-check" value="Yahtzee"> Yahtzee</label>
    <label><input type="checkbox" class="know-check" value="Liar's Dice"> Liar's Dice</label>
    <label><input type="checkbox" class="know-check" value="Battleship"> Battleship</label>
    <label><input type="checkbox" class="know-check" value="Boggle"> Boggle</label>
    <label><input type="checkbox" class="know-check" value="Mille Bornes"> Mille Bornes</label>
    <label><input type="checkbox" class="know-check" value="Settlers of Catan"> Settlers of Catan</label>
    <label><input type="checkbox" class="know-check" value="Ticket to Ride"> Ticket to Ride</label>
    <label><input type="checkbox" class="know-check" value="Carcassonne"> Carcassonne</label>
    <label><input type="checkbox" class="know-check" value="Risk"> Risk</label>
    <label><input type="checkbox" class="know-check" value="Clue"> Clue</label>
    <label><input type="checkbox" class="know-check" value="Monopoly"> Monopoly</label>
    <label><input type="checkbox" class="know-check" value="Sorry!"> Sorry!</label>
    <label><input type="checkbox" class="know-check" value="Sequence"> Sequence</label>
    <label><input type="checkbox" class="know-check" value="Codenames"> Codenames</label>
  </div>
</details>

<div class="field-label">Players</div>
<select id="gen-players">
  <option>Not sure yet (start with solo vs AI)</option>
  <option>Solo vs AI</option>
  <option>Hot seat (same device)</option>
  <option>Human + AI partner vs AI team</option>
  <option>2+ humans + AI fill</option>
  <option>Full multiplayer (networked)</option>
</select>

<div class="field-label">Devices</div>
<select id="gen-devices">
  <option>Not sure yet (start with desktop)</option>
  <option>Desktop</option>
  <option>Phone</option>
  <option>TV browser</option>
  <option>All devices</option>
</select>

<div class="field-label">Deploy</div>
<select id="gen-deploy">
  <option>Not sure yet (start local)</option>
  <option>Local only</option>
  <option>Static (GitHub Pages / Vercel / Netlify)</option>
  <option>Server (VPS / cloud)</option>
</select>

<details>
  <summary>Optional features</summary>
  <div class="checkbox-group">
    <label><input type="checkbox" id="opt-training"> Training mode (recommended plays + EV)</label>
    <label><input type="checkbox" id="opt-commentator"> Commentator (strategy narration panel)</label>
    <label><input type="checkbox" id="opt-opponent"> Opponent modeling (card counting / deduction)</label>
    <label><input type="checkbox" id="opt-visual"> Visual match (look like the real board)</label>
    <label><input type="checkbox" id="opt-variants"> Variant config (house rules, scoring modes)</label>
    <label><input type="checkbox" id="opt-step"> Step-through mode (click to advance AI turns)</label>
    <label><input type="checkbox" id="opt-explain"> Explain via a game I know</label>
  </div>
</details>

<div class="btn-row">
  <button class="btn-roll" id="gen-roll">Roll d20</button>
  <button class="btn-copy" id="gen-copy">Copy</button>
</div>

<pre id="gen-output"><code id="gen-text">Pick a game above to generate your prompt.</code></pre>
</div>

<script>
(function() {
  const gameInput = document.getElementById('gen-game');
  const knowChecks = document.querySelectorAll('.know-check');
  const knownCountEl = document.getElementById('known-count');
  const playersSelect = document.getElementById('gen-players');
  const devicesSelect = document.getElementById('gen-devices');
  const deploySelect = document.getElementById('gen-deploy');
  const checkboxes = {
    training: document.getElementById('opt-training'),
    commentator: document.getElementById('opt-commentator'),
    opponent: document.getElementById('opt-opponent'),
    visual: document.getElementById('opt-visual'),
    variants: document.getElementById('opt-variants'),
    step: document.getElementById('opt-step'),
    explain: document.getElementById('opt-explain')
  };

  const STORAGE_KEY = 'shapes-games-i-know';

  // Load known games from localStorage
  function loadKnown() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch { return []; }
  }

  function saveKnown() {
    const known = Array.from(knowChecks).filter(c => c.checked).map(c => c.value);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(known));
    updateKnownCount();
  }

  function updateKnownCount() {
    const n = Array.from(knowChecks).filter(c => c.checked).length;
    knownCountEl.textContent = n > 0 ? '(' + n + ')' : '';
  }

  function restoreKnown() {
    const known = loadKnown();
    knowChecks.forEach(cb => {
      cb.checked = known.includes(cb.value);
    });
    updateKnownCount();
  }

  // Restore on load
  restoreKnown();

  function highlightActive() {
    const val = gameInput.value.trim();
    knowChecks.forEach(cb => {
      cb.closest('label').classList.toggle('active', cb.value === val);
    });
  }

  // Clicking any game checks it AND sets it as the build target
  knowChecks.forEach(cb => {
    cb.addEventListener('change', function() {
      if (this.checked) {
        gameInput.value = this.value;
        highlightActive();
      }
      saveKnown();
      update();
    });
  });

  // Clicking label text (not checkbox) just selects for building
  document.getElementById('game-picker').addEventListener('click', function(e) {
    if (e.target.classList.contains('know-check')) return;
    const label = e.target.closest('label');
    if (!label) return;
    const cb = label.querySelector('.know-check');
    if (!cb) return;
    gameInput.value = cb.value;
    highlightActive();
    update();
  });

  // If user types, update live
  gameInput.addEventListener('input', update);

  function getKnownGames() {
    return Array.from(knowChecks).filter(c => c.checked).map(c => c.value);
  }

  function randomOption(sel) {
    const opts = sel.querySelectorAll('option');
    const start = opts[0].value === '' ? 1 : 0;
    sel.selectedIndex = start + Math.floor(Math.random() * (opts.length - start));
  }

  function randomGame() {
    const all = Array.from(knowChecks);
    const pick = all[Math.floor(Math.random() * all.length)];
    gameInput.value = pick.value;
  }

  function randomCheckboxes() {
    const keys = Object.keys(checkboxes);
    keys.forEach(k => checkboxes[k].checked = false);
    const n = 1 + Math.floor(Math.random() * 3);
    const shuffled = keys.sort(() => Math.random() - 0.5);
    shuffled.slice(0, n).forEach(k => checkboxes[k].checked = true);
  }

  function buildPrompt() {
    const game = gameInput.value.trim() || '[pick a game]';
    const players = playersSelect.value;
    const devices = devicesSelect.value;
    const deploy = deploySelect.value;

    const cleanPlayers = players.startsWith('Not sure') ? 'solo vs AI' : players.toLowerCase();
    const cleanDevices = devices.startsWith('Not sure') ? 'desktop' : devices.toLowerCase();
    const cleanDeploy = deploy.startsWith('Not sure') ? 'local' : deploy;

    const known = getKnownGames().filter(g => g !== game);

    let extras = [];
    if (checkboxes.training.checked) extras.push('training mode (recommended plays with EV, toggleable)');
    if (checkboxes.commentator.checked) extras.push('commentator panel (strategy narration)');
    if (checkboxes.opponent.checked) extras.push('opponent modeling (card counting / deduction)');
    if (checkboxes.visual.checked) extras.push('match the look of a real ' + game + ' board');
    if (checkboxes.variants.checked) extras.push('config page for house rule variants');
    if (checkboxes.step.checked) extras.push('step-through mode (click to advance AI turns)');
    if (checkboxes.explain.checked && known.length > 0) {
      extras.push('I already know ' + known.join(', ') + ' — explain ' + game + ' as differences from those');
    } else if (checkboxes.explain.checked) {
      extras.push('explain the rules as differences from a common game');
    }

    const extrasLine = extras.length > 0
      ? '\n\nAlso: ' + extras.join(', ') + '.'
      : '';

    const pageUrl = window.location.href;
    const prompt = `Read ${pageUrl} — then build ${game}. Standard rules, ${cleanPlayers}, ${cleanDevices}, ${cleanDeploy}.${extrasLine}`;

    return prompt;
  }

  function update() {
    document.getElementById('gen-text').textContent = buildPrompt();
  }

  // Live update on any change
  [playersSelect, devicesSelect, deploySelect].forEach(
    sel => sel.addEventListener('change', update)
  );
  Object.values(checkboxes).forEach(
    cb => cb.addEventListener('change', update)
  );

  document.getElementById('gen-roll').addEventListener('click', function() {
    randomGame();
    randomOption(playersSelect);
    randomOption(devicesSelect);
    randomOption(deploySelect);
    randomCheckboxes();
    update();
  });

  document.getElementById('gen-copy').addEventListener('click', function() {
    const text = document.getElementById('gen-text').textContent;
    navigator.clipboard.writeText(text).then(() => {
      this.textContent = 'Copied';
      this.classList.add('copied');
      setTimeout(() => { this.textContent = 'Copy'; this.classList.remove('copied'); }, 1500);
    });
  });
})();
</script>

---

## Stage 1: The Rulebook

The single most important thing you can do is write the rules down. Not a summary. Not "it's kind of like Uno." The actual rules, including your house rules.

> **About ShapeGame**: Throughout this page, examples use a made-up game called ShapeGame — a tile-matching game where players place colored geometric tiles on a shared board, connecting matching edges to score points. ShapeGame isn't real. It's a stand-in for *your* game. Every sample prompt and example uses it so you can see the shape of a good prompt without needing to know someone else's rules. Swap in your game wherever you see it.

Create a file called `RULEBOOK.md`. Include:

- **Setup**: how many players, what pieces, starting state
- **Turn structure**: what happens in what order
- **Legal moves**: what you can and can't do
- **Scoring**: how points work, when they're counted, edge cases
- **Win condition**: how the game ends, who wins
- **House rules**: anything your family does differently

Every family has house rules. Maybe you skip a penalty on the first round. Maybe you allow a move the official rules prohibit. Maybe you've played it wrong for twenty years and that's how the game works now. Write it all down. The rules you don't write become the bugs you find later.

### Sample prompt

> I want to build a digital version of ShapeGame. Interview me about the rules. Ask me about setup, turn structure, legal moves, scoring, win conditions, and any house rules my family plays with. Once you understand the rules, write them into RULEBOOK.md.

### Describing space

If your game has a board, a grid, a layout — anything spatial — this is the hardest thing to get right. Language models don't have a canvas. They process text, not geometry. Spatial relationships you leave to interpretation may be interpreted wrong.

Be explicit about:

- **Coordinate system**: name your axes. "Columns go left-to-right, rows go top-to-bottom. Position (0,0) is the top-left corner." Don't assume the AI knows which way is up.
- **Orientation**: if pieces have a direction (face-up, rotated, flipped), define what each orientation means and how it's stored. "A tile's value is read left-to-right. A vertical placement reads top-to-bottom."
- **Adjacency**: what does "next to" mean? Up/down/left/right only? Diagonals too? "Two tiles are adjacent if they share an edge. Diagonal tiles are not adjacent."
- **Connections**: if pieces connect (like tiles, cards in a tableau, or linked nodes), define exactly what a legal connection looks like. "The touching ends must match. A tile placed to the right of another tile connects its left end to the existing tile's right end."
- **ASCII diagrams**: draw the board state in text. This is the single most effective thing you can do. The AI can parse a labeled grid better than any paragraph of prose.

```
Example board state (ShapeGame):

     col 0   col 1   col 2
row 0  [▲red]—[▲blu]  .
row 1    .    [■blu]—[■grn]
row 2    .      .    [●grn]

Tile [▲red] has edges: top=red, right=red, bottom=blue
Placed at (0,0). Right edge connects to [▲blu] left edge (both red).
```

Orientation is one of the things you may correct often. If two pieces can connect in multiple orientations, spell out every case — and build test cases around it.

### Where you'll correct

The AI may miss ambiguities in the rules that you resolve without thinking. "What happens when there are no cards left to draw?" "Who goes first in a tie?" These are the things you know but haven't said. Every game has some of them.

2D spatial reasoning is a weak spot. The AI can confuse left/right, mix up which end of a piece connects where, or lose track of the board layout. The more spatial your game is, the more you may correct. Coordinate systems and ASCII diagrams in your rulebook prevent some of it — and since you've read this far, you may dodge the worst of it entirely.

---

## Stage 2: Core Engine

The game logic, separate from any UI. Pure rules: generate legal moves, validate plays, calculate scores, manage turns, detect game end.

The key architectural decision: **the engine should have zero dependencies on UI or networking.** It's a library that takes a game state and an action, and returns a new game state. This means you can test it without a browser, run tournaments without a server, and swap the UI later without touching game logic.

### Sample prompt

> Read RULEBOOK.md. Build the core game engine — no UI, no server. Just the game logic: board state, legal move generation, move validation, scoring, turn management, and game-end detection. Use dataclasses (Python) or plain types (TypeScript). Every function should be pure — take state in, return state out. Write tests that play a full game and verify scoring.

### Architecture patterns that work

- **Pure reducers**: game state in, action in, new state out. No side effects.
- **Deterministic RNG**: seed your randomness so games are reproducible. You can replay any game from its seed. Essential for testing and debugging.
- **Strategy pattern**: AI players are just functions that take a read-only game state and return a move. Plug in different strategies without changing the engine.
- **Event sourcing**: every action is a recorded event. The game state is derived from the event log. This gives you replay, undo, and a full audit trail for free.

### Where you'll correct

- Scoring edge cases. Ties, blocked games, what happens when someone can't move.
- The engine may be "close enough" on the first pass. The corrections tend to be about the 20% of rules that require real domain knowledge — the stuff you know from playing, not from reading.

---

## Stage 3: Player Count and Teams

Decide how many players, whether there are teams, and how human vs AI players work.

- **Solo play**: 1 human + AI opponents. Easiest to build and test.
- **Hot-seat**: multiple humans take turns on the same device. No networking needed.
- **Teams**: paired players sharing a score. The engine needs to track team scores separately.

### Sample prompt

> ShapeGame supports 2–4 players individually. Add individual scoring to the engine. For single-player mode, the human plays against 1–3 AI opponents. AI players use the strategy interface we built.

### Where you'll correct

- Team scoring aggregation
- Turn order and how it interacts with teams
- Rules about partnerships — can teammates communicate? Share information?

---

## Stage 4: UI — Make It Visible

Now you make it playable. Start with the simplest thing that works.

**Terminal UI** is the fastest to build. The AI can generate a working text-based game in minutes. Good for testing, hard to love.

**Vanilla HTML/CSS/JS** is the sweet spot. No framework needed. A canvas or a grid of divs. The AI may default to React — push back. You don't need a JavaScript framework to render a card game or a board.

**The key UX decisions:**
- How do you show the game state? (Board view? Hand view? Both?)
- How does the player indicate their move? (Click? Drag? Type?)
- How do you show legal moves? (Highlight? Filter? Tooltip?)
- How do you show scores?
- What happens between turns? (Pause? Animation? Sound?)

### Sample prompt

> Build a web UI for the game. Plain HTML, CSS, and vanilla JavaScript — no React, no framework.
>
> Show the ShapeGame board in the center as a grid. Show the player's tiles at the bottom. Highlight valid placements when it's your turn. Show scores in the corner. Use a dark felt background with the tile shapes in bright colors.
>
> The UI calls the engine for legal moves and validation — it never implements game logic itself.

### Where you'll correct

- Sizing and spacing. The AI may guess wrong on proportions.
- The "feel" of the game — transitions, announcements, pacing between turns
- Mobile layout if you care about phones
- The visual design may be generic. You'll want to make it feel like *your* game.

### Six things you'll say every time

These patterns showed up across multiple board game builds — cribbage, bridge, dominos. They're predictable. Every game hits them.

**1. "What just happened?"**

The game scores a point and the player doesn't know why. This is always the first complaint. Every game event needs a visible explanation. Don't just update a number — say "15 for 2" or "3-card run." If the player has to guess why their score changed, the UI is broken.

> When a game event occurs — a score, a penalty, a turn skip — show what rule triggered it and why. Log it, and briefly animate the rule name near where it happened.

**2. "Who goes first?"**

The game starts and the player doesn't know whose turn it is, or why. Narrate the flow. "You deal first (random)." "East opens the bidding." A status line that says what's happening in plain language is not optional.

> Always show: whose turn it is, what phase the game is in, and what the current player can do. If the starting player is random, say so.

**3. "It looks wrong."**

If the game has a physical form — a cribbage board, a card table, a chess board — the player has visual expectations. They'll know instantly if the board "looks wrong" even if the logic is correct. Google the real thing before rendering it.

> If your game has an iconic physical form, match it. Screenshot a real one and put it in the project as a reference. The first playtest catches this instantly — but only if you look.

**4. "It's covering the cards."**

Score explanations, advisor tips, and event logs will overlap the game area on the first try. Every time. Overlays get in the way, and making them smaller doesn't fix it. Give feedback its own dedicated space — a panel, a sidebar, a bottom bar with its own real estate.

> Never overlay game feedback on the play area. Dedicate a fixed region for scores, messages, and advisor output. If it needs more room, let the player expand it — don't let it cover the board.

**5. "What does that mean?"**

If the game has domain terms the player might not know — trump, meld, HCP, crib, NT — they need inline explanation. Don't assume the player already knows the game. They might be learning it through your app.

> Every domain term should have a tooltip or pop-out the first time it appears. Consider a "learn" panel that covers the basics — card values, scoring rules, common terms. Make it toggleable so experienced players can hide it.

**6. "Can it teach me?"**

You'll want a training mode. A toggle that shows: what should I play here, why, and what are the risks. On the second game you build, you'll ask for this in your opening prompt. On the first, you'll discover you want it after playing a few rounds.

> Plan for a training/advisor mode from the start. Show recommended moves, explain the reasoning, color-code options by expected value. This is often more valuable than the game itself — especially for games you're learning.

### Three more things (if you're building for a learner)

If the player is learning the game through your app — not just playing a game they know — these show up fast.

**7. "Explain it like I already know Hearts."**

The single most effective teaching move: map the new game onto a game the player already knows. "Bridge is like Hearts, except there's a trump suit you choose by bidding, and you play with a partner whose hand you can see." One sentence. More useful than a full rules page.

> Ask the player what games they already know. Frame the rules as differences from the familiar game. "Like Hearts, you must follow suit. Unlike Hearts, you choose a trump suit by bidding."

**8. "Too much text."**

The learn panel had everything in it — and the player still didn't understand. The problem wasn't missing information. It was too much information. Walls of rules don't teach. Short explanations at the moment they matter do.

> Keep reference text short. Teach in context — when the player needs to bid, explain bidding. When they need to play, explain playing. Don't front-load a rulebook.

**9. "I refreshed and lost my game."**

If the player is learning, they'll refresh by accident, fat-finger a navigation, or close the tab. Don't punish them. Save the game state. Let them come back.

> Persist game state to localStorage or the server. A refresh should resume the game, not start a new one.

---

## Stage 5: Validation — Prove It Works

This is where testing goes beyond "does it run" to "does it play right."

### Break it before you fix it

The biggest sin in debugging with AI: letting it fix something it hasn't reproduced. The AI sees an error, jumps to a fix, and tells you it's solved. But if there was no failing test before the fix, how do you know the fix did anything? Maybe it fixed a different problem. Maybe it fixed nothing and the bug comes and goes. Maybe it introduced a new bug that looks like progress.

The rule: **no fix without a failing test first.** When you find a bug, the first prompt isn't "fix this." It's:

> Write a test that reproduces this bug. The test should fail right now. Don't fix anything yet.

Once you have a red test, *then* fix it. The test goes green. Now you know. This is true for all software, but it's especially important with AI because the AI will confidently skip this step every single time.

### See the same thing

Here's a problem you'll hit: you look at the board and see a bug. The AI looks at the data and thinks everything's fine. You're both right about what you're looking at — you're just not looking at the same thing. You see pixels. The AI sees a data structure. And the two don't agree, but neither of you can tell from your own view.

You need to find a way to look at the same thing. Something you can see and the AI can read.

One approach that works: build small, standalone test pages. Place a known sequence of pieces on the board. Render them. Then interrogate what's actually there — DOM positions, bounding boxes, what's adjacent to what. The AI can read coordinates and adjacency lists. You can see the picture. Now you're both looking at the same thing.

For ShapeGame, a test page might render three tiles in a row and then dump:

```
Tile [▲red] at (0,0): right_neighbor=[▲blu] at (1,0)
  Connection: ▲red.right_edge=red, ▲blu.left_edge=red → MATCH
Tile [▲blu] at (1,0): right_neighbor=[■blu] at (2,0)
  Connection: ▲blu.right_edge=green, ■blu.left_edge=blue → MISMATCH
```

You can see the mismatch on screen. The AI can see it in the text output. Now you're arguing about the same thing instead of talking past each other.

The medium doesn't matter — DOM inspection, canvas pixel sampling, script output, a log file. What matters is that you both agree on what you're looking at.

### Test snapshots

Run a full game with a fixed random seed. Capture every move, every score, every state transition as a human-readable log. Save it as a golden file. If you change the engine and the log changes, you'll see exactly what changed and whether it's correct.

### Tournament simulation

Run 100 games with different seeds. Check that:
- Every game terminates
- All scores satisfy your game's scoring rules
- No illegal moves were made
- The winner's score meets the win condition

### Sample prompt

> Add deterministic testing: seed the RNG so games are reproducible. Write a test that plays a full game with seed 12345, logs every move to a snapshot file, and compares against a golden log. If anything changes, the test fails and shows the diff.
>
> Then write a tournament test: run 100 seeded games. Assert every game terminates, all scores are valid, and no illegal moves occurred. Report win rates by strategy.

### Sample prompt (test page)

> Build a standalone test page at `/test/three-tiles`. Place three ShapeGame tiles in a row with known values. Render them with the real renderer. After render, dump every tile's position, its neighbors, and whether each connection is valid. Show PASS/FAIL for each connection. I want to see the board AND read the validation output on the same page.

### Where you'll correct

- The AI may write tests that test its own code, not the rules. Push for rule-based assertions: "the score is always even," not "the score equals 14."
- Snapshot format — make it human-readable. You need to be able to read it and say "yes, that's a correct game of ShapeGame."
- The AI may skip reproduction and go straight to a fix. Hold the line: red test first, then fix, then green test. Every time.

---

## Stage 6: AI Strategy — Make It Smart

Start dumb, then get smarter. The strategy pattern from Stage 2 pays off here.

**Level 0 — Random**: pick a random legal move. This is your baseline. If random wins 50% against your "smart" AI, your smart AI isn't smart.

**Level 1 — Heuristic**: simple rules. Play the highest-scoring move. Or the move that blocks your opponent. Or the move that leaves you safest. You know what a good player does — tell the AI.

**Level 2 — Context-aware**: consider the whole board state. What's been played? What can opponents probably do? What information is hidden? This is where your domain knowledge as a player matters most.

**Level 3 — Learned**: train a model on game telemetry. Export per-turn features (game state, available moves, outcomes). Train a predictor to rank moves. This is optional and advanced — some games benefit from it, many don't need it.

### Sample prompt (heuristic)

> Add AI strategies to the engine. Start with three:
> 1. RandomStrategy — picks a random legal move
> 2. AggressiveStrategy — plays the move that scores the most points
> 3. DefensiveStrategy — plays the move that minimizes risk
>
> Run a tournament: each strategy plays 100 games against each other. Report win rates.

### Sample prompt (ML, optional)

> Export per-turn game features to JSONL: game state, all candidate moves, and the resulting outcome. Run 10,000 seeded games and export the data. Then train a predictor that ranks moves by expected outcome. Start with scikit-learn.

### The real work

Building the AI player is its own correction loop, separate from building the game. The engine can be perfect and the AI player can still be terrible.

The cycle looks like this:

1. **Watch it play.** Run a game with verbose logging. Read every move. You may immediately see moves no human would make.
2. **Name the mistake.** "It played a high-value piece early when it should have held it." "It ignored an obvious block." "It doesn't count what's been played." Turn your instinct into a rule.
3. **Add the rule.** Give the strategy a new heuristic. "If the opponent is within 10 points of winning, prioritize blocking over scoring."
4. **Tournament it.** Run 100 games. Did the win rate change? Did new dumb behavior emerge?
5. **Repeat.**

This is where you're the domain expert, not the programmer. You know what a good player *feels* like. The AI doesn't — it optimizes whatever you tell it to optimize. If you only tell it to maximize score, it'll play greedily and lose to any strategy that thinks two moves ahead.

### Where you'll correct

- The AI may optimize for one thing (usually scoring) and ignore everything else. Push for strategies that play like a real person.
- Feature engineering is where your domain knowledge matters most. You know what a good player pays attention to. The AI doesn't — tell it.
- Spatial games can hit the same 2D problem here: the AI player may misread the board. If it can't see that a position is blocked or that a connection creates a scoring opportunity, its moves may look random. Test spatial reasoning in the strategy separately from move selection.

---

## Stage 7: Multiplayer — Play Together

Some projects never get here. The author's didn't — six repositories, a year of work, an ML pipeline, and the game still runs on one machine. Not because the architecture couldn't handle it. The engine was pure, the state was serializable, the strategy pattern meant swapping humans for network players was a clean interface change. It just wasn't the itch that needed scratching.

That's fine. If you got through Stage 6 and you're playing a good game against an AI opponent that feels right — you built the thing. Multiplayer is here if you want it.

Two paths:

**WebSocket** — real-time, bidirectional. Both players see moves instantly. The server runs the engine; clients send moves and receive state updates.

**Turn-based API** — REST endpoints. Players poll for state. Simpler but higher latency.

### Network visibility is the whole game

The single most important rule of multiplayer: **the client only sees what that player is allowed to see.** Not "the UI hides it." The server never sends it.

If ShapeGame has hidden tiles in your hand, the server sends each player *only their own hand*. The board state is public — everyone gets it. The draw pile count is public — everyone gets it. But the contents of the draw pile? The other players' tiles? Never leaves the server.

This means the server doesn't broadcast one game state to all clients. It builds a **per-player view** — a filtered projection of the full state that contains only what that player should know.

```
Full state (server only):
  board, draw_pile, hands[player_0, player_1, player_2], scores, turn

Player 0's view (sent to player 0):
  board, draw_pile_count, my_hand, scores, turn, legal_moves

Player 1's view (sent to player 1):
  board, draw_pile_count, my_hand, scores, turn, legal_moves
```

If you open the browser dev tools and inspect the WebSocket messages, you should see *nothing* you couldn't learn from looking at your side of the table. That's the test.

The AI may get this wrong on the first pass — broadcasting the full game state to every client and letting the UI decide what to show. That's a cheat code waiting to happen. Push back. The server is the only authority, and it should filter before sending.

### Sample prompt

> Add WebSocket multiplayer to ShapeGame. The server runs the game engine. Clients connect, send moves as JSON, and receive per-player state views.
>
> Critical: build a `player_view(state, player_id)` function that returns only what that player is allowed to see — their own hand, the public board, scores, and their legal moves. Never send another player's hand or the draw pile contents. The client receives only its view, never the full state.
>
> Handle disconnects gracefully — the game pauses, doesn't crash.

### Where you'll correct

- **Network visibility** — this is the big one. The AI may default to broadcasting full state. Every time you add a new feature (chat, spectators, replays), re-check: does the client see anything it shouldn't?
- Race conditions: two players acting at the same time
- Reconnection: what happens when someone's wifi drops?
- Spectator mode: spectators should see the board but not any player's hand. That's a third view type.

---

## Stage 8: Deployment — Put It Somewhere

Get it running outside your laptop.

**GitHub Pages** — free, automatic. Works for games where the AI runs in the browser (no server needed).

**A VPS** — for games with a server. Run the backend, serve the frontend from the same process.

### Sample prompt

> I want to deploy ShapeGame. The frontend is static HTML/CSS/JS. The backend is a Python WebSocket server. What's the simplest way to get both running on a VPS?

### Where you'll correct

- CORS issues (frontend on one domain, backend on another)
- Secure WebSocket connections (wss:// vs ws://)
- Process management (the server needs to stay running)

---

## The real progression

This page describes a clean lifecycle, but real builds aren't clean. The author's board game project went through six repositories over a year. A sandbox. A proof of concept. An engine rewrite. A full-stack rebuild. A production UI. An ML training pipeline. Each one taught something the next one needed.

The breakthrough came when the author could hand the AI a rulebook and a steering file, and get a working game in a single session. But getting to that point required the earlier attempts — not because the code carried over, but because the human's ability to articulate the rules and architecture had sharpened. The AI got better at building. The human got better at asking.

That's the real lesson: the inflection point isn't just about smarter models. It's about you learning what to tell them.

---

## How prompting evolved

### Early 2024: function-by-function

```
Write a function that scores a round of ShapeGame.
It takes a list of tiles remaining in a player's hand.
Each tile's point value is the sum of its edge colors.
Wildcards score zero.
```

You were the architect. The AI was a typist. Every edge case you forgot was a bug.

### Mid 2025: system-level

```
Here are the rules of ShapeGame. Build a scoring engine that
handles multiple rounds, tracks cumulative scores, and
determines the winner.
```

Better. But still missed house rules, got confused by ambiguity, needed substantial debugging.

### November 2025+: the inflection point

```
Read RULEBOOK.md. Build a playable version with scoring, turn
management, and a web UI. Follow the rules exactly. Ask me
if anything is ambiguous.
```

Corrections shifted from "this function is broken" to "my family plays ShapeGame differently" and "I'd prefer the scores displayed this way." The shift from correcting fundamentals to correcting preferences — that's the inflection point.

### The second game: the flywheel

The first game prompt was four words: "It's cribbage. On a board."

The second game prompt, started three minutes later:

```
Build a contract bridge trainer for my aunt. She'll be viewing
it on her phone. She plays with friends, is a recent learner.
I'd like to learn it too. Maybe 2p v 2ai, or 1p+1ai v 2ai.
Customizable house rules. A mode that tells me what I should
play and why, toggle on and off. TV browser too — mouse
and/or keyboard, don't prefer switching between the two.
```

Same person. Same afternoon. But different reasons. Cribbage was goofing around — a game he already knows, built for fun, just to see if it works. Bridge was a gift — a game he doesn't know, built so he could learn it and play with his aunt on her phone.

The second prompt is more specific because the *intent* is different. When you're building for someone else, you think about their device, their skill level, their context. When you're building for yourself, "it's cribbage" is enough because you'll correct as you go.

But the flywheel is still there. The cribbage build is where training mode was *discovered* — asked for late, after playing a few rounds. The bridge build is where training mode was *assumed* — requested in the opening prompt, because now it's obvious that any game should teach you while you play. Both games were playable within three hours. The human spent about fifteen minutes on each, dropping in to correct what looked wrong.

The flywheel doesn't just make your prompts longer. It changes what you think a game *should be*. After cribbage, a game without a training mode feels incomplete.

---

## Book connection

This is the correction shape from Chapter 7. The first version is never right — not because the AI failed, but because building something is how you discover what you actually want.

It's also the trust shape from Chapter 10. Each stage builds evidence. The engine passes tests — you trust the scoring. The tournament runs 10,000 games — you trust the rules. Trust is earned stage by stage, with evidence.

And it's the maxim: make a system that will learn, but don't make it guess — tell it what you know. The RULEBOOK.md is you telling it. The corrections are you telling it more. The ML pipeline is you letting it learn from what you've told it. Every stage is the same motion: your knowledge, articulated, becoming the system's capability.

---

## External references

- [Phaser](https://phaser.io/) — the most popular open-source HTML5 game framework. Overkill for card games, useful if your board game needs real-time rendering or physics.
- [Boardgame.io](https://boardgame.io/) — a framework specifically for turn-based games with multiplayer. Handles state management, AI, and networking.
- [chess-programming.org](https://www.chessprogramming.org/Main_Page) — deep reference on game tree search, evaluation functions, and AI strategy. Relevant for Stage 6.
