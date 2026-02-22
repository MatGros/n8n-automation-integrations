# Workflow PR Checklist (copy into PR description)

_Last updated: 2026-02-19 • Audience: Contributors & Maintainers_

Use this checklist when opening or reviewing PRs that add or change workflows.

## Required (must pass)
- [ ] README: `Description`, `Purpose`, `Trigger`, `Process`, `Output`, `Setup Requirements`
- [ ] `workflow.json` present and valid JSON
- [ ] `workflow.json` contains top-level `name`
- [ ] All major nodes have meaningful `name` values (not `node-1`)
- [ ] No credentials or sensitive values committed
- [ ] `scripts/tests` updated (unit tests for major validators when applicable)

## Recommended (should do)
- [ ] Add `Quick start` instructions in README
- [ ] Add example `test.json` for automated tests
- [ ] Add `CHANGELOG.md` if behavior changes
- [ ] Add screenshots / short demo GIF for complex flows

## QA steps
1. Import `workflow.json` into a local n8n instance (or use `development/` copy)
2. Verify triggers fire correctly
3. Validate outputs and side effects
4. Run `pytest` locally and ensure all tests pass

---

Copy-paste this checklist into your PR description and check items before requesting review.
