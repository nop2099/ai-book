#!/usr/bin/env python3
"""
Render a podcast path from the universal path + tool config.

One path. Six costumes. The story follows you.

Usage:
    python3 render-podcast-path.py --list
    python3 render-podcast-path.py --matrix
    python3 render-podcast-path.py --tool claude-code [--depth long] [--format md|script|html]
    python3 render-podcast-path.py --all --format script    # render all 12 paths
"""

import json, sys, re
from pathlib import Path

BASE = Path(__file__).parent
TREE_FILE = BASE / "podcast-tree.json"
CONTENT_DIR = BASE / "podcast-content"


def load_tree():
    with open(TREE_FILE) as f:
        return json.load(f)


def load_file(rel_path):
    """Load a content file relative to podcast-content/. Returns content or placeholder."""
    full = CONTENT_DIR / rel_path
    if full.exists():
        return full.read_text().strip()
    return f"[TODO: write podcast-content/{rel_path}]"


def theme(text, tool_cfg, family_cfg):
    """Replace all template variables in text with tool config values."""
    replacements = {
        "{{TOOL}}": tool_cfg.get("label", ""),
        "{{KAREN}}": tool_cfg.get("karen") or "the assistant",
        "{{INSTALL}}": tool_cfg.get("install", ""),
        "{{LAUNCH}}": tool_cfg.get("launch", ""),
        "{{INTERFACE}}": tool_cfg.get("interface", ""),
        "{{OPEN_CMD}}": tool_cfg.get("open_cmd", ""),
        "{{PASTE_METHOD}}": tool_cfg.get("paste_method", ""),
        "{{TOOL_URL}}": tool_cfg.get("url", ""),
        "{{FAMILY}}": family_cfg.get("label", ""),
    }
    for key, val in replacements.items():
        text = text.replace(key, val)
    return text


def render_path(tool_id, depth, style, tree):
    """Render the universal path with a tool's costume and style applied."""
    tool_cfg = tree["tools"][tool_id]
    family = tool_cfg["family"]
    family_cfg = tree["families"][family]
    style_cfg = tree["styles"][style]

    sections = []

    for node in tree["universal_path"]:
        # Load universal content
        content = load_file(node["file"])

        # Inject insert if this section has one
        inserts = node.get("inserts")
        if inserts and inserts["type"] == "per-family":
            insert_file = inserts["files"].get(family)
            if insert_file:
                insert_content = load_file(insert_file)
                insert_content = theme(insert_content, tool_cfg, family_cfg)
                point = inserts["point"]
                if point in content:
                    content = content.replace(point, insert_content)
                else:
                    content = content + "\n\n" + insert_content

        # Apply template variables
        content = theme(content, tool_cfg, family_cfg)

        # Depth: short = first paragraph only from universal + first paragraph from insert
        if depth == "short":
            paras = [p.strip() for p in content.split("\n\n") if p.strip()]
            content = paras[0] if paras else content

        sections.append({
            "id": node["id"],
            "title": node["title"],
            "content": content,
            "notes": node.get("notes", ""),
        })

    return {
        "tool_id": tool_id,
        "tool": tool_cfg,
        "family": family_cfg,
        "depth": depth,
        "style": style,
        "style_cfg": style_cfg,
        "sections": sections,
    }


def format_markdown(path):
    """Render as markdown."""
    lines = []
    lines.append(f"# I Want a Podcast — {path['tool']['label']}")
    lines.append(f"")
    lines.append(f"*{path['tool']['label']} ({path['family']['label']}). "
                 f"{'The Map — quick reference.' if path['depth'] == 'short' else 'The Walk — full guided build.'}*")
    lines.append(f"")

    for s in path["sections"]:
        lines.append(f"## {s['title']}")
        lines.append(f"")
        lines.append(s["content"])
        lines.append(f"")

    return "\n".join(lines)


def format_script(path):
    """Render as audiobook script, adapting to the selected style."""
    karen = path["tool"].get("karen") or "the assistant"
    style = path["style"]
    style_cfg = path["style_cfg"]
    lines = []

    depth_label = "The Map" if path["depth"] == "short" else "The Walk"
    lines.append(f"# I Want a Podcast — {path['tool']['label']} ({depth_label}, {style_cfg['label']})")
    lines.append(f"")
    lines.append(f"## Voice Design Notes")
    lines.append(f"")
    lines.append(f"| Tag | Draft Voice | Why |")
    lines.append(f"|---|---|---|")
    lines.append(f"| JAMES | Daniel | Author. Cold open and signoff. |")
    lines.append(f"| NARRATOR | Daniel | Main voice. Warm, direct. |")
    lines.append(f"| STAGE | Samantha | Section headers. |")
    if "KAREN" in style_cfg["speakers"] and path["tool"].get("karen"):
        karen_desc = style_cfg.get("karen_role", "The agent's voice")
        lines.append(f"| KAREN | Karen | {karen}. {karen_desc}. |")
    lines.append(f"")
    lines.append(f"## Script")
    lines.append(f"")
    lines.append(f"> **Cold open**: Prepend `cold-open.md` before this script.")
    lines.append(f"")
    lines.append(f"[JAMES]")
    lines.append(f"This is I Want a Podcast, the {path['tool']['label']} edition. "
                 f"Same tutorial, different tool. By the end you'll have a podcast episode. "
                 f"Let's build.")
    lines.append(f"")

    for s in path["sections"]:
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"[STAGE]")
        lines.append(f"{s['title']}.")
        lines.append(f"")

        paras = [p.strip() for p in s["content"].split("\n\n") if p.strip() and not p.strip().startswith("#")]

        if style == "lecture":
            # Pure narrator. No Karen.
            for para in paras:
                lines.append(f"[NARRATOR]")
                lines.append(para)
                lines.append(f"")

        elif style == "conversation":
            # Alternate: Karen asks, narrator explains.
            # Every other paragraph becomes a Karen question.
            for i, para in enumerate(paras):
                if i > 0 and i % 3 == 0 and path["tool"].get("karen"):
                    # Karen interjects with a question derived from the next content
                    lines.append(f"[KAREN]")
                    # Synthesize a question from the paragraph
                    first_sentence = para.split(".")[0] if "." in para else para[:60]
                    lines.append(f"Wait — {first_sentence.lower().rstrip('.')}? What does that mean?")
                    lines.append(f"")
                lines.append(f"[NARRATOR]")
                lines.append(para)
                lines.append(f"")

        elif style == "workshop":
            # Karen executes, narrator explains.
            for i, para in enumerate(paras):
                if i > 0 and i % 2 == 1 and path["tool"].get("karen"):
                    # Karen reports what she's doing
                    lines.append(f"[KAREN]")
                    lines.append(f"OK, I'm doing that now. Let me show you what I see.")
                    lines.append(f"")
                lines.append(f"[NARRATOR]")
                lines.append(para)
                lines.append(f"")

        elif style == "encounters":
            # Each section becomes a self-contained encounter
            lines.append(f"[NARRATOR]")
            lines.append(f"Encounter: {s['title']}.")
            lines.append(f"")
            for para in paras:
                lines.append(f"[NARRATOR]")
                lines.append(para)
                lines.append(f"")
            if path["tool"].get("karen"):
                lines.append(f"[KAREN]")
                lines.append(f"That's one way to handle it. Roll again or pick the next encounter.")
                lines.append(f"")

    lines.append(f"---")
    lines.append(f"")
    lines.append(f"[JAMES]")
    lines.append(f"That's I Want a Podcast, the {path['tool']['label']} edition. "
                 f"You have a folder, a script, and an episode. "
                 f"The second one starts from where this one ended. "
                 f"Thanks for listening.")

    return "\n".join(lines)


def print_matrix(tree):
    """Show which insert files each family needs."""
    print(f"\n{'Section':<20} {'Universal':<30} {'CLI':<20} {'Desktop':<20} {'Web':<20} {'NLM':<20}")
    print("-" * 130)
    for node in tree["universal_path"]:
        row = f"{node['id']:<20} {node['file']:<30}"
        inserts = node.get("inserts")
        if inserts:
            for fam in ["cli", "desktop", "web", "nlm"]:
                f = inserts["files"].get(fam, "—")
                row += f" {f:<20}"
        else:
            row += f" {'—':<20}" * 4
        print(row)

    # Count files needed
    files = set()
    for node in tree["universal_path"]:
        files.add(node["file"])
        inserts = node.get("inserts")
        if inserts:
            for f in inserts["files"].values():
                files.add(f)
    print(f"\nTotal unique content files: {len(files)}")

    # Check which exist
    existing = sum(1 for f in files if (CONTENT_DIR / f).exists())
    print(f"Written: {existing} / {len(files)}")
    if existing < len(files):
        print(f"TODO:")
        for f in sorted(files):
            if not (CONTENT_DIR / f).exists():
                print(f"  podcast-content/{f}")


def print_list(tree):
    """List all paths."""
    print("\nAll paths:")
    for tool_id, tool in tree["tools"].items():
        fam = tree["families"][tool["family"]]["label"]
        print(f"  --tool {tool_id:<15} ({tool['label']}, {fam})")
    print(f"\n{len(tree['tools'])} tools × 2 depths = {len(tree['tools']) * 2} total paths")
    print(f"Content: 1 universal path + family inserts. Theme applied at render time.")


if __name__ == "__main__":
    tree = load_tree()

    if "--list" in sys.argv:
        print_list(tree)
    elif "--matrix" in sys.argv:
        print_matrix(tree)
    elif "--all" in sys.argv:
        fmt = "script" if "--format" in sys.argv and sys.argv[sys.argv.index("--format") + 1] == "script" else "md"
        depth = "long"
        if "--depth" in sys.argv:
            depth = sys.argv[sys.argv.index("--depth") + 1]
        style = "lecture"
        if "--style" in sys.argv:
            style = sys.argv[sys.argv.index("--style") + 1]
        out_dir = BASE / "podcast-output"
        out_dir.mkdir(exist_ok=True)
        for tool_id in tree["tools"]:
            path = render_path(tool_id, depth, style, tree)
            content = format_script(path) if fmt == "script" else format_markdown(path)
            out_file = out_dir / f"podcast-{tool_id}-{depth}-{style}.md"
            out_file.write_text(content)
            print(f"  wrote {out_file.name}")
        print(f"\n{len(tree['tools'])} paths rendered to {out_dir}/")
    elif "--tool" in sys.argv:
        tool_id = sys.argv[sys.argv.index("--tool") + 1]
        depth = "long"
        if "--depth" in sys.argv:
            depth = sys.argv[sys.argv.index("--depth") + 1]
        style = "lecture"
        if "--style" in sys.argv:
            style = sys.argv[sys.argv.index("--style") + 1]
        fmt = "md"
        if "--format" in sys.argv:
            fmt = sys.argv[sys.argv.index("--format") + 1]

        if tool_id not in tree["tools"]:
            sys.exit(f"Unknown tool: {tool_id}. Use --list.")
        if style not in tree["styles"]:
            sys.exit(f"Unknown style: {style}. Options: {', '.join(tree['styles'].keys())}")

        path = render_path(tool_id, depth, style, tree)

        if fmt == "script":
            print(format_script(path))
        else:
            print(format_markdown(path))
    else:
        print("Usage:")
        print("  python3 render-podcast-path.py --list")
        print("  python3 render-podcast-path.py --matrix")
        print("  python3 render-podcast-path.py --tool claude-code [--depth long] [--style lecture] [--format md|script]")
        print("  python3 render-podcast-path.py --all --format script --depth long --style conversation")
        print(f"\nStyles: {', '.join(tree['styles'].keys())}")
        print(f"Depths: short, long")
        print(f"Tools:  {', '.join(tree['tools'].keys())}")
