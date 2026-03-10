---
title: Set Up Your Workspace
book_chapter: 03-building/13-the-steering-file
summary: Create a project directory, open a terminal, and install a package manager — the physical first step before any tool.
platforms: [mac, windows, linux]
---

# Set Up Your Workspace

## What it is

A workspace is a directory on your machine where your projects live. Not your home folder. Not your Desktop. Not Downloads. A deliberate place you chose, with a name that means "this is where I build things."

## Why you'd do this first

Every other page in this reference assumes you have a place to put things. Git repos, project folders, config files — they all need to live somewhere. If you skip this step, you end up with projects scattered across your home directory, your Desktop, and three folders called "untitled."

This takes two minutes. Do it now.

## Step 1: Create ~/work

### Mac / Linux

```bash
mkdir -p ~/work
```

### Windows (PowerShell)

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\work"
```

That's it. You now have a place for your stuff. Every project you build goes inside `~/work/project-name`.

Why not your home directory? Because your home directory is full of invisible config files, application data, and system folders. You don't want your projects mixed in with `.zshrc` and `.config` and `Library`. Keep your work separate from your system's work.

## Step 2: Open a terminal

The terminal is where you'll run commands, talk to your AI coding tools, and manage your projects. If you've never opened one:

### Mac

Press `Cmd + Space`, type "Terminal", press Enter. That's the built-in terminal. It works fine.

If you want something better later, install [iTerm2](https://iterm2.com/) or use the terminal built into VS Code. But the default Terminal app is enough to start.

### Windows

Press `Win + X`, choose "Terminal" or "PowerShell." Use PowerShell, not Command Prompt (CMD). They look similar but PowerShell is what modern tools expect.

If you see "Windows PowerShell" and "PowerShell 7" as options, pick PowerShell 7 — it's newer and better. If you only see Windows PowerShell, that's fine for now.

### Linux

You already know. `Ctrl + Alt + T` on most distros, or find "Terminal" in your application menu.

## Step 3: Install a package manager

A package manager lets you install developer tools with a single command instead of downloading installers from websites. You'll use it to install git, programming languages, and CLI tools.

### Mac — Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After it finishes, it'll tell you to add something to your shell profile. Do what it says. Then restart your terminal and verify:

```bash
brew --version
```

### Windows — winget

winget comes pre-installed on Windows 10 (version 1809+) and Windows 11. Verify it's there:

```powershell
winget --version
```

If it's not installed, get it from the [Microsoft Store](https://apps.microsoft.com/detail/9nblggh4nns1) (it's called "App Installer").

### Linux — apt (Debian/Ubuntu) or dnf (Fedora)

These are already installed. Verify:

```bash
apt --version      # Debian/Ubuntu
dnf --version      # Fedora
```

If you're on Arch, you know what you're doing.

## How to verify it worked

```bash
# Check your workspace exists
ls ~/work

# Check your package manager works
brew --version      # Mac
winget --version    # Windows (in PowerShell)
apt --version       # Linux (Debian/Ubuntu)
```

If both commands work, you're ready for everything else in this reference.

## How to prompt your AI to do it

> Help me set up a development workspace. I want my projects in ~/work, not my home directory. Check if I have a package manager installed. I'm on [Mac/Windows/Linux].

Or if you want the AI to handle it all:

> Read this page and help me set up my workspace. Check what I already have and walk me through anything that's missing.

## What can go wrong

- **"Permission denied" on mkdir**: On shared or corporate machines, your home directory might be locked down. Try creating the folder in a location you control, and tell your AI what happened.
- **Homebrew installation hangs**: It downloads Xcode Command Line Tools, which can take 10-20 minutes on a slow connection. Let it finish.
- **"brew: command not found" after install**: You didn't add Homebrew to your PATH. The installer printed instructions at the end — scroll up and follow them. Or paste this into your terminal: `eval "$(/opt/homebrew/bin/brew shellenv)"`
- **winget not recognized**: Your Windows version might be too old. Update Windows or install App Installer from the Microsoft Store.

## Book connection

The workspace is the foundation under everything the book describes. The steering file lives in a project folder inside `~/work`. Your board game, your data wall, your personal agent — they all start as a directory inside this workspace. Getting this right means every future "create a new project" step is just `mkdir ~/work/new-project && cd ~/work/new-project`.
