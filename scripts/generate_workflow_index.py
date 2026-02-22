#!/usr/bin/env python3
"""Generate a markdown index of workflows with metadata.

This helper scans the ``workflows/`` directory and produces an
arborescent listing that includes:

- relative path of each workflow
- last Git commit date when the workflow was modified
- the short description (first line or description in README)
- the status (parsed from README's "## Status" section)

Usage::

    python scripts/generate_workflow_index.py > workflows/WORKFLOW_INDEX.md

The generated file can be committed or used for quick overview.

This script can be invoked from CI as well (see docs/ci-cd-setup.md)
"""

import subprocess
import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).parent.parent / "workflows"

# Emoji mapping for categories
CATEGORY_EMOJI = {
    "01-communication": "📧",
    "02-marketing": "📱",
    "03-sales": "💼",
    "04-data-intelligence": "📊",
}

# Emoji mapping for status
def get_status_emoji(status: str) -> str:
    """Return emoji based on status."""
    status_lower = status.lower()
    if "published" in status_lower:
        return "🟢"
    elif "development" in status_lower:
        return "🚧"
    elif "archived" in status_lower or "deprecated" in status_lower:
        return "📦"
    return "❓"


def normalize_status(status: str) -> str:
    """Normalize status names for display (using n8n terminology)."""
    status_lower = status.lower()
    if "published" in status_lower:
        return "Published"
    elif "development" in status_lower:
        return "Development"
    elif "archived" in status_lower or "deprecated" in status_lower:
        return "Archived"
    return status


def git_last_commit(path: pathlib.Path) -> str:
    """Return the ISO date of the last git commit that touched ``path``.
    If git is not available or the file is untracked, return empty string.
    """
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ci", str(path)],
            cwd=BASE.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def parse_metadata(path: pathlib.Path) -> str:
    """Extract status from metadata.json."""
    metadata_file = path / "metadata.json"
    if not metadata_file.exists():
        return ""

    try:
        data = json.loads(metadata_file.read_text(encoding="utf-8"))
        return data.get("status", "")
    except (json.JSONDecodeError, KeyError):
        return ""


def parse_readme(path: pathlib.Path) -> str:
    """Return description extracted from README.md.

    - ``description`` is the first non-empty line after the main heading.
    """
    description = ""
    readme_file = path / "README.md"
    if not readme_file.exists():
        return description

    text = readme_file.read_text(encoding="utf-8").splitlines()
    # description: first non-heading, non-empty line after the first heading
    seen_heading = False
    for line in text:
        if not seen_heading and line.startswith("# "):
            seen_heading = True
            continue
        if seen_heading and line.strip() and not line.startswith("#"):
            description = line.strip()
            break

    return description


def main() -> None:
    # make sure stdout is utf-8 so emojis and accents don't crash on Windows
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    lines: list[str] = []
    lines.append("# Workflow index\n")

    # Build hierarchical tree: category -> subcategory -> workflow
    tree: dict[str, dict[str, list[dict]]] = {}

    for wf_dir in sorted(BASE.rglob("workflow.json")):
        wf_dir = wf_dir.parent
        rel = wf_dir.relative_to(BASE).as_posix()

        # Skip archived workflows
        if "/archive/" in rel:
            continue

        parts = rel.split('/')
        category = parts[0] if parts else ''
        subcategory = parts[1] if len(parts) > 1 else None
        workflow_name = parts[-1]

        commit_date = git_last_commit(wf_dir / "workflow.json")
        desc = parse_readme(wf_dir)
        stat = parse_metadata(wf_dir)

        # Add emoji and normalize status
        status_emoji = get_status_emoji(stat)
        normalized_stat = normalize_status(stat)
        status_text = f"{status_emoji} {normalized_stat}" if stat else ""

        workflow_entry = {
            "name": workflow_name,
            "date": commit_date,
            "status": status_text,
            "desc": desc
        }

        if category not in tree:
            tree[category] = {}
        if subcategory:
            if subcategory not in tree[category]:
                tree[category][subcategory] = []
            tree[category][subcategory].append(workflow_entry)

    # Generate output with proper hierarchy
    for category in sorted(tree.keys()):
        cat_emoji = CATEGORY_EMOJI.get(category, "📁")
        lines.append(f"- {cat_emoji} **{category}/**")

        for subcategory in sorted(tree[category].keys()):
            lines.append(f"  - **{subcategory}/**")

            for workflow in tree[category][subcategory]:
                date_text = f"(last modified {workflow['date']})" if workflow['date'] else ""
                status_text = f"- {workflow['status']}" if workflow['status'] else ""
                desc_text = workflow['desc']

                # Format: workflow name with metadata on separate line
                lines.append(f"    - **{workflow['name']}/**")
                if date_text or status_text or desc_text:
                    info_parts = [p for p in [date_text, status_text, desc_text] if p]
                    lines.append(f"      {' '.join(info_parts)}")

    # Write directly to file instead of stdout to avoid PowerShell encoding issues on Windows
    output_file = BASE / "WORKFLOW_INDEX.md"
    output_file.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
