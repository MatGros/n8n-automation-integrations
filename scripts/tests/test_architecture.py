from scripts.validators.architecture_validator import (
    find_missing_categories,
    categories_without_readme,
    find_non_kebab_paths,
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
