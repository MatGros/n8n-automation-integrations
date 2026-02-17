#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security tests for n8n workflow files and configuration
Validates that no sensitive data is exposed in the repository
"""

import json
import os
import re
from pathlib import Path
import pytest


class TestSecurityScan:
    """Test suite for security scanning of sensitive data"""

    WORKFLOWS_DIR = Path(__file__).parent.parent.parent / "workflows"

    # Patterns for detecting sensitive data
    VPS_URL_PATTERN = r'https?://[a-z0-9\.\-]*srv[a-z0-9\.\-]*\.'
    CREDENTIAL_ID_PATTERN = r'^[a-zA-Z0-9]{16}$'
    INSTANCE_ID_PATTERN = r'^[a-f0-9]{64}$'
    WEBHOOK_UUID_PATTERN = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
    IP_ADDRESS_PATTERN = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def get_workflow_files(self):
        """Get all JSON workflow files"""
        return list(self.WORKFLOWS_DIR.rglob("*.json"))

    def test_01_detect_vps_urls(self):
        """Test: Détection URLs serveurs - no VPS URLs should be found"""
        sensitive_urls = []

        for workflow_file in self.get_workflow_files():
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if re.search(self.VPS_URL_PATTERN, content, re.IGNORECASE):
                        sensitive_urls.append(str(workflow_file))
            except Exception:
                pass

        assert len(sensitive_urls) == 0, f"VPS URLs found in: {sensitive_urls}"

    def test_02_detect_credential_ids(self):
        """Test: Détection credential IDs - should be anonymized as CRED_XXXX

        Uses the JSON-contextual validator to avoid false positives from 16-char
        tokens that are not credential IDs (e.g. property names).
        """
        from scripts.validators.security_validator import find_credential_like_ids_in_workflows

        matches = find_credential_like_ids_in_workflows()
        assert matches == [], f"Found raw credential-like ids in workflows: {matches}"

    def test_03_detect_instance_ids(self):
        """Test: Détection instance IDs - should be removed from JSON"""
        files_with_instance_ids = []

        for workflow_file in self.get_workflow_files():
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    # Check for instanceId key
                    def search_instance_id(obj):
                        if isinstance(obj, dict):
                            if 'instanceId' in obj:
                                return True
                            return any(search_instance_id(v) for v in obj.values())
                        elif isinstance(obj, list):
                            return any(search_instance_id(item) for item in obj)
                        return False

                    if search_instance_id(data):
                        files_with_instance_ids.append(str(workflow_file))
            except Exception:
                pass

        assert len(files_with_instance_ids) == 0, f"InstanceId found in: {files_with_instance_ids}"

    def test_04_detect_webhook_ids(self):
        """Test: Détection webhook IDs - should be removed from nodes"""
        files_with_webhook_ids = []

        for workflow_file in self.get_workflow_files():
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    if isinstance(data, dict) and 'nodes' in data:
                        for node in data.get('nodes', []):
                            if isinstance(node, dict) and 'webhookId' in node:
                                files_with_webhook_ids.append(str(workflow_file))
                                break
            except Exception:
                pass

        assert len(files_with_webhook_ids) == 0, f"WebhookId found in: {files_with_webhook_ids}"

    def test_05_detect_ip_addresses(self):
        """Test: Détection IP addresses - private IPs might indicate config"""
        files_with_ips = []

        for workflow_file in self.get_workflow_files():
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Look for private IP ranges
                    private_ips = re.findall(
                        r'\b(192\.168|10\.|172\.(1[6-9]|2[0-9]|3[01]))\.',
                        content
                    )
                    if private_ips:
                        files_with_ips.append(str(workflow_file))
            except Exception:
                pass

        assert len(files_with_ips) == 0, f"Private IPs found in: {files_with_ips}"

    def test_06_detect_api_tokens(self):
        """Test: Détection tokens/API keys - should be in .env, not JSON"""
        suspicious_patterns = [
            r'api[_-]?key["\']?\s*[:=]',
            r'secret["\']?\s*[:=]',
            r'token["\']?\s*[:=]',
            r'password["\']?\s*[:=]',
        ]

        files_with_tokens = []
        for workflow_file in self.get_workflow_files():
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern in suspicious_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            files_with_tokens.append((str(workflow_file), pattern))
                            break
            except Exception:
                pass

        assert len(files_with_tokens) == 0, f"API keys/tokens found in: {files_with_tokens[:5]}"

    def test_07_detect_personal_emails(self):
        """Test: Détection emails personnels - should use example.com"""
        dangerous_domains = [
            r'@gmail\.com',
            r'@yahoo\.com',
            r'@outlook\.com',
            r'@hotmail\.com',
            r'@protonmail\.com',
        ]

        files_with_personal_emails = []
        for workflow_file in self.get_workflow_files():
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for domain_pattern in dangerous_domains:
                        if re.search(domain_pattern, content, re.IGNORECASE):
                            files_with_personal_emails.append((str(workflow_file), domain_pattern))
                            break
            except Exception:
                pass

        assert len(files_with_personal_emails) == 0, f"Personal emails found in: {files_with_personal_emails[:5]}"


class TestSecurityConfiguration:
    """Test security configuration files"""

    def test_env_example_exists(self):
        """Test: .env.example should exist with safe placeholders"""
        env_file = Path(__file__).parent.parent.parent / ".env.example"
        assert env_file.exists(), ".env.example file not found"

        with open(env_file, 'r') as f:
            content = f.read()
            # Should not contain real credentials
            assert 'your_' in content or 'YOUR_' in content, ".env.example should use placeholders"

    def test_gitignore_has_env_patterns(self):
        """Test: .gitignore should exclude .env and credentials"""
        gitignore_file = Path(__file__).parent.parent.parent / ".gitignore"
        assert gitignore_file.exists(), ".gitignore file not found"

        with open(gitignore_file, 'r') as f:
            content = f.read()
            assert '.env' in content, ".gitignore should exclude .env files"
            assert 'credentials' in content.lower() or 'credential' in content.lower(), \
                ".gitignore should exclude credential files"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
