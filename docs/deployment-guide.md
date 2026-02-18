# Deployment Guide

## Purpose

This guide covers the complete workflow for deploying n8n workflows from development to production, including setup, configuration, testing, and backup strategies.

## Prerequisites

- n8n instance running (Docker, self-hosted, or cloud)
- Git access to the repository
- API key for n8n (for automated deployments)
- Access to any external services (Gmail, Slack, databases, etc.)

## Deployment Phases

### Phase 1: Local Development Setup

#### 1.1 Install n8n Locally

```bash
# Using npm
npm install -g n8n

# Using Docker
docker run -it --rm --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n:latest

# Start n8n
n8n start
```

#### 1.2 Clone and Explore Workflows

```bash
# Clone the repository
git clone https://github.com/yourusername/n8n-automation-integrations.git
cd n8n-automation-integrations

# Review the workflow directory structure
ls -la workflows/
ls -la workflows/active/
```

#### 1.3 Import a Workflow

1. Open n8n UI (http://localhost:5678)
2. Click "Import from file" in the main menu
3. Select a workflow JSON from `workflows/active/`
4. Click "Import"

### Phase 2: Development & Testing

#### 2.1 Configure Credentials

1. Go to Settings → Credentials
2. For each external service (Gmail, Slack, OpenAI, etc.):
   - Click "New credential"
   - Select the credential type
   - Enter connection details from your `.env` file (NEVER hardcode)
   - Test the connection
   - Save

#### 2.2 Test the Workflow

```
1. Open the imported workflow
2. For each node:
   - Verify input data format
   - Test node execution (right-click → Execute)
   - Check output structure
3. Test error scenarios:
   - Missing inputs
   - Invalid credentials
   - Network failures
4. Document expected vs. actual behavior
```

#### 2.3 Validate Against Style Guide

Before moving to staging, ensure:
- [ ] All nodes follow naming convention: `verb-resource[-detail]`
- [ ] Color-coded correctly per [color-reference.md](./color-reference.md)
- [ ] No hardcoded secrets or API keys
- [ ] README with Description, Purpose, Trigger, Process, Output, Setup
- [ ] Error handling documented
- [ ] Performance acceptable (no timeouts, infinite loops)

#### 2.4 Run Security Checks

```bash
# Check for exposed secrets
python scripts/sanitize_workflows.py --dry-run workflows/active/your-workflow.json

# Verify no credentials in JSON
grep -i "password\|token\|secret\|key" workflows/active/your-workflow.json
```

### Phase 3: Staging Deployment

#### 3.1 Prepare for Staging

```bash
# Create a staging branch
git checkout -b feat/your-workflow-staging

# Add workflow to staging directory
cp workflows/active/your-workflow.json workflows/staging/

# Create PR with checklist
git add workflows/staging/your-workflow.json
git commit -m "feat: Add workflow to staging for testing"
git push origin feat/your-workflow-staging
```

#### 3.2 Deploy to Staging Environment

If you have a separate staging n8n instance:

```bash
# Using n8n API
curl -X POST http://staging-n8n:5678/api/workflows \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d @workflows/staging/your-workflow.json
```

Or manually via UI on staging instance.

#### 3.3 Run Integration Tests

```bash
# Example: Test email workflow
# 1. Send test email to your address
# 2. Verify workflow triggers correctly
# 3. Check output (draft email created, etc.)
# 4. Verify no errors in execution log

# Run automated tests if available
pytest tests/integration/test_email_workflows.py
```

#### 3.4 Load Testing (if applicable)

For workflows handling high volume:

```bash
# Simulate concurrent executions
ab -n 100 -c 10 http://staging-n8n:5678/webhook/your-workflow

# Monitor resource usage during test
watch 'curl http://staging-n8n:5678/api/health'
```

### Phase 4: Production Deployment

#### 4.1 Pre-Production Checklist

Before deploying to production:

- [ ] All tests pass in staging
- [ ] Stakeholders approved the workflow
- [ ] Credentials updated for production environment
- [ ] Backup strategy in place
- [ ] Monitoring/alerting configured
- [ ] Rollback plan documented
- [ ] Change log updated

#### 4.2 Deploy to Production

**Option A: Via API (Recommended)**

```bash
# Get workflow from staging
WORKFLOW_ID=$(curl -s http://staging-n8n:5678/api/workflows \
  -H "X-N8N-API-KEY: $STAGING_API_KEY" \
  | jq -r '.data[] | select(.name == "Your Workflow") | .id')

# Export workflow JSON
curl -s http://staging-n8n:5678/api/workflows/$WORKFLOW_ID \
  -H "X-N8N-API-KEY: $STAGING_API_KEY" > workflow.json

# Import to production
curl -X POST http://prod-n8n:5678/api/workflows \
  -H "X-N8N-API-KEY: $PROD_API_KEY" \
  -H "Content-Type: application/json" \
  -d @workflow.json
```

**Option B: Via UI**

1. Login to production n8n instance
2. Click "Import from file"
3. Select the workflow JSON
4. Verify all nodes are present
5. Configure production credentials
6. Test execution

#### 4.3 Enable Monitoring

```javascript
// Add notification on workflow failure
// In your error handling node:
await notifySlack({
  channel: '#n8n-alerts',
  text: `Production workflow failed: ${workflowName}`,
  color: 'danger'
});
```

### Phase 5: Backup & Recovery

#### 5.1 Backup Workflows Regularly

```bash
# Backup all workflows to JSON files
for workflow_id in $(curl -s http://prod-n8n:5678/api/workflows \
  -H "X-N8N-API-KEY: $PROD_API_KEY" \
  | jq -r '.data[].id'); do
  curl -s http://prod-n8n:5678/api/workflows/$workflow_id \
    -H "X-N8N-API-KEY: $PROD_API_KEY" > backup_$workflow_id.json
done

# Commit backups to git (weekly)
git add backups/
git commit -m "chore: Weekly workflow backup $(date +%Y-%m-%d)"
git push origin main
```

#### 5.2 Database Backup

If using PostgreSQL for n8n data:

```bash
# Automated daily backup
0 2 * * * pg_dump -h localhost -U n8n_user n8n_db > /backups/n8n_$(date +\%Y\%m\%d).sql

# Store backups securely (AWS S3, Azure, etc.)
aws s3 cp /backups/n8n_20260218.sql s3://n8n-backups/
```

#### 5.3 Recovery Procedure

If a workflow fails in production:

```bash
# 1. Find the last known working version
git log --oneline workflows/active/failed-workflow.json

# 2. Checkout the previous version
git show HEAD~1:workflows/active/failed-workflow.json > rollback.json

# 3. Import the previous version
curl -X POST http://prod-n8n:5678/api/workflows \
  -H "X-N8N-API-KEY: $PROD_API_KEY" \
  -d @rollback.json

# 4. Investigate the issue
# - Review execution logs
# - Check for credential issues
# - Verify external service availability
```

## Environment Configuration

### Development Environment

```json
{
  "N8N_PORT": 5678,
  "NODE_ENV": "development",
  "DB_TYPE": "sqlite",
  "WEBHOOK_URL": "http://localhost:5678",
  "N8N_LOG_LEVEL": "debug"
}
```

### Production Environment

```json
{
  "N8N_PORT": 5678,
  "NODE_ENV": "production",
  "DB_TYPE": "postgresql",
  "DB_HOST": "prod-db.example.com",
  "DB_PORT": 5432,
  "DB_NAME": "n8n_prod",
  "DB_USER": "n8n_app",
  "N8N_ENCRYPTION_KEY": "your-encryption-key",
  "WEBHOOK_URL": "https://n8n.example.com",
  "N8N_LOG_LEVEL": "info",
  "N8N_METRICS": true
}
```

## Post-Deployment Validation

### Day 1 Validation

- [ ] Workflow executions complete without errors
- [ ] Output data is correct and complete
- [ ] Notifications are sent to correct recipients
- [ ] No performance degradation observed
- [ ] Logs show normal operation

### Week 1 Validation

- [ ] Workflow runs successfully for multiple cycles
- [ ] Data consistency verified in target systems
- [ ] No unexpected errors or edge cases
- [ ] Team is comfortable with the workflow

### Ongoing Monitoring

```bash
# Monitor n8n health
curl http://prod-n8n:5678/api/health

# Monitor workflow execution rate
curl http://prod-n8n:5678/api/executions?limit=100

# Set up alerts for failures (via monitoring tool)
# - Alert on workflow failure
# - Alert on high error rate
# - Alert on slow execution times
```

## Troubleshooting

### Workflow Won't Start

```
1. Check credentials are valid
2. Verify webhook URL is accessible
3. Check logs for error messages
4. Test each node individually
5. Verify API rate limits not exceeded
```

### Execution Timeout

```
1. Check network connectivity
2. Increase timeout in HTTP Request node
3. Break workflow into smaller parts
4. Optimize database queries
5. Consider async processing
```

### Data Inconsistency

```
1. Verify transformation logic
2. Check field mapping
3. Test with sample data
4. Review error handling
5. Check for race conditions
```

## Related Documentation

- [Security Best Practices](./security-best-practices.md) — Secure deployment
- [CI/CD Setup](./ci-cd-setup.md) — Automated deployment
- [Workflow Style Guide](./workflow-style-guide.md) — Deployment requirements

## Rollback Procedures

Keep a documented procedure for emergency rollbacks:

1. **Immediate**: Disable the workflow in n8n UI
2. **Investigation**: Review execution logs and identify issue
3. **Restore**: Deploy previous working version
4. **Validate**: Test restored workflow
5. **Communicate**: Notify stakeholders of the incident
