---
title: SSH Keys
book_chapter: 03-building/13-the-steering-file
summary: Generate an SSH key and connect it to GitHub so git push works without passwords.
platforms: [mac, windows, linux]
---

# SSH Keys

## What it is

An SSH key is a pair of files on your computer — one private (stays on your machine, never shared), one public (you give to services like GitHub). Together they prove your identity without a password.

## Why you'd use it

Every time you `git push` or `git pull` from GitHub, your machine needs to prove who you are. Without an SSH key, you're typing passwords or dealing with token expiration. With one, it just works. Silently. Every time.

This is the plumbing underneath everything. If the book says "push to GitHub," this is the thing that makes that sentence possible.

## How to set it up

### Mac

```bash
# Generate a new key (Ed25519 is the modern default)
ssh-keygen -t ed25519 -C "your_email@example.com"

# When it asks for a file location, press Enter for the default (~/.ssh/id_ed25519)
# When it asks for a passphrase, either set one or press Enter for none

# Start the SSH agent
eval "$(ssh-agent -s)"

# Add your key to the agent
ssh-add ~/.ssh/id_ed25519

# Copy the public key to your clipboard
pbcopy < ~/.ssh/id_ed25519.pub
```

Now go to GitHub → Settings → SSH and GPG keys → New SSH Key → paste → save.

### Windows

```powershell
# Open PowerShell (not CMD)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Default location is fine, press Enter
# Passphrase is optional

# Start the SSH agent service
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent

# Add your key
ssh-add $env:USERPROFILE\.ssh\id_ed25519

# Copy the public key to clipboard
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard
```

Now go to GitHub → Settings → SSH and GPG keys → New SSH Key → paste → save.

### Linux

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy to clipboard (install xclip if needed: sudo apt install xclip)
xclip -selection clipboard < ~/.ssh/id_ed25519.pub
```

Now go to GitHub → Settings → SSH and GPG keys → New SSH Key → paste → save.

## How to verify it worked

```bash
ssh -T git@github.com
```

You should see:
```
Hi yourusername! You've successfully authenticated, but GitHub does not provide shell access.
```

If you see "Permission denied," your key isn't registered with GitHub or the agent isn't running.

## How to prompt your AI to do it

> Read this page and help me set up SSH keys for GitHub. Check if I already have keys, and if I do, help me figure out if they're already connected to GitHub. If not, walk me through generating new ones and adding them.

Or more directly:

> I need to set up SSH keys so I can push to GitHub without passwords. I'm on [Mac/Windows/Linux]. Check if I already have keys at ~/.ssh/ and tell me what to do next.

## What can go wrong

- **Multiple keys**: If you have keys for different services (work GitHub, personal GitHub, a server), you may need an `~/.ssh/config` file. It tells SSH which key to use where.
- **Agent not running**: If `ssh-add` says "Could not open connection to authentication agent," the agent isn't started. Run the `eval` command above.
- **Wrong permissions**: SSH is picky. Your `~/.ssh` directory should be `700`, your private key `600`. Run `chmod 700 ~/.ssh && chmod 600 ~/.ssh/id_ed25519` if things look wrong.
- **Passphrase fatigue**: If you set a passphrase and get tired of typing it, you can add it to your Mac keychain with `ssh-add --apple-use-keychain ~/.ssh/id_ed25519`.

## Book connection

This supports every chapter that involves code. The steering file chapter (Chapter 13) assumes you can push to a repo. The pair programming chapter (Chapter 5) assumes you're working in a git-tracked project. SSH keys are the invisible foundation under all of it.
