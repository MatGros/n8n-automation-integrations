# Gmail AI Auto-Responder

## Description
Analyzes incoming Gmail messages, generates AI-powered draft replies, and applies intelligent labels to organize the inbox.

## Purpose
Automate email management with AI-generated responses and intelligent categorization.

## Trigger
- **Type**: Gmail Watch
- **Event**: New email received

## Process
1. Monitor incoming emails
2. Extract email content and metadata
3. Generate AI responses using OpenAI/Gemini
4. Apply labels based on email category
5. Create draft replies

## Output
- Draft email replies in Gmail
- Automated labels applied to emails

## Setup Requirements
1. Gmail API credentials configured
2. OpenAI API key (or alternative AI service)
3. Email categories defined for labeling
4. Draft folder configured

## Status
🚧 Development

## Quick start
1. Import `gmail-ai-responder/workflow.json` into n8n.
2. Configure `Gmail OAuth2` and `OpenAI` credentials.
3. Test in `development/` before promoting to `active/`.

## Example
Input (email):
```
Subject: Pricing request
Body: Hi — can you send your pricing tiers?
```
Expected result (draft created in Gmail — excerpt):
```
Subject: Re: Pricing request
Hi John,
Thanks for your message — our Starter plan is $X/month. I attached the pricing sheet.
```

## Tags
`gmail`, `email`, `ai`, `automation`, `labels`
