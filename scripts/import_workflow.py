import argparse
import json
import os
import shutil
import subprocess
import sys
import re
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Import a new n8n workflow into the inbox.")
    parser.add_argument("file", help="Path to the JSON workflow file to import")
    parser.add_argument("--no-tests", action="store_true", help="Skip running quality tests")
    parser.add_argument("--no-gen", action="store_true", help="Do not generate markdown or metadata files")
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
    orig_stem = stem  # keep original for title generation

    # Extract suffix if present (e.g., _PUB_20260221, _DEV_20260221)
    suffix_match = re.search(r'(_(?:PUB|DEV|DRF|DEP|ARC)_\d{8})$', stem)
    suffix = suffix_match.group(1) if suffix_match else ""

    # compute kebab destination name in advance to warn user
    # remove suffix before normalizing so we append it only once
    base_without_suffix = orig_stem
    if suffix and base_without_suffix.endswith(suffix):
        base_without_suffix = base_without_suffix[: -len(suffix)]
    temp_kebab = base_without_suffix.replace(' ', '-').replace('_', '-').lower()
    temp_kebab = re.sub(r'[^a-z0-9-]', '-', temp_kebab)
    temp_kebab = re.sub(r'-+', '-', temp_kebab)
    dest_name = f"{temp_kebab}{suffix}.json"
    if dest_name != source_file.name:
        print(f"⚠️  Source filename does not respect kebab-case:")
        print(f"    {source_file.name}")
        print(f"It will be renamed to: {dest_name}")
        ans = input("Proceed with rename? (Y/n): ").strip().lower()
        if ans == 'n':
            print("Import aborted. Please rename the file manually.")
            sys.exit(1)

    # Extract suffix if present (e.g., _PUB_20260221, _DEV_20260221)
    suffix_match = re.search(r'(_(?:PUB|DEV|DRF|DEP|ARC)_\d{8})$', stem)
    suffix = suffix_match.group(1) if suffix_match else ""

    if suffix:
        base_name = stem[:-len(suffix)]
    else:
        base_name = stem

    # Replace spaces and underscores with hyphens, convert to lowercase
    kebab_base = base_name.replace(' ', '-').replace('_', '-').lower()
    # Replace any character that is not lowercase letter, digit or hyphen
    kebab_base = re.sub(r'[^a-z0-9-]', '-', kebab_base)
    # Collapse consecutive hyphens
    kebab_base = re.sub(r'-+', '-', kebab_base)

    # Destination path
    dest_file = inbox_dir / f"{kebab_base}{suffix}.json"

    # Copy or move the file
    removed_original = False
    if source_file.resolve() != dest_file.resolve():
        print(f"Copying '{source_file}' to '{dest_file}'...")
        shutil.copy2(source_file, dest_file)
        # ask user whether to delete original
        delete_ans = input(f"Remove original file '{source_file.name}'? (y/N): ").strip().lower()
        if delete_ans == 'y':
            try:
                source_file.unlink()
                removed_original = True
                print(f"Removed original file '{source_file}' after import")
            except Exception:
                print(f"Warning: could not remove source file '{source_file}'")
        else:
            print("Original file left in place.")
        # check for an unsanitized markdown file
        orig_md = inbox_dir / (source_file.stem + '.md')
        if orig_md.exists():
            print(f"⚠️  Found a non‑kebab markdown file '{orig_md.name}' in inbox.")
            answer = input("Delete it? (y/N): ").strip().lower()
            if answer == 'y':
                try:
                    orig_md.unlink()
                    print(f"Deleted {orig_md.name}")
                except Exception:
                    print(f"Failed to delete {orig_md.name}")
            else:
                print("Please handle or rename the file manually before running tests.")
    else:
        print(f"File is already in '{inbox_dir}'.")

    # Sanitize the workflow
    print("\n--- Sanitizing Workflow ---")
    sanitize_cmd = [sys.executable, "scripts/sanitize_workflows.py", "--force", str(dest_file)]
    subprocess.run(sanitize_cmd, check=False)

    if not args.no_gen:
        # Generate Markdown template
        md_file = dest_file.with_suffix('.md')
        if not md_file.exists():
            print(f"\n--- Generating Markdown Template ---")
            try:
                with open(dest_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # choose heading: prefer original filename cleaned, fallback to workflow name
                def clean_title(s):
                    # remove status suffix if present
                    t = re.sub(r'_(PUB|DEV|DRF|DEP|ARC)_\d{8}$', '', s)
                    t = t.replace('-', ' ').replace('_', ' ')
                    return t.strip()
                name = clean_title(orig_stem) or data.get('name', dest_file.stem)
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

        # Generate metadata stub if none exists
        metadata_file = dest_file.with_name(dest_file.stem + '.metadata.json')
        if not metadata_file.exists():
            print(f"\n--- Generating metadata.json stub ---")
            try:
                # ensure we have the workflow data
                try:
                    with open(dest_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception:
                    data = {}

                # reuse data from workflow, but populate schema‑safe placeholders
                meta = {
                    "name": data.get('name', dest_file.stem),
                    # default to a generic category; user should update when relocating
                    "category": "99-templates",
                    "version": "1.0.0",
                    "status": "development",
                    # at least one credential placeholder (must be non-empty)
                    "required_credentials": ["replace-with-credential"],
                    # minimum two tags required by schema
                    "tags": ["placeholder", "to-edit"]
                }
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(meta, f, indent=2, ensure_ascii=False)
                print(f"Created '{metadata_file}' (update fields before moving the workflow)")
            except Exception as e:
                print(f"Failed to create metadata: {e}")
    # prefer per-file metadata to avoid collisions in inbox; use <base>.metadata.json
    metadata_file = dest_file.with_name(dest_file.stem + '.metadata.json')
    if not metadata_file.exists():
        print(f"\n--- Generating metadata.json stub ---")
        print(f"metadata target path is: {metadata_file}")
        try:
            # ensure we have the workflow data
            try:
                with open(dest_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception:
                data = {}

            # reuse data from workflow, but populate schema‑safe placeholders
            meta = {
                "name": data.get('name', dest_file.stem),
                # default to a generic category; user should update when relocating
                "category": "99-templates",
                "version": "1.0.0",
                "status": "development",
                # at least one credential placeholder (must be non-empty)
                "required_credentials": ["replace-with-credential"],
                # minimum two tags required by schema
                "tags": ["placeholder", "to-edit"]
            }
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
            print(f"Created '{metadata_file}' (update fields before moving the workflow)")
        except Exception as e:
            print(f"Failed to create metadata: {e}")

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
