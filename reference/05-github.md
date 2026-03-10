---
title: GitHub
book_chapter: 03-building/13-the-steering-file
summary: Get a GitHub account, install the CLI, clone your first repo, and understand what push/pull/commit actually mean.
platforms: [mac, windows, linux]
---

# GitHub

## What it is

GitHub is where your code lives online. It's a hosting service for git repositories — which are just folders that remember every change you've ever made to the files inside them. Git is the tool. GitHub is the website. They're not the same thing, but they work together.

## Why you'd use it

The book's entire workflow assumes your projects live in git repos. Steering files, AI memory, code changes, version history — all of it depends on git. GitHub is where those repos sync to the cloud, where you collaborate, and where AI coding tools (Claude Code, Codex, Copilot) expect your code to be.

If you've never used GitHub: it's the difference between a document on your desktop and a document in Google Drive. One is local and fragile. The other is backed up, versioned, and shareable.

## How to set it up

### Step 1: Create a GitHub account

Go to [github.com](https://github.com) and sign up. Free tier is fine. Pick a username you don't hate — it'll be in URLs forever.

### Step 2: Install git

#### Mac
```bash
# Git comes with Xcode Command Line Tools
xcode-select --install

# Or via Homebrew (gets you a newer version)
brew install git
```

#### Windows
```powershell
# Via winget
winget install Git.Git

# Then restart your terminal
```

#### Linux
```bash
sudo apt install git    # Debian/Ubuntu
sudo dnf install git    # Fedora
```

### Step 3: Configure git

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Use the same email you used for GitHub. This tags your commits so GitHub knows they're yours.

### Step 4: Install GitHub CLI

The `gh` command makes GitHub operations fast from the terminal. No more switching to the browser to create repos or pull requests.

#### Mac
```bash
brew install gh
```

#### Windows
```powershell
winget install GitHub.cli
```

#### Linux
```bash
# Debian/Ubuntu
sudo apt install gh

# Or see https://github.com/cli/cli/blob/trunk/docs/install_linux.md
```

### Step 5: Authenticate

```bash
gh auth login
```

Choose: GitHub.com → SSH → Yes (use existing key or generate) → Login with browser.

This connects your terminal to your GitHub account. After this, `gh` commands just work.

### Step 6: Set up SSH keys

See [SSH Keys](04-ssh-keys.html). You need this for `git push` to work without passwords.

## Core concepts (the minimum)

**Repository (repo):** A folder tracked by git. Every change is recorded.

**Commit:** A snapshot. "Here's what the files looked like at this moment, and here's why I changed them."

**Push:** Send your local commits to GitHub.

**Pull:** Get commits from GitHub that you don't have locally.

**Clone:** Download a repo from GitHub to your machine for the first time.

**Branch:** A parallel version of the code. You work on a branch, then merge it back.

That's it. You can learn the rest as you need it.

## Common operations

```bash
# Clone a repo
gh repo clone username/repo-name

# Create a new repo from an existing folder
cd your-project
git init
gh repo create your-project --source=. --push

# Check what's changed
git status

# Stage and commit changes
git add specific-file.md
git commit -m "describe what you changed and why"

# Push to GitHub
git push

# Pull latest changes
git pull
```

## How to verify it worked

```bash
# Check git is installed
git --version

# Check gh is installed and authenticated
gh auth status

# Check SSH works with GitHub
ssh -T git@github.com

# Try cloning something
gh repo clone cli/cli -- --depth 1
```

If all four work, you're fully set up.

## How to prompt your AI to do it

> Read this page and help me get set up with GitHub. I've never used git before. Check what I already have installed and walk me through the rest.

For someone who has git but not `gh`:

> I have git installed but I've never used the GitHub CLI. Help me install gh, authenticate, and create a repo from my current project folder.

For ongoing work:

> I made changes to files in my project. Help me commit them with a good message and push to GitHub.

## What can go wrong

- **"fatal: not a git repository"** — You're not in a folder that's been initialized with `git init` or cloned from GitHub.
- **"Permission denied (publickey)"** — SSH keys aren't set up. See [SSH Keys](04-ssh-keys.html).
- **"Updates were rejected because the remote contains work"** — Someone (or you, from another machine) pushed changes you don't have. Run `git pull` first.
- **Accidentally committed a secret** — If you push an API key or password, it's in the git history forever (even if you delete the file). Rotate the key immediately and add a `.gitignore` to prevent it next time.
- **"detached HEAD"** — You checked out a specific commit instead of a branch. Run `git checkout main` to get back to normal.

## Book connection

GitHub is the backbone of every building chapter. The steering file (Chapter 13) is a file in your repo. The pair programming chapter (Chapter 5) assumes you're working in a git-tracked project. The data wall concept depends on your commit history being preserved. Your git log is part of your data — it's a timestamped record of every decision you made and why.
