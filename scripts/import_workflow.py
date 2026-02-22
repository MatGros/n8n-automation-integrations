import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Import a new n8n workflow into the inbox.")
    parser.add_argument("file", help="Path to the JSON workflow file to import")
    parser.add_argument("--no-tests", action="store_true", help="Skip running quality tests")
    args = parser.parse_args()

    source_file = Path(args.file)
    if not source_file.exists():
        print(f"Error: File '{source_file}' does not exist.")
        sys.exit(1)

    if source_file.suffix.lower() != '.json':
        print(f"Error: File '{source_file}' is not a JSON file.")
        sys.exit(1)

    # Create inbox directory if it doesn't exist
    inbox_dir = Path("workflows/inbox")
    inbox_dir.mkdir(parents=True, exist_ok=True)

    # Convert filename to kebab-case but preserve _STATUS_DATE suffix
    stem = source_file.stem
    import re

    # Extract suffix if present (e.g., _PUB_20260221, _DEV_20260221)
    suffix_match = re.search(r'(_(?:PUB|DEV|DRF|DEP|ARC)_\d{8})$', stem)
    suffix = suffix_match.group(1) if suffix_match else ""

    if suffix:
        base_name = stem[:-len(suffix)]
    else:
        base_name = stem

    # Replace spaces and underscores with hyphens, convert to lowercase
    kebab_base = base_name.replace(' ', '-').replace('_', '-').lower()
    # Remove multiple hyphens
    kebab_base = re.sub(r'-+', '-', kebab_base)

    # Destination path
    dest_file = inbox_dir / f"{kebab_base}{suffix}.json"

    # Copy or move the file
    if source_file.resolve() != dest_file.resolve():
        print(f"Copying '{source_file}' to '{dest_file}'...")
        shutil.copy2(source_file, dest_file)
    else:
        print(f"File is already in '{inbox_dir}'.")

    # Sanitize the workflow
    print("\n--- Sanitizing Workflow ---")
    sanitize_cmd = [sys.executable, "scripts/sanitize_workflows.py", "--force", str(dest_file)]
    subprocess.run(sanitize_cmd, check=False)

    # Generate Markdown template
    md_file = dest_file.with_suffix('.md')
    if not md_file.exists():
        print(f"\n--- Generating Markdown Template ---")
        try:
            with open(dest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            name = data.get('name', dest_file.stem)
            nodes = data.get('nodes', [])

            md_content = f"# {name}\n\n"
            md_content += "## Description\n\n"
            md_content += "Description of the workflow goes here.\n\n"
            md_content += "## Nodes\n\n"
            for node in nodes:
                node_name = node.get('name', 'Unknown')
                node_type = node.get('type', 'Unknown')
                md_content += f"- **{node_name}** (`{node_type}`)\n"

            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"Created '{md_file}'")
        except Exception as e:
            print(f"Failed to generate Markdown: {e}")

    # Run quality tests
    if not args.no_tests:
        print("\n--- Running Quality Tests ---")
        # We can run pytest specifically on this file by setting an environment variable or just running the tests
        # Since the tests might test all workflows, we can just run pytest and see if it passes.
        # Or we can pass the specific file to a test script if supported.
        # For now, let's run pytest on the tests directory.
        env = os.environ.copy()
        env["WORKFLOW_TO_TEST"] = str(dest_file) # In case tests can use this

        test_cmd = [sys.executable, "-m", "pytest", "scripts/tests/", "-v"]
        result = subprocess.run(test_cmd, env=env, check=False)

        if result.returncode == 0:
            print("\n✅ Quality tests passed!")
        else:
            print("\n❌ Quality tests failed. Please review the errors above.")

    print("\nImport process completed.")

if __name__ == "__main__":
    main()
