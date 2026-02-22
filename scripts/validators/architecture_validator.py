"""Validators for repository architecture and naming conventions."""
from pathlib import Path
import re
from typing import List

# EXPECTED_CATEGORIES: Categories that currently exist with workflows.
# As new categories are created, add them to this list in numeric order.
# See RULES.md for the full vision of 16 categories (01-communication through 15-transportation).
EXPECTED_CATEGORIES = [
    "01-communication",
    "02-marketing",
    "03-sales",
    "04-data-intelligence",
    "99-templates",
]

_KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def find_missing_categories(workflows_path: str = "workflows") -> List[str]:
    root = Path(workflows_path)
    missing = []
    for cat in EXPECTED_CATEGORIES:
        if not (root / cat).exists():
            missing.append(cat)
    return missing


def categories_without_readme(workflows_path: str = "workflows") -> List[str]:
    root = Path(workflows_path)
    missing = []
    for cat in EXPECTED_CATEGORIES:
        p = root / cat / "README.md"
        if not p.exists():
            missing.append(cat)
    return missing


def is_kebab(name: str) -> bool:
    return bool(_KEBAB_RE.match(name))


def find_non_kebab_paths(workflows_path: str = "workflows") -> List[str]:
    root = Path(workflows_path)
    bad = []
    # check directory names under workflows (category and subdirs)
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        parts = rel.parts
        # skip files that are README.md
        if p.is_dir():
            for part in parts:
                # ignore numeric prefixes like '01-communication' (they contain numbers and hyphen — still kebab)
                if not is_kebab(part) and part.lower() != part:
                    bad.append(str(rel))
                    break
        else:
            # check filenames (without extension) for kebab-case if json file
            if p.suffix == ".json":
                # skip schema files (e.g., workflow-metadata.schema.json)
                if p.name.endswith(".schema.json"):
                    continue
                name = p.stem
                # Allow specific _STATUS_DATE suffixes (e.g., _PUB_20260221, _DEV_20260221)
                name_without_suffix = re.sub(r'_(PUB|DEV|DRF|DEP|ARC)_\d{8}$', '', name)
                if not is_kebab(name_without_suffix):
                    bad.append(str(rel))
    return bad


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "workflows"
    report = {
        "missing_categories": find_missing_categories(path),
        "categories_missing_readme": categories_without_readme(path),
        "non_kebab_paths": find_non_kebab_paths(path),
    }
    print(json.dumps(report, indent=2))
