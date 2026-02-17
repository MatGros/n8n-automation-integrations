from scripts.validators.security_validator import (
    find_emails_in_workflows,
    find_vps_urls_in_workflows,
    find_credential_like_ids_in_workflows,
    find_instance_ids_in_workflows,
    find_webhook_ids_in_workflows,
)


def test_no_hardcoded_emails_in_workflows():
    matches = find_emails_in_workflows()
    assert matches == [], f"Found hard-coded emails in workflows: {matches}"


def test_no_vps_urls_in_workflows():
    matches = find_vps_urls_in_workflows()
    assert matches == [], f"Found VPS URLs in workflows: {matches}"


def test_no_raw_credential_ids_in_workflows():
    matches = find_credential_like_ids_in_workflows()
    assert matches == [], f"Found raw credential-like ids in workflows: {matches}"


def test_no_instance_or_webhook_ids_in_workflows():
    assert find_instance_ids_in_workflows() == []
    assert find_webhook_ids_in_workflows() == []
