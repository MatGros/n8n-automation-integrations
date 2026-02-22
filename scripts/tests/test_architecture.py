from scripts.validators.architecture_validator import (
    find_missing_categories,
    categories_without_readme,
    find_non_kebab_paths,
)
from scripts.validators.metadata_validator import (
    find_workflows_missing_metadata,
    validate_metadata_files,
)


def test_all_categories_present():
    missing = find_missing_categories()
    assert missing == [], f"Missing expected workflow categories: {missing}"


def test_readme_present_in_all_categories():
    missing = categories_without_readme()
    assert missing == [], f"Categories missing README.md: {missing}"


def test_workflow_and_dir_naming_kebab_case():
    bad = find_non_kebab_paths()
    assert bad == [], f"Non-kebab file/dir names found: {bad}"


def test_metadata_present_for_all_workflows():
    missing = find_workflows_missing_metadata()
    assert missing == [], f"Workflows missing metadata.json: {missing}"


def test_metadata_valid_against_schema():
    errors = validate_metadata_files()
    assert not errors, f"Metadata schema violations: {errors}"
