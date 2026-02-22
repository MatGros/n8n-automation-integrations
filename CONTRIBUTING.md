# Contributing

Thanks for contributing! Follow these steps to make your PR reviewable and mergeable. For the full contributor guide (detailed checklists and examples), see `docs/contributing.md`.

## Local setup
1. Create a virtualenv and install dev deps:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
   pip install -r requirements.txt
   ```

## Before you open a PR
- Run `pre-commit run --all-files` and fix issues.
- Run `pytest -q` and ensure tests pass.
- Run `python scripts/sanitize_workflows.py workflows --dry-run` if you modified workflows.
- Update `docs/` and include `Quick start` + `Process` steps for new workflows.
- Use the PR template and include the `workflow-checklist.md` when applicable.

## PR process
- Create a feature branch named `feature/<short-description>`.
- Open a draft PR if work is in progress; mark Ready when finished.
- Assign reviewers and wait for at least one approval before merging.

## Documentation standards
- Follow `docs/workflow-style-guide.md` for README content and node naming.
- Add examples and a `Quick start` for any new workflow.

Thanks — your contributions keep this project healthy and useful!
