# CI/CD Setup Guide

## Purpose

This guide documents the continuous integration and continuous deployment (CI/CD) setup for automated testing, security scanning, and deployment of n8n workflows. Automated workflows ensure quality, security, and reliability across all environments.

## Overview

The CI/CD pipeline consists of:

1. **Source Control**: GitHub (with branch protection)
2. **Continuous Integration**: GitHub Actions (automated tests)
3. **Security Scanning**: Automated secret detection, dependency scanning
4. **Deployment Automation**: Automated workflow imports and configuration
5. **Monitoring**: Post-deployment health checks

## GitHub Actions Workflow

### Workflow Structure

Create `.github/workflows/` directory with these workflows:

#### 1. Pull Request Validation (`validate-pr.yml`)

```yaml
name: Validate PR

on:
  pull_request:
    paths:
      - 'workflows/**'
      - 'docs/**'
      - 'scripts/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r scripts/requirements.txt

      - name: Validate JSON
        run: |
          python scripts/validators/json_validator.py workflows/

      - name: Check for secrets
        run: |
          python scripts/sanitize_workflows.py --dry-run

      - name: Validate documentation
        run: |
          python scripts/validators/documentation_validator.py workflows/

      - name: Run tests
        run: |
          pytest tests/ -v

      - name: Check formatting
        run: |
          pytest tests/test_style.py -v
```

#### 2. Automated Testing (`test.yml`)

```yaml
name: Test Workflows

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run unit tests
        run: |
          pytest tests/unit/ -v --cov=scripts

      - name: Run integration tests
        run: |
          pytest tests/integration/ -v
        env:
          TEST_DB_URL: postgresql://postgres:postgres@localhost/n8n_test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

#### 3. Security Scanning (`security.yml`)

```yaml
name: Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Run GitLeaks (Secret Detection)
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Dependency Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          path: '.'
          format: 'JSON'

      - name: Upload security results
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            dependency-check-report.json

      - name: Check for hardcoded credentials
        run: |
          python scripts/sanitize_workflows.py --dry-run
```

#### 4. Deployment to Staging (`deploy-staging.yml`)

```yaml
name: Deploy to Staging

on:
  push:
    branches: [develop]
    paths:
      - 'workflows/staging/**'
  workflow_dispatch:  # Allow manual trigger

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install n8n CLI
        run: |
          npm install -g n8n

      - name: Deploy workflows
        env:
          N8N_API_URL: ${{ secrets.STAGING_N8N_URL }}
          N8N_API_KEY: ${{ secrets.STAGING_N8N_API_KEY }}
        run: |
          python scripts/deploy_workflows.py \
            --environment staging \
            --workflows workflows/staging/

      - name: Run smoke tests
        env:
          STAGING_N8N_URL: ${{ secrets.STAGING_N8N_URL }}
          STAGING_N8N_API_KEY: ${{ secrets.STAGING_N8N_API_KEY }}
        run: |
          pytest tests/smoke/ -v

      - name: Notify Slack
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
          payload: |
            {
              "text": "Staging deployment: ${{ job.status }}",
              "channel": "#n8n-deployments"
            }
```

#### 5. Deployment to Production (`deploy-production.yml`)

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
    paths:
      - 'workflows/active/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Generate changelog
        run: |
          python scripts/generate_changelog.py > DEPLOYMENT_NOTES.md

      - name: Deploy to production
        env:
          N8N_API_URL: ${{ secrets.PROD_N8N_URL }}
          N8N_API_KEY: ${{ secrets.PROD_N8N_API_KEY }}
        run: |
          python scripts/deploy_workflows.py \
            --environment production \
            --workflows workflows/active/ \
            --backup

      - name: Health check
        run: |
          python scripts/health_check.py \
            --url ${{ secrets.PROD_N8N_URL }} \
            --timeout 300

      - name: Notify deployment
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
          payload: |
            {
              "text": "Production deployment completed: ${{ job.status }}",
              "channel": "#n8n-alerts",
              "attachments": [
                {
                  "text": "${{ github.event.head_commit.message }}"
                }
              ]
            }
```

## GitHub Secrets Configuration

### Required Secrets

Set up these secrets in GitHub (Settings → Secrets and variables → Actions):

```
# n8n Instances
STAGING_N8N_URL = https://staging-n8n.example.com
STAGING_N8N_API_KEY = sk_staging_...

PROD_N8N_URL = https://prod-n8n.example.com
PROD_N8N_API_KEY = sk_prod_...

# Notifications
SLACK_WEBHOOK_URL = https://hooks.slack.com/services/T.../B.../X...

# Other integrations
OPENAI_API_KEY = sk-...
GMAIL_CREDENTIALS_B64 = base64-encoded-json
```

## Branch Protection Rules

Configure branch protection for `main` and `develop`:

1. Go to Settings → Branches
2. Add rule for `main`:
   - Require PR reviews: Yes (≥1)
   - Require status checks to pass:
     - validate-pr
     - test
     - security
   - Require branches to be up to date
   - Include administrators

3. Add rule for `develop`:
   - Same as above but allow auto-merge after review

## Testing Strategy

### Unit Tests

File: `tests/unit/test_transformations.py`

```python
import pytest
from scripts.transformers import format_email_body

def test_format_email_body():
    """Test email formatting"""
    input_data = {
        "subject": "Test",
        "body": "Hello <name>"
    }
    result = format_email_body(input_data, {"name": "John"})
    assert "Hello John" in result
    assert "<name>" not in result

def test_sanitize_input():
    """Test input sanitization"""
    from scripts.sanitizers import sanitize_sql_input

    malicious = "'; DROP TABLE users; --"
    result = sanitize_sql_input(malicious)
    assert "DROP" not in result
```

### Integration Tests

File: `tests/integration/test_workflows.py`

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def n8n_client():
    """Mock n8n API client"""
    return Mock()

def test_workflow_execution(n8n_client):
    """Test workflow execution flow"""
    n8n_client.execute_workflow.return_value = {
        "status": "success",
        "data": {"email_count": 5}
    }

    result = n8n_client.execute_workflow("gmail-processor")
    assert result["status"] == "success"
    assert result["data"]["email_count"] == 5

@patch('requests.post')
def test_slack_notification(mock_post):
    """Test Slack notification sending"""
    from scripts.notifiers import send_slack_notification

    send_slack_notification("Test", "#test")

    mock_post.assert_called_once()
    args = mock_post.call_args
    assert "Test" in str(args)
```

### Smoke Tests

File: `tests/smoke/test_production.py`

```python
def test_n8n_health():
    """Verify n8n instance is healthy"""
    import requests
    response = requests.get(
        f"{os.getenv('PROD_N8N_URL')}/api/health"
    )
    assert response.status_code == 200

def test_workflow_list():
    """Verify workflows are accessible"""
    import requests
    response = requests.get(
        f"{os.getenv('PROD_N8N_URL')}/api/workflows",
        headers={"X-N8N-API-KEY": os.getenv('PROD_N8N_API_KEY')}
    )
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0
```

## Deployment Scripts

### Deploy Workflows (`scripts/deploy_workflows.py`)

```python
#!/usr/bin/env python3
import argparse
import json
import requests
import os
from pathlib import Path

def deploy_workflows(environment, workflows_path, backup=False):
    """Deploy workflows to n8n instance"""

    api_url = os.getenv(f'{environment.upper()}_N8N_URL')
    api_key = os.getenv(f'{environment.upper()}_N8N_API_KEY')

    headers = {
        'X-N8N-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    workflow_files = Path(workflows_path).glob('*.json')

    for workflow_file in workflow_files:
        with open(workflow_file, 'r') as f:
            workflow_data = json.load(f)

        # Create backup if requested
        if backup:
            backup_path = f"backups/{environment}/{workflow_file.name}"
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            with open(backup_path, 'w') as f:
                json.dump(workflow_data, f, indent=2)

        # Deploy to n8n
        response = requests.post(
            f'{api_url}/api/workflows',
            json=workflow_data,
            headers=headers
        )

        if response.status_code == 200:
            print(f"✓ Deployed {workflow_file.name}")
        else:
            print(f"✗ Failed to deploy {workflow_file.name}: {response.text}")
            raise Exception(f"Deployment failed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--environment', required=True)
    parser.add_argument('--workflows', required=True)
    parser.add_argument('--backup', action='store_true')
    args = parser.parse_args()

    deploy_workflows(args.environment, args.workflows, args.backup)
```

## Health Checks

### Monitoring Script (`scripts/health_check.py`)

```python
#!/usr/bin/env python3
import requests
import time
import sys

def check_health(url, timeout=300):
    """Check n8n instance health"""
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(f'{url}/api/health', timeout=10)
            if response.status_code == 200:
                print("✓ n8n instance healthy")
                return True
        except Exception as e:
            print(f"Health check attempt failed: {e}")
            time.sleep(10)

    print("✗ Health check timeout")
    return False

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--timeout', type=int, default=300)
    args = parser.parse_args()

    success = check_health(args.url, args.timeout)
    sys.exit(0 if success else 1)
```

## Monitoring and Alerts

### Slack Integration

Post deployment status to Slack channel:

```
Channel: #n8n-deployments
Alerts: #n8n-alerts
```

### Dashboard

Consider setting up a monitoring dashboard to track:
- Deployment frequency
- Failure rate
- Lead time
- Mean time to recovery (MTTR)

## Rollback Strategy

If a deployment fails:

```yaml
name: Rollback Production

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Git commit to rollback to'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          ref: ${{ github.event.inputs.version }}

      - name: Deploy previous version
        env:
          N8N_API_URL: ${{ secrets.PROD_N8N_URL }}
          N8N_API_KEY: ${{ secrets.PROD_N8N_API_KEY }}
        run: |
          python scripts/deploy_workflows.py \
            --environment production \
            --workflows workflows/active/

      - name: Notify team
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
          payload: |
            {
              "text": "⚠️ Production rollback completed to ${{ github.event.inputs.version }}"
            }
```

## Related Documentation

- [Deployment Guide](./deployment-guide.md) — Manual deployment procedures
- [Security Best Practices](./security-best-practices.md) — Security in pipelines
- [Contributing Guide](./contributing.md) — PR requirements
