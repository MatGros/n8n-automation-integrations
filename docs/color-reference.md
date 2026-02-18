# Node Color Reference Guide

## Purpose

This guide defines the standardized color scheme for n8n nodes across all workflows in this repository. Consistent color usage improves workflow readability and helps contributors quickly identify node types and their purposes.

## Color Palette

| Color | Purpose | Hex Code | Use Cases |
|-------|---------|----------|-----------|
| **Blue** | Fetch / Input / Output | `#0099ff` | API calls, HTTP requests, Database reads, File downloads, IMAP/SMTP email reads |
| **Green** | Logic / Transformation | `#00a651` | Conditional logic, Data transformation, JavaScript/Python code, Data parsing, Set/Format nodes |
| **Yellow** | Storage / Persistence | `#f4a400` | Database writes, File operations, Cache operations, S3 uploads, Document storage |
| **Red** | Error / Alerting | `#ff4444` | Error handling nodes, Exception catching, Alert notifications, Critical notifications |
| **Orange** | Triggers | `#ff9800` | Webhook triggers, Cron/Schedule triggers, Event listeners, Start nodes |
| **Violet** | AI / LLM Calls | `#9c27b0` | OpenAI calls, Claude API, LLM prompting, ML model inference, AI processing |
| **Cyan** | Communication | `#00bcd4` | Slack messages, Email sending, SMS notifications, Chat integrations, Messaging platforms |

## Usage Guidelines

### 1. Node Type Classification

When adding a node to a workflow, follow these rules:

- **Fetch (Blue)**: Use for any node that retrieves data from external systems
  - Examples: HTTP Request, Gmail Query, Database Read, File Download

- **Logic (Green)**: Use for nodes that process, transform, or make decisions
  - Examples: If/Switch, Code nodes, Set node, Format as JSON

- **Storage (Yellow)**: Use for nodes that persist or write data
  - Examples: Database Insert, Google Sheet Write, File Create, S3 Upload

- **Error (Red)**: Use exclusively for error handling
  - Examples: Try/Catch, Error notification, Retry logic

- **Trigger (Orange)**: Use only for workflow triggers
  - Examples: Webhook Trigger, Cron trigger, Event listener

- **AI (Violet)**: Use for AI/LLM operations
  - Examples: OpenAI node, Claude API, Any model inference

- **Communication (Cyan)**: Use for sending messages/notifications
  - Examples: Slack Message, Send Email, Telegram, Teams Message

### 2. Layout Best Practices

When designing workflow layouts:

1. **Trigger on the left** (Orange)
2. **Data flow left to right**: Fetch (Blue) → Logic (Green) → Storage (Yellow)
3. **Communication nodes (Cyan)** positioned on the right for final notifications
4. **Error paths (Red)** positioned below main flow or in separate branches
5. **AI nodes (Violet)** positioned in the middle where processing happens

### 3. Complex Workflow Example

For a workflow that fetches emails, classifies them with AI, and sends notifications:

```
[Webhook Trigger] (Orange)
    ↓
[Fetch Gmail] (Blue)
    ↓
[AI Classification] (Violet)
    ↓
[Logic Branch] (Green)
    ├→ [Send Email] (Cyan)
    └→ [Database Store] (Yellow)

[Error Handler] (Red) — catches all errors
```

## Implementation Notes

- All colors are CSS-compatible hex codes
- When setting node colors in n8n UI, use the hex codes provided above
- For accessibility, ensure sufficient contrast when viewing workflows
- Document complex workflows with a legend in the README
- Consistency across all workflows is required for PR approval

## Color Accessibility

If you need to adjust colors for accessibility reasons (e.g., colorblind users):
- Always maintain the same semantic meaning (Blue = Fetch, etc.)
- Document any overrides in workflow README
- Ensure sufficient contrast for colorblind users
- Consider using patterns or labels in addition to colors

## Related Documentation

- [Workflow Style Guide](./workflow-style-guide.md) — Node naming and layout conventions
- [Node Naming Convention](./workflow-style-guide.md#3-node-naming) — How to name nodes consistently
