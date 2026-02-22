# Harmonization Rules — n8n Workflows Project

**Source of Truth** for all project conventions. This document is the canonical reference for contributors, validators, and CI/CD workflows.

---

## Table of Contents

1. [README Structure (Required)](#1-readme-structure-required)
2. [Workflow JSON Structure](#2-workflow-json-structure)
3. [Node Naming Conventions](#3-node-naming-conventions)
4. [Color Mapping](#4-color-mapping)
5. [Workflow Metadata](#5-workflow-metadata)
6. [Security Rules](#6-security-rules)
7. [Project Structure](#7-project-structure)
8. [Enforcement Matrix](#8-enforcement-matrix)

---

## 1. README Structure (Required)

Every workflow directory (containing `workflow.json`) **MUST** have a `README.md` with these sections in order:

### Required Sections (Must be present)

| # | Section | Min Length | Format | Example |
|---|---------|-----------|--------|---------|
| 1 | `## Description` | 1–3 sentences | Plain text | "Analyzes incoming emails and generates AI-powered draft replies." |
| 2 | `## Purpose` | 1–2 sentences | Plain text | "Automate email management with intelligent categorization." |
| 3 | `## Trigger` | List trigger type + event | Markdown list or table | "**Type**: Gmail Watch<br/>**Event**: New email received" |
| 4 | `## Process` | Min 2 steps | Numbered list | "1. Monitor emails<br/>2. Extract content<br/>3. Generate response" |
| 5 | `## Output` | 1–2 artifacts | Plain text or bullet list | "- Draft email replies in Gmail<br/>- Automated labels" |
| 6 | `## Setup Requirements` | List all dependencies | Bullet list | "- Gmail API credentials<br/>- OpenAI API key<br/>- Email categories defined" |
| 7 | `## Quick start` | Step-by-step import guide | Numbered list | "1. Import workflow.json<br/>2. Configure credentials<br/>3. Test" |
| 8 | `## Example` | Concrete input + output | Code fence or table | Shows actual message + bot response |
| 9 | `## Tags` | Searchable keywords | Comma-separated or list | `telegram`, `bot`, `communication`, `simple` |
| 10 | `## Status` | Workflow stage | Badge or text | `✅ Active` / `🚧 Development` / `⚠️ Deprecated` |

### Optional Sections (May be present)

- **Features** — for complex workflows with distinct capabilities
- **Supported Platforms** — for multi-channel workflows
- **Data Sources** — for data intelligence workflows
- **AI Integration** — for workflows using LLM calls
- **CHANGELOG** — version history and breaking changes

---

## 2. Workflow JSON Structure

### Top-Level Fields (Canonical Schema)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | **YES** | Human-readable workflow name; no generic IDs like "workflow-1" |
| `nodes` | array | **YES** | All nodes in the workflow |
| `connections` | object | **YES** | Wiring map: `{"sourceNodeName": [{ node, type, index }]}` |
| `active` | boolean | **YES** | `true` if live, `false` if draft |
| `settings` | object | **YES** | Must contain `{"executionOrder": "v1"}` |
| `versionId` | string | **YES** | UUID version identifier (auto-assigned by n8n) |
| `meta` | object | **NO** | Optional metadata (e.g., `templateCredsSetupCompleted`, `templateId`) |
| `id` | string | **YES** | Unique workflow ID (auto-assigned by n8n) |
| `tags` | array | **NO** | Tag list for categorization |
| `pinData` | object | **NO** | Test data pins per node (usually empty `{}`) |

### Node Fields (Within `nodes` array)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | string | **YES** | Unique node ID (UUID format) |
| `name` | string | **YES** | Human-readable, follows `verb-resource[-detail]` (kebab-case); **never** generic like "node-1" |
| `type` | string | **YES** | e.g., `n8n-nodes-base.telegramTrigger`, `n8n-nodes-base.httpsRequest` |
| `typeVersion` | number | **YES** | Version of the node type |
| `position` | array | **YES** | `[x, y]` coordinates for UI layout |
| `parameters` | object | **YES** | Node-specific configuration |
| `credentials` | object | **NO** | Credential references: `{"credentialType": {"id": "...", "name": "..."}}` |

---

## 3. Node Naming Conventions

### Format Rule

```
verb-resource[-detail]
```

- **verb**: Action word (fetch, send, create, classify, transform, validate, apply, etc.)
- **resource**: What is being operated on (email, message, label, draft, etc.)
- **detail** (optional): Specificity to disambiguate (e.g., `send-notification-email` instead of `send-email`)

### Examples

✅ **Good**
```
fetch-gmail
classify-email
create-draft
send-notification-email
transform-json-to-csv
validate-phone-number
apply-label
wait-for-approval
```

❌ **Bad**
```
node-1
do-stuff
process
email
response
```

### Forbidden Generic Names

These names are **NOT allowed** and will fail validation:
```
node-1, node-2, node-N
step-1, step-2
process, action, execute
data, result, output
temp, test
workflow-start
```

---

## 4. Color Mapping (Visual Consistency)

Use these node colors to indicate function at a glance:

| Color | Nodes | Examples |
|-------|-------|----------|
| 🔵 **Blue** | Fetch / Input / Data Access | HTTP, IMAP, Database, API calls |
| 🟢 **Green** | Logic / Transformation | If/Then, Code, Merge, Transform, Filter |
| 🟡 **Yellow** | Storage / Persistence | Write DB, Append to Sheet, Save File |
| 🔴 **Red** | Error / Alert / Fail Stop | Error Handler, Notify on Fail, Throw Error |
| 🟠 **Orange** | Triggers | Telegram Trigger, Gmail Watch, Webhook, Schedule |
| 🟣 **Violet** | AI / LLM | OpenAI, Gemini, Claude, LLM Tool |
| 🔷 **Cyan** | Communication | Slack, Email Send, Telegram Send, Discord |

**Guidelines:**
- Assign colors when creating nodes; keep it consistent
- For complex workflows (>10 nodes), include a legend in the README
- Error paths should form a visually distinct group (usually on the right or bottom)

---

## 5. Workflow Metadata

Every workflow **MUST** have a `metadata.json` file alongside `workflow.json` and `README.md`.

### Schema (see `workflows/schema/workflow-metadata.schema.json`)

```json
{
  "name": "Echo Bot",
  "category": "01-communication",
  "version": "1.0.0",
  "status": "active",
  "required_credentials": ["telegram"],
  "tags": ["telegram", "bot", "communication", "simple"],
  "n8n_version_min": "1.0.0",
  "author": "Your Name"
}
```

### Field Definitions

| Field | Type | Required | Values | Notes |
|-------|------|----------|--------|-------|
| `name` | string | **YES** | Any | Human-readable name (should match README `# Heading`) |
| `category` | string | **YES** | One of 16 categories | See [Project Structure](#7-project-structure) |
| `version` | string | **YES** | SemVer `X.Y.Z` | Increment on changes; `1.0.0` for new workflows |
| `status` | string | **YES** | `active`, `development`, `deprecated`, `archived` | Workflow lifecycle state |
| `required_credentials` | array | **YES** | Credential type strings | e.g., `["gmail", "openai"]` — **exact list of what's needed** |
| `tags` | array | **YES** | Lowercase, hyphenated strings | For search/discovery; minimum 2 tags |
| `n8n_version_min` | string | **NO** | SemVer `X.Y.Z` | Minimum n8n version required (optional, for complex workflows) |
| `author` | string | **NO** | Your GitHub handle or name | Original creator (optional) |

---

## 6. Security Rules

### What Gets Detected (Automated)

The `scripts/validators/security_validator.py` automatically scans for and **blocks**:

| Risk | Pattern | Action |
|------|---------|--------|
| **Email exposure** | Any email domain NOT in `example.com`, `example.org`, `example.net`, `localhost` | 🚫 Blocks commit via pre-commit hook |
| **Credential IDs** | 16-char alphanumeric strings NOT starting with `CRED_` in `credentials.*.id` | 🚫 Blocks commit |
| **Instance IDs** | 64-char hex values in any `instanceId` field | 🚫 Blocks commit |
| **Webhook IDs** | UUID-format values in `webhookId` fields | 🚫 Blocks commit |
| **VPS URLs** | Hostnames containing `srv`, specifically `hstgr.cloud`, `n8n.srv` (case-insensitive) | 🚫 Blocks commit |

### Manual Security Practices

- **Never commit `.env` files** — use `.env.example` as a template
- **Always use credentials stored in n8n**, not hardcoded in JSON
- **Sanitize workflow JSON before committing**: run `scripts/sanitize_workflows.py --dry-run` before `git add`
- **Review credential placeholders**: Use `{{$credentials.credentialName.apiKey}}` instead of hardcoding
- **Limit node output**: Avoid exposing full API responses; extract only needed fields

---

## 7. Project Structure

### Workflow Categories (16 Total, 5 Currently Active)

**Active Categories** (workflows exist)

```
workflows/
├── 01-communication/          # Email, Telegram, Slack, Discord, SMS
├── 02-marketing/              # Social media, SEO, Email campaigns
├── 03-sales/                  # Lead generation, CRM, Proposals
├── 04-data-intelligence/      # News agents, Data processing, BI
└── 99-templates/              # Reusable components and starter templates
```

**Future Categories** (for expansion)

```
├── 05-iot/                    # Sensors, MQTT, Smart home
├── 06-industry-4.0/           # Manufacturing, Supply chain, PLC
├── 07-edge-computing/         # Edge analytics, Local AI
├── 08-blockchain/             # Smart contracts, NFT, DeFi
├── 09-robotics/               # Robot control, Vision, ROS
├── 10-cloud-infrastructure/   # AWS, Azure, GCP, Kubernetes
├── 11-cybersecurity/          # Threat detection, Vulnerability
├── 12-healthcare/             # Patient monitoring, HL7/FHIR
├── 13-energy/                 # Smart grid, Renewable, Consumption
├── 14-agriculture/            # Precision farming, Weather, Crops
└── 15-transportation/         # Fleet management, Route optimization
```

**Template Structure Within a Category**

```
workflows/
└── 01-communication/
    ├── README.md                     # Category index (optional)
    ├── email/
    │   ├── gmail-ai-responder/
    │   │   ├── workflow.json         # Workflow definition
    │   │   ├── metadata.json         # Metadata (THIS file)
    │   │   └── README.md             # Workflow documentation
    │   └── outlook-sync/
    │       └── ...
    ├── telegram/
    │   ├── echo-bot/
    │   │   ├── workflow.json
    │   │   ├── metadata.json
    │   │   └── README.md
    │   └── ...
    ├── slack/
    └── discord/
```

### Documentation Structure

```
docs/
├── RULES.md                          # THIS FILE
├── workflow-style-guide.md           # Detailed style and layout guide
├── workflow-checklist.md             # PR checklist template
├── contributing.md                   # Contributor onboarding
├── security-best-practices.md        # Security details
├── deployment-guide.md               # How to deploy workflows
├── color-reference.md                # Color codes reference
├── by-industry/                      # Industry-specific guides
│   ├── healthcare-guide.md
│   ├── industry-4.0-guide.md
│   └── iot-guide.md
└── by-technology/                    # Technology-specific guides
    ├── kubernetes-automation.md
    ├── mqtt-integration.md
    └── ...
```

---

## 8. Enforcement Matrix

This table shows what is checked automatically, at what stage, and what requires manual review:

| Rule | Validator | Pre-Commit | CI/CD | Manual Review |
|------|-----------|-----------|-------|---------------|
| README has required 10 sections | `documentation_validator.py` | ✅ | ✅ | ✅ |
| `workflow.json` has `name` | `documentation_validator.py` | ✅ | ✅ | ✅ |
| All nodes have `name` field | `documentation_validator.py` | ✅ | ✅ | ✅ |
| No generic node names (node-1) | None currently | ❌ | ❌ | ✅ |
| Node naming format (verb-resource) | None currently | ❌ | ❌ | ✅ |
| Color mapping followed | None currently | ❌ | ❌ | ✅ |
| `metadata.json` present | None currently | ❌ | ❌ | ✅ |
| `metadata.json` valid JSON | `json` linter | ✅ | ✅ | ❌ |
| No emails in workflow.json | `security_validator.py` | ✅ | ✅ | ❌ |
| No credential IDs leaked | `security_validator.py` | ✅ | ✅ | ❌ |
| No instance IDs leaked | `security_validator.py` | ✅ | ✅ | ❌ |
| No webhook IDs leaked | `security_validator.py` | ✅ | ✅ | ❌ |
| No private IPs in JSON | `test_security.py test_05` | ❌ | ✅ | ❌ |
| No hardcoded API tokens | `test_security.py test_06` | ❌ | ✅ | ❌ |
| Category directory exists | `architecture_validator.py` | ❌ | ✅ | ❌ |
| All categories have README | `architecture_validator.py` | ❌ | ✅ | ❌ |
| No trailing whitespace | `pre-commit` hook | ✅ | ✅ | ❌ |
| End of file has newline | `pre-commit` hook | ✅ | ✅ | ❌ |
| Valid JSON format | `pre-commit` hook | ✅ | ✅ | ❌ |

---

## Summary

**For Contributors:**
1. Create `README.md` with all 10 sections
2. Name all nodes using `verb-resource[-detail]` kebab-case
3. Create `metadata.json` with required fields
4. Assign appropriate node colors
5. Run `pre-commit run --all-files` before pushing
6. Run `pytest -q` locally to catch security/docs issues

**For Maintainers:**
1. Use this `RULES.md` as the canonical reference when reviewing PRs
2. Update `RULES.md` if conventions change
3. Update validators in `scripts/validators/` to match `RULES.md`
4. Keep the enforcement matrix in sync with actual CI/CD checks

---

**Last Updated**: 2026-02-19
**Maintained By**: Project Team
