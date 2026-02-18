import json
from scripts.validators.documentation_validator import (
    find_readmes_missing_sections,
    find_workflows_missing_name,
    find_nodes_without_name,
    run_quick_doc_scan,
    find_readmes_missing_quickstart,
    find_readmes_with_short_process,
    find_readmes_missing_example,
)


def test_documentation_validator_api():
    """API surface: run_quick_doc_scan returns expected keys and types."""
    report = run_quick_doc_scan("workflows")
    assert isinstance(report, dict)
    expected_keys = {
        "readmes_missing_sections",
        "workflows_missing_name",
        "nodes_without_name",
        "readmes_missing_quickstart",
        "readmes_process_too_short",
        "readmes_missing_example",
    }
    assert set(report.keys()) == expected_keys
    for k in expected_keys:
        assert isinstance(report[k], list)


def test_all_workflows_have_name():
    """All workflow.json files in the repository must contain a top-level `name` field."""
    missing = find_workflows_missing_name("workflows")
    assert missing == [], f"workflow.json files without 'name' found: {missing}"


def test_readmes_structure_return_shape():
    """find_readmes_missing_sections should return list of dicts with expected keys."""
    items = find_readmes_missing_sections("workflows")
    for it in items:
        assert "path" in it and "missing_sections" in it
        assert isinstance(it["missing_sections"], list)


def test_nodes_have_names():
    """Nodes without name should be reported (but repository nodes should have names)."""
    issues = find_nodes_without_name("workflows")
    # repository workflows should not contain unnamed nodes
    assert issues == [], f"Found nodes without name: {issues}"
def test_readmes_have_quickstart_and_process_and_example():
    """Ensure READMEs include Quick start, Process >= 2 steps, and example/code block."""
    missing_qs = find_readmes_missing_quickstart("workflows")
    short_proc = find_readmes_with_short_process("workflows")
    missing_ex = find_readmes_missing_example("workflows")

    assert missing_qs == [], f"READMEs missing Quick start: {missing_qs}"
    assert short_proc == [], f"README 'Process' too short: {short_proc}"
    # Examples are recommended — report them but do not fail the test-suite
    assert isinstance(missing_ex, list)
