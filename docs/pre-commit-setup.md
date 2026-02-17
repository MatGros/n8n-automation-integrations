# Pre-commit setup

This repository includes a `.pre-commit-config.yaml` to help prevent accidental
commits that introduce secrets or broken JSON.

Quick install (developer machine):

1. Install pre-commit:

   ```bash
   pip install pre-commit
   ```

2. Install the git hook in your repo:

   ```bash
   pre-commit install
   ```

3. Run checks against all files (optional):

   ```bash
   pre-commit run --all-files
   ```

Notes:
- The `sanitizer-dry-run` hook runs the sanitizer in `--dry-run` and blocks the
  commit if sensitive values would be changed.
- To fix detected issues, run:

  ```bash
  python scripts/sanitize_workflows.py workflows --force
  ```

- Keep pre-commit updated (`pip install --upgrade pre-commit`) and run hooks
  locally before committing.
