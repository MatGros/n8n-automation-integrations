#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sanitization script for n8n workflows
Removes/anonymizes sensitive data: credential IDs, instance IDs, webhook IDs, etc.
"""

import json
import re
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
import argparse
from copy import deepcopy

# Ensure UTF-8 encoding for output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

class WorkflowSanitizer:
    """Sanitizes n8n workflow files by removing sensitive data"""

    # Patterns to detect sensitive data
    PATTERNS = {
        'credential_id': r'^[a-zA-Z0-9_]{16}$',  # n8n credential IDs are 16 chars alphanumeric
        'instance_id': r'^[a-f0-9]{64}$',  # 64 char hex
        'webhook_id': r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',  # UUID format
    }

    # URLs to anonymize
    VPS_URLS = [
        'https://n8n.srv830801.hstgr.cloud',
        'https://n8n.srv',
    ]

    # Bot names to replace
    BOT_NAMES = {
        'ZedMg_bot': 'my_bot',
    }

    def __init__(self, dry_run: bool = True, verbose: bool = True):
        self.dry_run = dry_run
        self.verbose = verbose
        self.anonymization_map = {}
        self.changes = []

    def log(self, message: str, level: str = "INFO"):
        if self.verbose:
            print(f"[{level}] {message}")

    def anonymize_credential_id(self, cred_id: str) -> str:
        """Generate consistent anonymous credential ID"""
        if cred_id not in self.anonymization_map:
            self.anonymization_map[cred_id] = f"CRED_{len(self.anonymization_map):04d}"
        return self.anonymization_map[cred_id]

    def sanitize_url(self, text: str) -> str:
        """Replace VPS URLs with placeholder"""
        for url in self.VPS_URLS:
            if url in text:
                self.changes.append(f"Removed VPS URL: {url}")
                return text.replace(url, "https://your-n8n-instance.com")
        return text

    def sanitize_bot_name(self, text: str) -> str:
        """Replace bot names"""
        for old_name, new_name in self.BOT_NAMES.items():
            if old_name in text:
                self.changes.append(f"Anonymized bot name: {old_name} → {new_name}")
                return text.replace(old_name, new_name)
        return text

    def sanitize_value(self, key: str, value: Any) -> Any:
        """Sanitize a single value based on context"""
        if not isinstance(value, str):
            return value

        # Sanitize URLs
        if key and ('url' in key.lower() or 'host' in key.lower()):
            return self.sanitize_url(value)

        # Sanitize credential IDs ONLY (not workflow IDs!)
        # n8n credential IDs: exactly 16 alphanumeric chars, only in 'credentials.*.id' context
        if key and key.lower() == 'id' and len(value) == 16 and value.isalnum() and value not in ['CRED_0000', 'CRED_0001']:
            return self.anonymize_credential_id(value)

        # Sanitize instance IDs
        if key and 'instanceid' in key.lower() and len(value) == 64:
            return "INSTANCE_ID_REMOVED"

        # Sanitize webhook IDs
        if key and 'webhookid' in key.lower() and self.is_uuid(value):
            return "WEBHOOK_ID_REMOVED"

        # Sanitize bot names
        for old_name, new_name in self.BOT_NAMES.items():
            if old_name in value:
                return self.sanitize_bot_name(value)

        return value

    @staticmethod
    def is_uuid(value: str) -> bool:
        """Check if value is a UUID format"""
        uuid_pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
        return bool(re.match(uuid_pattern, value))

    def sanitize_json(self, data: Dict[str, Any], key: str = None, parent_key: str = None, depth: int = 0) -> Dict[str, Any]:
        """Recursively sanitize JSON data
        depth: 0 = root level, 1+ = nested
        """
        if isinstance(data, dict):
            result = {}
            for k, value in data.items():
                # Skip instanceId entirely (remove from JSON)
                if k.lower() == 'instanceid':
                    self.changes.append("Removed instanceId from meta")
                    continue
                result[k] = self.sanitize_json(value, k, key, depth + 1)
            return result
        elif isinstance(data, list):
            return [self.sanitize_json(item, key, parent_key, depth) for item in data]
        elif isinstance(data, str):
            # Don't sanitize root-level 'id' (it's the workflow ID, not a credential ID)
            if key == 'id' and depth == 1:
                return data
            return self.sanitize_value(key, data)
        else:
            return data

    def sanitize_workflow_file(self, filepath: str) -> Dict[str, Any]:
        """Load, sanitize, and return workflow data"""
        self.log(f"Processing: {filepath}")
        self.changes.clear()

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.log(f"Failed to parse JSON: {e}", "ERROR")
            return None

        # Make a copy to avoid modifying original during dry-run
        sanitized = deepcopy(data)

        # Sanitize the data
        sanitized = self.sanitize_json(sanitized)

        # Remove webhookId fields entirely (they shouldn't be in repo)
        # Only from nodes, not from other places
        if 'nodes' in sanitized:
            for node in sanitized['nodes']:
                if 'webhookId' in node:
                    self.changes.append(f"Removed webhookId from node '{node.get('name', 'unknown')}'")
                    del node['webhookId']

        return sanitized

    def process_file(self, filepath: str) -> bool:
        """Process a single workflow file"""
        sanitized = self.sanitize_workflow_file(filepath)

        if sanitized is None:
            return False

        if self.changes:
            self.log(f"Changes detected in {filepath}:", "INFO")
            for change in self.changes:
                self.log(f"  - {change}")

            if not self.dry_run:
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(sanitized, f, indent=2, ensure_ascii=False)
                    self.log(f"✓ Saved: {filepath}", "SUCCESS")
                except IOError as e:
                    self.log(f"Failed to save: {e}", "ERROR")
                    return False
            else:
                self.log(f"[DRY-RUN] Would save: {filepath}", "INFO")
        else:
            self.log(f"No changes needed: {filepath}", "OK")

        return True

    def process_directory(self, directory: str, pattern: str = "*.json") -> int:
        """Process all workflow files in directory"""
        workflow_files = list(Path(directory).rglob(pattern))

        if not workflow_files:
            self.log(f"No workflow files found in {directory}", "WARNING")
            return 0

        self.log(f"Found {len(workflow_files)} workflow files", "INFO")

        success_count = 0
        for filepath in workflow_files:
            if self.process_file(str(filepath)):
                success_count += 1

        return success_count


def main():
    parser = argparse.ArgumentParser(description='Sanitize n8n workflow files')
    parser.add_argument('path', nargs='?', default='workflows',
                        help='Path to workflow file or directory (default: workflows)')
    parser.add_argument('--dry-run', action='store_true', default=True,
                        help='Show changes without writing (default: enabled)')
    parser.add_argument('--force', action='store_true',
                        help='Actually write changes (disable dry-run)')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress verbose output')

    args = parser.parse_args()

    # Determine if path is file or directory
    path = Path(args.path)

    if not path.exists():
        print(f"Error: Path not found: {args.path}")
        return 1

    sanitizer = WorkflowSanitizer(
        dry_run=not args.force,
        verbose=not args.quiet
    )

    if path.is_file():
        success = sanitizer.process_file(str(path))
    else:
        success = sanitizer.process_directory(str(path)) > 0

    if args.dry_run and not args.force:
        print("\n[INFO] This was a DRY-RUN. Use --force to apply changes.")

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
