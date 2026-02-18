"""Validators for workflow documentation (README + in-workflow hints).

Provides small, focused checks used by tests and CI.
"""
from pathlib import Path
import json
from typing import List, Dict

REQUIRED_README_SECTIONS = ["Description", "Purpose", "Trigger", "Output"]


def _read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def find_readmes_missing_sections(workflows_path: str = "workflows") -> List[Dict[str, List[str]]]:
    """Return list of README files missing one or more required sections.

    Each entry: { 'path': '01-communication/telegram/echo-bot', 'missing_sections': ['Output'] }
    """
    root = Path(workflows_path)
    results = []

    for readme in root.rglob("README.md"):
        # skip category-level READMEs (they are allowed to be summary-level)
        rel = readme.relative_to(root)
        # consider only README.md that live inside a workflow folder (i.e. have a sibling workflow.json)
        if not (readme.parent / "workflow.json").exists():
            continue

        content = _read_text(readme)
        missing = [s for s in REQUIRED_README_SECTIONS if f"## {s}" not in content and s not in content]
        if missing:
            results.append({"path": str(rel.parent), "missing_sections": missing})
    return results


def find_workflows_missing_name(workflows_path: str = "workflows") -> List[str]:
    """Return workflow file paths that are missing the top-level `name` field."""
    root = Path(workflows_path)
    bad = []
    for wf in root.rglob("workflow.json"):
        try:
            j = json.loads(wf.read_text(encoding="utf-8"))
            if not j.get("name"):
                bad.append(str(wf.relative_to(root)))
        except Exception:
            bad.append(str(wf.relative_to(root)))
    return bad


def find_nodes_without_name(workflows_path: str = "workflows") -> List[Dict[str, List[str]]]:
    """Return workflows that contain nodes with missing/empty `name` fields.

    Each entry: { 'path': '01-communication/telegram/echo-bot', 'nodes': ['<node-id>'] }
    """
    root = Path(workflows_path)
    issues = []
    for wf in root.rglob("workflow.json"):
        try:
            j = json.loads(wf.read_text(encoding="utf-8"))
            nodes = j.get("nodes", [])
            bad_nodes = [n.get("id") or n.get("name") or "<unknown>" for n in nodes if not n.get("name")]
            if bad_nodes:
                issues.append({"path": str(wf.relative_to(root)), "nodes": bad_nodes})
        except Exception:
            issues.append({"path": str(wf.relative_to(root)), "nodes": ["<invalid-json>"]})
    return issues


def run_quick_doc_scan(workflows_path: str = "workflows") -> Dict:
    return {
        "readmes_missing_sections": find_readmes_missing_sections(workflows_path),
        "workflows_missing_name": find_workflows_missing_name(workflows_path),
        "nodes_without_name": find_nodes_without_name(workflows_path),
    }


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "workflows"
    print(json.dumps(run_quick_doc_scan(path), indent=2))
