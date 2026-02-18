# Social Media Content Creator

## Description
Automatically generates content for multiple social media platforms with platform-specific formatting and optimization.

## Purpose
Streamline content creation across different social networks (Twitter, LinkedIn, Instagram, Facebook, etc.).

## Trigger
- **Type**: Schedule (periodic) or Manual
- **Frequency**: Configurable

## Process
1. Generate base content (AI-powered or from template)
2. Adapt content for each platform
3. Add platform-specific hashtags and mentions
4. Schedule or publish directly
5. Track engagement metrics

## Output
- Formatted posts for multiple platforms
- Scheduling or direct publishing
- Engagement reports

## Supported Platforms
- Twitter/X
- LinkedIn
- Instagram
- Facebook
- TikTok
- YouTube

## Setup Requirements
1. Social media API credentials for each platform
2. Content templates or AI service integration
3. Scheduling configuration

## Status
🚧 Development

## Quick start
1. Import `multi-platform-creator/workflow.json` into n8n.
2. Add OpenAI and social platform credentials (Twitter/X, LinkedIn, Instagram).
3. Run in staging and validate posts per-platform.

## Example
Base prompt: `Write a short promotional post about our 30% spring discount.`

Example generated outputs (excerpt):
```
Twitter: "Spring sale! 30% off all plans — limited time. #SpringSavings"
LinkedIn: "We’re offering 30% off our plans this spring. Learn more and save today. [link]"
Instagram: "Spring vibes 🌷 — 30% off! Tap the link in bio. #Sale"
```

## Tags
`social-media`, `content-creation`, `marketing`, `multi-platform`, `ai`
