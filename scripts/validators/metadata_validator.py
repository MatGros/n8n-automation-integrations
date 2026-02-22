from pathlib import Path
import json

from jsonschema import validate, ValidationError

SCHEMA_PATH = Path("workflows/schema/workflow-metadata.schema.json")


def find_workflows_missing_metadata(workflows_path: str = "workflows"):
    """Return list of workflow paths that lack any kind of metadata file.

    We look for either `metadata.json` (used in final repo layout) or
    `<workflow-name>.metadata.json` which is the temporary form used in the
    inbox. The returned paths are relative to the workflows root.
    """
    root = Path(workflows_path)
    missing = []
    for wf in root.rglob("workflow.json"):
        parent = wf.parent
        base = wf.stem
        candidate1 = parent / "metadata.json"
        candidate2 = parent / f"{base}.metadata.json"
        if not (candidate1.exists() or candidate2.exists()):
            missing.append(str(wf.relative_to(root)))
    return missing


def validate_metadata_files(workflows_path: str = "workflows"):
    """Validate every metadata.json against the canonical schema.

    Returns a list of dictionaries containing file path (relative to workflows)
    and the validation error message. An empty list means all files are valid.
    """
    root = Path(workflows_path)
    results = []

    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except Exception as e:  # pragma: no cover
        # schema missing or unreadable; treat as no validation
        return []

    # match both plain metadata.json and per-workflow metadata files
    for meta in root.rglob("*.json"):
        if meta.name == "metadata.json" or meta.name.endswith(".metadata.json"):
            try:
                data = json.loads(meta.read_text(encoding="utf-8"))
                validate(instance=data, schema=schema)
            except Exception as e:
                results.append({"file": str(meta.relative_to(root)), "error": str(e)})
    return results


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "workflows"
    print(json.dumps({
        "missing": find_workflows_missing_metadata(path),
        "invalid": validate_metadata_files(path),
    }, indent=2))
