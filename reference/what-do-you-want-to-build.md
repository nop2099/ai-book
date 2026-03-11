---
title: What Do You Want to Build?
book_chapter: 01-meeting/01-first-contact
summary: Pick a project shape that matches your ambition, then let your AI help you start building it today.
platforms: [mac, windows, linux]
---

# What Do You Want to Build?

Don't start with tools. Don't start with GitHub. Start with desire.

You have access to an intelligence that can write code, reason about structure, and build working software from a description. The question isn't what it can do. The question is what you want to exist in the world that doesn't exist yet.

Pick a shape. Then build it.

## The project shapes

### Board Game

You have a game your family plays. You want a digital version — scoring, rules enforcement, maybe a tournament tracker. The key: you already know the rules. The AI doesn't. You bring the rulebook, and it builds what you describe.

**Sample prompt to start:**

> I want to build a digital version of [game name]. Here are the rules: [paste rulebook or describe rules]. Start with a scoring engine that handles a single round. Don't build a UI yet — just the logic.

### Octopus in a Box

A voice assistant or personal AI agent that lives on your machine, remembers your preferences, and does things for you. Think Jarvis, but scoped to what you actually need — not what a corporation thinks you need.

**Sample prompt to start:**

> I want to build a personal AI agent that runs locally. It should be able to take voice input, remember context between sessions, and perform tasks I define. Start by building a simple command loop: I type or speak, it responds, and it saves our conversation to a file I can review later.

### Operations Report Agent

You have messy data — spreadsheets, logs, exports from three different systems. You need to turn it into a report that reflects expert judgment, not just numbers. The AI reads the mess, applies rules you define, and produces defensible output.

**Sample prompt to start:**

> I have data in [describe format: CSV, spreadsheet, database export]. I need to produce a [weekly/monthly] report that [describe what the report should show]. Here's an example of what the finished report looks like: [paste example or describe structure]. Start by reading the raw data and producing a summary.

### Health / Personal Tracker

Sensors, wearable data, manual logs — you want a dashboard that doesn't just display numbers. You want an AI that can reason about trends, catch anomalies, and tell you what they might mean.

**Sample prompt to start:**

> I want to build a personal health tracker. I'll input [weight, blood pressure, mood, sleep, exercise — pick yours]. I want a dashboard that shows trends over time and lets me ask an AI questions about my data. Start with a simple CSV-based logging system and a script that generates a weekly summary.

### Home Automation

Smart home, sensors, MQTT brokers, devices talking to each other. You want agents that react to your environment — not just timers and triggers, but reasoning about what's happening.

**Sample prompt to start:**

> I want to build a home automation system. I have [describe devices: temperature sensors, smart plugs, lights, etc.]. I want an AI agent that can read sensor data, apply rules I define, and control devices. Start with reading data from one sensor and logging it.

### Wall of Data

Your conversations with AI, your git commits, your notes and bookmarks — assembled into something browsable, searchable, and yours. Not trapped in someone else's app. On your machine.

**Sample prompt to start:**

> I want to build a personal data wall. I have [conversations, notes, bookmarks, commit history — pick yours] scattered across [describe locations]. I want a local web page that assembles it all into a browsable timeline. Start by reading from one source and rendering it as HTML.

### Budget App

Personal finance tracking. Income, expenses, categories, projections. You define the rules — what counts as "essential," what your savings targets are, how you think about money.

**Sample prompt to start:**

> I want to build a personal budget tracker. I want to categorize expenses, set monthly targets, and see where my money goes. I'll import transactions from [bank CSV export / manual entry]. Start with a script that reads a CSV of transactions and categorizes them by rules I define.

### Memory Viewer

Foveated memory — high resolution for recent and important things, compressed for the rest. An AI librarian that can retrieve what you need without you remembering where you put it.

**Sample prompt to start:**

> I want to build a personal memory system. I'll store notes, conversations, ideas, and references. I want an AI that can search this archive and answer questions about what I've written, decided, or discussed. Start with a simple system that ingests text files from a folder and lets me query them.

### "Reimplement, Don't Import"

Find an open-source tool you admire. Read its code. Understand what it does. Then build your own version from scratch — no forking, no dependencies, just your understanding translated into your code. This is how you learn what the tool actually does instead of trusting a black box.

**Sample prompt to start:**

> I want to understand how [tool name] works by building my own version. Here's the repository: [link]. Read the source code, explain the core architecture to me, then help me build a minimal version that implements [specific feature] from scratch without importing the original.

---

Pick one. Then your AI will tell you what tools you need. The rest of this reference helps you set those tools up.

## The Interview Pattern

Before you build, have the AI interview you. Don't just dump a feature list. Let it ask you questions.

The key insight: **the first question should be about your rules and constraints, not your features.** What are the boundaries? What's out of scope? What do you already know that the AI doesn't?

Paste this into your AI agent before you start building:

> Before we start building, interview me about this project. Ask me questions one at a time. Start with constraints and rules — what this must NOT do, what's out of scope, what I already know about the domain. Then move to features and preferences. Don't write any code until you understand the shape of what I want.

Good interview questions the AI should ask:

- "What's the one thing this absolutely must get right?"
- "What's explicitly out of scope for the first version?"
- "Who is this for — just you, or will others use it?"
- "Do you have existing data, or are we starting from nothing?"
- "Is there a tool you've tried that came close but failed? What did it get wrong?"
- "What does 'done' look like for a first version you'd actually use?"

The interview takes five minutes. It saves hours of building the wrong thing.

## Start small, start now

You don't need to understand git to pick a shape. You don't need a GitHub account to start a conversation with your AI about what you want to build. You need desire and a prompt.

The tools come after the decision. The setup pages in this reference exist to support what you've already decided to build — not the other way around.

Start small. Start now.

If the first version is going on the internet or into someone else's hands, add one more step before you ship it: read [The AI Wrote It, You Shipped It](security-for-directors.html), [Prompt Injection](prompt-injection.html), and [Before You Deploy](before-you-deploy.html).
