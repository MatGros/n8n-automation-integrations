# Smart Gmail Labeler & Reply Draft

**Version:** 1.0.0
**Date:** 2026-02-22

## Description
Analyzes incoming Gmail messages, generates AI-powered draft replies, and applies intelligent labels to organize the inbox.

## Purpose
Automate email management with AI-generated responses and intelligent categorization.

## Trigger
- **Type**: Schedule Trigger / Manual Trigger
- **Event**: Scheduled execution or manual run

## Process
1. Aggregate Gmail messages
2. Fetch available Gmail labels
3. Classify email with AI (OpenAI/Gemini)
4. Apply classification label
5. Assess if message needs a reply
6. Generate email reply
7. Create draft reply

## Output
- Draft replies in Gmail
- Labeled emails in Gmail
