import json
from scripts.validators.documentation_validator import (
    find_readmes_missing_sections,
    find_workflows_missing_name,
    find_nodes_without_name,
    run_quick_doc_scan,
)


def test_documentation_validator_api():
    """API surface: run_quick_doc_scan returns expected keys and types."""
    report = run_quick_doc_scan("workflows")
    assert isinstance(report, dict)
    assert set(report.keys()) == {"readmes_missing_sections", "workflows_missing_name", "nodes_without_name"}
    assert isinstance(report["readmes_missing_sections"], list)
    assert isinstance(report["workflows_missing_name"], list)
    assert isinstance(report["nodes_without_name"], list)


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
