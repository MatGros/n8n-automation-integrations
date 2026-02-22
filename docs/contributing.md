# Contributing Guide

_Last updated: 2026-02-19 • Audience: Contributors & Maintainers_

## Welcome

Thank you for your interest in contributing to n8n-automation-integrations! This guide explains how to contribute workflows, documentation, and improvements to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn
- Report issues professionally
- No harassment or discrimination

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/yourusername/n8n-automation-integrations.git
cd n8n-automation-integrations

# Add upstream remote
git remote add upstream https://github.com/original/n8n-automation-integrations.git
```

### 2. Create a Feature Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feat/your-feature-name
# OR for bug fixes
git checkout -b fix/bug-description
# OR for documentation
git checkout -b docs/documentation-update
```

Branch naming convention:
- `feat/` — new workflows or features
- `fix/` — bug fixes
- `docs/` — documentation improvements
- `refactor/` — code restructuring
- `test/` — test additions

### 3. Development Workflow

#### For Workflows

1. **Create locally** in your n8n instance
2. **Test thoroughly** with real data
3. **Export the JSON** to `workflows/` directory
4. **Create README** following the template
5. **Add to staging** directory first (`workflows/staging/`)

#### For Documentation

1. **Edit files** in `docs/` directory
2. **Follow markdown style** from existing docs
3. **Check links** are relative and working
4. **Preview locally** if possible

#### For Code/Scripts

1. **Follow Python style** (PEP 8)
2. **Add unit tests** for new functions
3. **Document functions** with docstrings
4. **Ensure no secrets** are committed

## Workflow Submission Checklist

Before creating a pull request for a workflow:

- [ ] **Naming**
  - [ ] File is in kebab-case: `email-processor-workflow.json`
  - [ ] All nodes have descriptive names: `fetch-gmail`, `classify-email`, etc.
  - [ ] No node named `node-1` or generic names

- [ ] **Documentation**
  - [ ] README.md exists in the workflow directory
  - [ ] Contains: Description, Purpose, Trigger, Process, Output, Setup Requirements
  - [ ] Includes Quick Start section
  - [ ] Has error handling documentation

- [ ] **Colors**
  - [ ] Nodes follow [color-reference.md](./color-reference.md)
  - [ ] Blue = Fetch, Green = Logic, Yellow = Storage, etc.
  - [ ] Complex workflows include color legend

- [ ] **Security**
  - [ ] No hardcoded secrets or API keys
  - [ ] All credentials referenced (not hardcoded)
  - [ ] Input validation documented
  - [ ] Error messages don't leak sensitive info

- [ ] **Testing**
  - [ ] Tested with real data in staging
  - [ ] Error scenarios tested
  - [ ] Performance acceptable (no timeouts)
  - [ ] Execution logs show no warnings

- [ ] **Code Quality**
  - [ ] JSON is valid and formatted
  - [ ] No commented-out nodes
  - [ ] No debug logging left in
  - [ ] Follows workflow-style-guide.md

- [ ] **Integration**
  - [ ] Works with existing credentials
  - [ ] Doesn't conflict with other workflows
  - [ ] External API calls have timeout
  - [ ] Database queries use parameterized statements

## Code Submission Checklist

For Python scripts and code:

- [ ] Code follows PEP 8
- [ ] Functions have docstrings
- [ ] Type hints where applicable
- [ ] Unit tests added/updated
- [ ] All tests pass locally
- [ ] No hardcoded paths or secrets
- [ ] Error handling implemented
- [ ] Comments explain "why" not "what"

Example docstring:

```python
def sanitize_email_input(email: str) -> str:
    """
    Validate and sanitize an email address.

    Args:
        email: Raw email input from user

    Returns:
        Sanitized email string

    Raises:
        ValueError: If email format is invalid

    Example:
        >>> sanitize_email_input("Test@Example.COM")
        'test@example.com'
    """
    if not email or '@' not in email:
        raise ValueError("Invalid email format")
    return email.lower().strip()
```

## Documentation Submission Checklist

For documentation improvements:

- [ ] Markdown is valid
- [ ] Headers are properly formatted (#, ##, ###)
- [ ] Code blocks have language specified
- [ ] Links are relative and working
- [ ] No broken references
- [ ] Grammar and spelling checked
- [ ] Consistent terminology
- [ ] Examples are accurate and tested
- [ ] Related docs cross-referenced

## Making a Pull Request

### 1. Push Your Branch

```bash
# Make commits with clear messages
git commit -m "feat: Add Gmail auto-responder workflow"

# Push to your fork
git push origin feat/your-feature-name
```

### 2. Create PR on GitHub

1. Go to the original repository
2. Click "New Pull Request"
3. Select your branch
4. Fill in the template:

```markdown
## Description
Brief description of what you're adding

## Type
- [ ] New workflow
- [ ] Documentation update
- [ ] Bug fix
- [ ] Code improvement

## Checklist
- [ ] I've followed the style guides
- [ ] I've tested this locally
- [ ] I've added/updated documentation
- [ ] No secrets in my code
- [ ] CI checks pass

## Testing
How to test this change:
1. Import the workflow
2. Set up credentials
3. Send test email
4. Verify draft is created

## Screenshots (if applicable)
Add workflow screenshot or before/after

## Closes
Closes #123 (if applicable)
```

### 3. Respond to Feedback

- Be open to suggestions
- Make requested changes in new commits
- Ask questions if anything is unclear
- Re-request review after updates

## PR Review Process

### What Reviewers Look For

1. **Functionality** — Does it work as intended?
2. **Security** — No exposed secrets or vulnerabilities?
3. **Style** — Follows conventions and guidelines?
4. **Documentation** — Clear and complete?
5. **Testing** — Adequately tested?
6. **Performance** — No unnecessary slowdowns?

### CI/CD Checks

Your PR must pass:

- `validate-pr` — JSON validation, documentation check
- `test` — Unit and integration tests
- `security` — Secret detection, dependency check

View check results on your PR page.

## Running Tests Locally

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_sanitizers.py -v

# Run with coverage
pytest tests/ --cov=scripts --cov-report=html
```

## Project Structure

```
n8n-automation-integrations/
├── workflows/
│   ├── active/          # Production-ready workflows
│   ├── staging/         # Testing workflows
│   ├── templates/       # Reusable templates
│   └── development/     # Work-in-progress
├── docs/
│   ├── by-industry/     # Industry-specific guides
│   ├── by-technology/   # Technology guides
│   └── *.md            # General documentation
├── scripts/
│   ├── validators/      # Validation scripts
│   ├── sanitizers/      # Security tools
│   └── deploy/          # Deployment scripts
├── tests/
│   ├── unit/            # Unit tests
│   ├── integration/      # Integration tests
│   └── smoke/           # Smoke tests
└── README.md
```

## Style Guide References

- **Workflows**: [Workflow Style Guide](./workflow-style-guide.md)
- **Colors**: [Color Reference](./color-reference.md)
- **Editing**: [Workflow Editing Guide](./workflow-editing-guide.md)
- **Security**: [Security Best Practices](./security-best-practices.md)

## Common Questions

### How long does review take?

Typically 1-3 business days. Complex workflows may take longer.

### Can I work on multiple issues?

Yes, in separate branches. Keep PRs focused and manageable.

### What if my PR gets rejected?

No worries! We'll explain why and suggest improvements. You can reopen with changes.

### Can I ask questions while working?

Absolutely! Open a draft PR or discussion to get feedback early.

## Community

- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Report bugs or request features
- **Slack**: Join our community Slack (link in README)
- **Meetings**: Weekly contributor calls (time TBD)

## Licensing

By contributing, you agree your work is licensed under the project's license (check LICENSE file).

## Getting Help

- Read the [FAQ](./faq.md) (if available)
- Check existing issues and PRs
- Ask in GitHub Discussions
- Contact maintainers

## Thank You

We appreciate all contributions, from workflows to typo fixes. Every contribution makes this project better!

---

Happy contributing!
