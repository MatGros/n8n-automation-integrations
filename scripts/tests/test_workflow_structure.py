#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for workflow directory structure validation
Ensures all workflows follow the required file naming convention
"""

import json
from pathlib import Path


def get_workflow_directories():
    """Get all workflow folders (excluding category READMEs)"""
    workflows_dir = Path(__file__).parent.parent.parent / "workflows"

    # Find all directories that contain workflow files
    workflow_dirs = []

    # Look for directories with workflow.json
    for workflow_file in workflows_dir.rglob("workflow.json"):
        workflow_dir = workflow_file.parent
        workflow_dirs.append(workflow_dir)

    return sorted(workflow_dirs)


def test_all_workflows_have_required_files():
    """Test: All workflows must have workflow.json and README.md"""

    missing_files = []

    for workflow_dir in get_workflow_directories():
        workflow_json = workflow_dir / "workflow.json"
        readme_md = workflow_dir / "README.md"

        issues = []
        if not workflow_json.exists():
            issues.append("missing workflow.json")
        if not readme_md.exists():
            issues.append("missing README.md")

        if issues:
            missing_files.append({
                "path": str(workflow_dir.relative_to(workflow_dir.parent.parent.parent / "workflows")),
                "issues": issues
            })

    if missing_files:
        error_msg = "Workflows with missing required files:\n"
        for item in missing_files:
            error_msg += f"  {item['path']}: {', '.join(item['issues'])}\n"
        raise AssertionError(error_msg)

    print(f"[OK] All {len(get_workflow_directories())} workflows have required files (workflow.json + README.md)")


def test_workflow_json_is_valid():
    """Test: All workflow.json files must be valid JSON"""

    invalid_files = []

    for workflow_dir in get_workflow_directories():
        workflow_json = workflow_dir / "workflow.json"

        try:
            with open(workflow_json, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            invalid_files.append({
                "path": str(workflow_json.relative_to(workflow_json.parent.parent.parent / "workflows")),
                "error": str(e)
            })
        except Exception as e:
            invalid_files.append({
                "path": str(workflow_json.relative_to(workflow_json.parent.parent.parent / "workflows")),
                "error": str(e)
            })

    if invalid_files:
        error_msg = "Invalid JSON files:\n"
        for item in invalid_files:
            error_msg += f"  {item['path']}: {item['error']}\n"
        raise AssertionError(error_msg)

    print(f"[OK] All {len(get_workflow_directories())} workflow.json files are valid JSON")


def test_readme_contains_required_sections():
    """Test: All README.md must contain required documentation sections"""

    required_sections = ["Description", "Purpose", "Trigger", "Setup"]
    missing_sections = []

    for workflow_dir in get_workflow_directories():
        readme_md = workflow_dir / "README.md"

        try:
            with open(readme_md, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            missing_sections.append({
                "path": str(readme_md.relative_to(readme_md.parent.parent.parent / "workflows")),
                "error": str(e)
            })
            continue

        missing = []
        for section in required_sections:
            if f"## {section}" not in content and section not in content:
                missing.append(section)

        if missing:
            missing_sections.append({
                "path": str(readme_md.relative_to(readme_md.parent.parent.parent / "workflows")),
                "missing_sections": missing
            })

    if missing_sections:
        error_msg = "READMEs with missing required sections:\n"
        for item in missing_sections:
            if "error" in item:
                error_msg += f"  {item['path']}: Error - {item['error']}\n"
            else:
                error_msg += f"  {item['path']}: Missing {', '.join(item['missing_sections'])}\n"
        raise AssertionError(error_msg)

    print(f"[OK] All {len(get_workflow_directories())} README.md files contain required sections")


def test_optional_files_naming():
    """Test: Optional files follow naming conventions (warning only, not enforced)"""

    optional_files = {
        "template.json": "template",
        "test.json": "test",
        "config.json": "config",
        "CHANGELOG.md": "changelog"
    }

    found_optional = 0

    for workflow_dir in get_workflow_directories():
        for filename in optional_files.keys():
            if (workflow_dir / filename).exists():
                found_optional += 1

    print(f"[INFO] Found {found_optional} optional files across workflows (not enforced)")


if __name__ == '__main__':
    print("Running workflow structure validation tests...\n")

    try:
        test_all_workflows_have_required_files()
        test_workflow_json_is_valid()
        test_readme_contains_required_sections()
        test_optional_files_naming()

        print("\n" + "="*70)
        print("ALL TESTS PASSED!")
        print("="*70)
    except AssertionError as e:
        print("\n" + "="*70)
        print("TEST FAILED!")
        print("="*70)
        print(str(e))
        exit(1)
