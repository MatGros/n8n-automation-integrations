# Workflows Directory

This directory contains all n8n automation workflows organized by category and domain.

## Directory Structure

```
workflows/
├── 01-communication/      # Email, Telegram, Slack, Discord
├── 02-marketing/          # Social media, SEO, Campaigns
├── 03-sales/              # Lead gen, CRM, Proposals
├── 04-data-intelligence/  # News agents, Data processing, ML, Reporting
├── 05-iot/                # Sensors, MQTT, Smart home
├── 06-industry-4.0/       # Manufacturing, Supply chain, PLC, SCADA
├── 07-edge-computing/     # Edge analytics, Local AI, Data sync
├── 08-blockchain/         # Smart contracts, NFT, DeFi
├── 09-robotics/           # Robot control, Vision, ROS
├── 10-cloud-infrastructure/ # AWS, Azure, GCP, Kubernetes
├── 11-cybersecurity/      # Threat detection, Vulnerability, SIEM
├── 12-healthcare/         # Patient monitoring, Medical devices, HL7/FHIR
├── 13-energy/             # Smart grid, Renewable, Consumption
├── 14-agriculture/        # Precision farming, Weather, Crops
├── 15-transportation/     # Fleet management, Route optimization
└── 99-templates/          # Reusable templates and examples
```

## Workflow File Structure

Each workflow folder follows a standard architecture:

### Required Files (tested)

```
workflow-folder/
├── workflow.json          ← REQUIRED: n8n-ready workflow file
└── README.md              ← REQUIRED: Documentation (Purpose, Trigger, Output)
```

### Optional Files (documented but not tested)

```
workflow-folder/
├── template.json          ← OPTIONAL: Base/template version
├── test.json              ← OPTIONAL: Test cases and scenarios
├── config.json            ← OPTIONAL: Workflow-specific configuration
├── CHANGELOG.md           ← OPTIONAL: Version history
├── test-data/             ← OPTIONAL: Test payloads and data
│   ├── input-sample.json
│   └── expected-output.json
├── logs/                  ← OPTIONAL: Execution logs
│   ├── test-runs.log
│   └── execution.log
└── docs/                  ← OPTIONAL: Additional documentation
    ├── setup-guide.md
    └── troubleshooting.md
```

## Conventions

### File Naming

- **`workflow.json`** - The executable n8n workflow file (always present, always this name)
- **`template.json`** - Base/template version if this is a variation or template
- **`README.md`** - Documentation with mandatory sections (see template below)
- **`test.json`** - Test cases in JSON format
- **`config.json`** - Configuration parameters for the workflow

### Kebab-case Naming

All folder and file names MUST use kebab-case:
- ✅ `echo-bot/`
- ✅ `gmail-ai-responder/`
- ❌ `echo_bot/` (wrong)
- ❌ `EchoBot/` (wrong)

## README Template

Every workflow README.md MUST include:

```markdown
# Workflow Name

## Description
Brief description of what the workflow does.

## Purpose
What problem does it solve?

## Trigger
- **Type**: (HTTP, Telegram, Gmail, Schedule, etc.)
- **Event**: (Message received, Email arrived, etc.)

## Process
1. Step 1 description
2. Step 2 description
3. Step 3 description

## Output
- **Type**: (JSON, File, Message, etc.)
- **Format**: (Description of output format)

## Setup Requirements
1. API credentials needed
2. Configuration steps
3. Dependencies

## Status
- ✅ Active
- 🚧 Development
- ⚠️ Testing
- ⛔ Deprecated

## Tags
`tag1`, `tag2`, `tag3`
```

## Best Practices

1. **Never store secrets** in workflow files - use n8n Credentials
2. **Always use `workflow.json`** as the filename for the main executable
3. **Keep READMEs updated** when workflow changes
4. **Use templates** for reusable workflow patterns
5. **Test before production** - use test.json for test cases
6. **Document setup requirements** in README.md

## Contributing

When adding a new workflow:

1. Create a folder under the appropriate category (01-15 or 99-templates)
2. Add `workflow.json` (exported from n8n)
3. Create `README.md` with required sections
4. Optionally add `template.json`, test files, or documentation
5. Follow kebab-case naming convention

## Validation

Workflows are automatically validated to ensure:
- ✅ `workflow.json` exists and is valid JSON
- ✅ `README.md` exists with required sections
- ✅ No sensitive data (VPS URLs, personal emails, credentials)
- ⚠️ Optional files follow naming conventions (not enforced)

## Examples

See individual workflow folders for examples:
- [01-communication/telegram/echo-bot/](01-communication/telegram/echo-bot/)
- [01-communication/email/gmail-ai-responder/](01-communication/email/gmail-ai-responder/)
- [99-templates/](99-templates/)
