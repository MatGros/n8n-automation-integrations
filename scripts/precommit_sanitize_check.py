#!/usr/bin/env python3
"""Pre-commit wrapper: run the sanitizer in dry-run and fail if any changes would be applied.
Exits with code 1 if sanitizer reports changes.
"""
import subprocess
import sys

def main():
    cmd = [sys.executable, "scripts/sanitize_workflows.py", "workflows", "--dry-run"]
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except Exception as e:
        print(f"[precommit] Failed to run sanitizer: {e}")
        return 1

    out = completed.stdout + completed.stderr
    # sanitizer prints lines like: "[DRY-RUN] Would save: <path>"
    if "Would save:" in out or "Changes detected" in out or "Removed webhookId" in out:
        print("[precommit] Sanitizer detected changes that must be applied before commit:")
        # show relevant lines
        for line in out.splitlines():
            if "Would save:" in line or "Removed" in line or "Anonymized" in line:
                print(line)
        print("\nRun: python scripts/sanitize_workflows.py workflows --force  OR fix the offending files before committing.")
        return 1

    print("[precommit] Sanitizer dry-run: no changes detected.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
