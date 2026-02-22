# Archive

This directory contains legacy and development workflow files that have been archived.

## Contents

### workflows-development/
Workflow files from the original `workflows/development/` directory before restructuring in PHASE 2.

These files were:
- Moved to appropriate category folders (e.g., `01-communication/email/`)
- OR archived because they were duplicates/variations
- OR kept for reference/history

**Files:**
- `Gmail AI Auto-Responder_ Create Draft Replies to incoming emails_20260215.json` - Development version
- `Gmail AI Auto-Responder_ Create Draft Replies to incoming emails_20260215-2.json` - Development variation
- `gmail-ai-auto-responder.json` - Final version (migrated to 01-communication/email/)
- `social-media-content-creator.json` - Final version (migrated to 02-marketing/)

### original-templates/
Original template files from `workflows/templates/` before PHASE 2 restructuring.

**Files:**
- `Auto AI Label Gmail unread msg_20260217.json` - Email labeling template
- `Auto-classify Gmail emails with AI and apply labels for inbox organization_20260217.json` - Email classification
- `Gmail AI Auto-Responder_ Create Draft Replies to incoming emails.json` - Email responder template

## Usage

These files are kept for:
- **Reference**: Understanding workflow evolution
- **Recovery**: In case specific variations are needed
- **History**: Tracking development iterations

## Cleanup Policy

- Archive files are NOT used in production
- Archive files are NOT loaded by n8n
- Archived files can be safely deleted after 6 months (if no longer needed)
- If you need content from archive, migrate it to appropriate `workflows/XX-category/` folder

## Questions?

Refer to the main [workflows/README.md](../workflows/README.md) for the current structure.
