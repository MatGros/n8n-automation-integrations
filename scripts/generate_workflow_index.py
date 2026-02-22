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


def parse_readme(path: pathlib.Path) -> tuple[str, str]:
    """Return a pair ``(description, status)`` extracted from README.md.

    - ``description`` is the first non-empty line after the main heading.
    - ``status`` is any text under the "## Status" section.
    """
    description = ""
    status = ""
    if not path.exists():
        return description, status

    text = path.read_text(encoding="utf-8").splitlines()
    # description: first non-heading, non-empty line after the first heading
    seen_heading = False
    for line in text:
        if not seen_heading and line.startswith("# "):
            seen_heading = True
            continue
        if seen_heading and line.strip() and not line.startswith("#"):
            description = line.strip()
            break
    # status: gather lines following "## Status" until next heading
    for idx, line in enumerate(text):
        if line.strip().lower().startswith("## status"):
            # collect next lines until blank or new section
            for l in text[idx+1:]:
                if l.strip().startswith("## "):
                    break
                if l.strip():
                    status += (l.strip() + " ")
            status = status.strip()
            break

    return description, status


def main() -> None:
    # make sure stdout is utf-8 so emojis and accents don't crash on Windows
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    lines: list[str] = []
    lines.append("# Workflow index\n")
    # collect entries by top-level category for indentation
    tree: dict[str, list[str]] = {}
    entries: dict[str, dict] = {}

    for wf_dir in sorted(BASE.rglob("workflow.json")):
        wf_dir = wf_dir.parent
        rel = wf_dir.relative_to(BASE).as_posix()
        parts = rel.split('/')
        category = parts[0] if parts else ''
        commit_date = git_last_commit(wf_dir / "workflow.json")
        desc, stat = parse_readme(wf_dir / "README.md")
        status_text = f" – Status: {stat}" if stat else ""
        date_text = f" (last modified {commit_date})" if commit_date else ""
        entry_text = f"- **{rel}/**{date_text}{status_text} – {desc}"
        tree.setdefault(category, []).append(entry_text)

    # print categories in sorted order with indentation for entries
    for category in sorted(tree.keys()):
        lines.append(f"- **{category}/**")
        for entry in tree[category]:
            # indent with two spaces
            lines.append(f"  {entry}")

    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
