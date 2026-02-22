# Security Best Practices

_Last updated: 2026-02-19 • Audience: Contributors & Maintainers_

## Purpose

This guide documents security best practices for developing, testing, and deploying workflows in the n8n-automation-integrations repository. Security is a shared responsibility across all contributors.

## Core Principles

1. **Never embed secrets** in workflow files or code
2. **Sanitize all user inputs** before using in queries or APIs
3. **Use environment variables** for all credentials and sensitive data
4. **Audit credentials** regularly
5. **Encrypt sensitive data** in transit and at rest
6. **Document security requirements** for each workflow

## Secret Management

### What is a Secret?

Secrets include:
- API keys, access tokens, authentication credentials
- Database connection strings with passwords
- Private SSH keys, SSL certificates
- OAuth tokens, Bearer tokens
- Email addresses (if treating as PII)
- Encryption keys, encryption salts

### Best Practice: Using Credentials in n8n

1. **Create credentials in n8n Settings**
   - Navigate to Settings → Credentials
   - Create new credential of the required type
   - Name it descriptively: `gmail-account-prod`, `slack-bot-dev`
   - n8n encrypts these automatically

2. **Reference credentials in workflows**
   - In HTTP Request nodes: Select credential from dropdown (not hardcoded)
   - In custom code: Use `$credentials` variable
   ```javascript
   // ✅ CORRECT
   const apiKey = $credentials.api_key;

   // ❌ WRONG
   const apiKey = 'sk-12345...'; // Never hardcode!
   ```

3. **Export safely**
   - n8n removes credential values when exporting
   - Always verify exported JSON has no visible tokens
   - Use `scripts/sanitize_workflows.py` before committing

### Environment Variables

For n8n instances, use `.env` files for configuration:

```bash
# .env (NEVER commit this file)
N8N_ENCRYPTION_KEY=your-encryption-key
DATABASE_URL=postgresql://user:pass@localhost/n8n
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
OPENAI_API_KEY=sk-...
```

Add `.env` to `.gitignore`:
```gitignore
.env
.env.local
.env.*.local
```

## Input Sanitization

### SQL Injection Prevention

When building database queries, always use parameterized queries:

```javascript
// ✅ CORRECT - Parameterized query
db.query(
  'SELECT * FROM users WHERE email = ?',
  [userEmail]
);

// ❌ WRONG - String concatenation
db.query('SELECT * FROM users WHERE email = ' + userEmail);
```

### NoSQL Injection Prevention

For MongoDB or similar:

```javascript
// ✅ CORRECT - Query parameters
db.collection.find({ email: userEmail });

// ❌ WRONG - Unsafe operators
db.collection.find({ $where: userInput });
```

### XSS Prevention

When outputting user data in HTML/emails:

```javascript
// ✅ CORRECT - Escape HTML
const escaped = html_escape(userInput);

// ❌ WRONG - Direct output
const result = `<p>${userInput}</p>`;
```

### API Request Sanitization

```javascript
// ✅ CORRECT - Validate and sanitize
const validateEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

const email = input.email;
if (!validateEmail(email)) {
  throw new Error('Invalid email format');
}

// ❌ WRONG - No validation
const response = await fetch(`https://api.example.com/users/${input.userId}`);
```

## Credential Handling

### For Database Credentials

1. Use n8n's built-in credential types (PostgreSQL, MySQL, etc.)
2. n8n encrypts connection strings
3. Rotate credentials quarterly
4. Use least-privilege database users (read-only when possible)

Example setup:
- Production: `readonly-app-prod@prod-db`
- Development: `app-dev@dev-db`

### For API Keys

1. Store as "Generic credential type" in n8n
2. Use API key rotation if the service supports it
3. Restrict API key scopes (e.g., read-only where possible)
4. Monitor API usage for unauthorized requests

### For OAuth / Bearer Tokens

1. Use n8n's OAuth credential type (Gmail, Slack, etc.)
2. Enable token refresh if available
3. Set appropriate expiration policies
4. Remove inactive credentials after 90 days

## Audit and Monitoring

### Credential Audit Checklist

Monthly, review:
- [ ] List all credentials in n8n (Settings → Credentials)
- [ ] Verify each credential is still needed
- [ ] Check last usage date (if available)
- [ ] Remove unused credentials
- [ ] Document who has access
- [ ] Review credential type and scope

### Workflow Audit Checklist

Before deploying any workflow:
- [ ] Run `scripts/sanitize_workflows.py --dry-run` to check for exposed secrets
- [ ] Review all HTTP Request nodes use credentials, not hardcoded tokens
- [ ] Verify no plaintext passwords in node configuration
- [ ] Check all user inputs are validated
- [ ] Verify error messages don't leak sensitive info
- [ ] Ensure logging doesn't capture secrets

### Sanitization Script Usage

```bash
# Dry run (shows what would be sanitized)
python scripts/sanitize_workflows.py --dry-run

# Apply sanitization
python scripts/sanitize_workflows.py

# Sanitize specific workflow
python scripts/sanitize_workflows.py workflows/active/gmail-auto-responder.json
```

## Data Protection

### In Transit

- Always use HTTPS/TLS for API calls
- Verify SSL certificates
- Use VPN for sensitive on-premises integrations

### At Rest

- Enable database encryption
- Encrypt sensitive files
- Use AWS KMS or similar for cloud storage

### PII (Personally Identifiable Information)

- Minimize PII collection
- Hash email addresses where possible
- Implement data retention policies
- Document PII processing in workflow README

## Workflow-Specific Security

### Email Workflows

```javascript
// ✅ CORRECT - Validate before using in email
const recipient = input.email;
if (!isValidEmail(recipient)) {
  throw new Error('Invalid recipient email');
}

// Include security notice in emails
const emailBody = `
...content...
---
This email was generated automatically. Do not reply directly.
`;
```

### Database Workflows

```javascript
// ✅ CORRECT - Validate and limit
const limit = Math.min(input.limit || 10, 100); // Max 100 records
const offset = Math.max(0, input.offset || 0);

// Use prepared statements
db.query('SELECT * FROM records LIMIT ? OFFSET ?', [limit, offset]);
```

### API Integration Workflows

```javascript
// ✅ CORRECT - Rate limiting
if (rateLimiter.isLimited(userId)) {
  throw new Error('Rate limit exceeded');
}

// Timeout for external calls
const response = await fetch(url, {
  timeout: 30000, // 30 second timeout
  headers: { 'User-Agent': 'n8n/2.x' }
});
```

## Incident Response

If you suspect a credential has been compromised:

1. **Immediately** rotate the credential in n8n
2. **Search** for recent workflow executions using that credential
3. **Audit** any external systems accessed by that credential
4. **Document** the incident in a private note
5. **Notify** project maintainers
6. **Review** git history to check if the secret was ever committed

## Related Documentation

- [Deployment Guide](./deployment-guide.md) — Secure deployment procedures
- [Contributing Guide](./contributing.md) — PR security requirements
- [Workflow Style Guide](./workflow-style-guide.md) — Standards for all workflows

## Additional Resources

- [n8n Security Guide](https://docs.n8n.io/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
