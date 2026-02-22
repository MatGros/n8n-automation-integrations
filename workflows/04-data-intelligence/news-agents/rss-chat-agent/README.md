# RSS Chat Agent - Talk with the News

## Description
AI-powered conversational agent that reads RSS feeds and allows users to have discussions about current news and topics.

## Purpose
Enable natural language conversations about news from multiple RSS sources using AI.

## Trigger
- **Type**: Telegram / Chat interface
- **Event**: User message received

## Process
1. Monitor RSS feeds for new articles
2. Process incoming user queries
3. Search relevant articles from feeds
4. Generate contextual AI responses
5. Return conversational responses

## Output
- Natural language responses about news topics
- Citations and source links
- Follow-up conversation support

## Data Sources
- Configurable RSS feeds
- Support for multiple sources

## AI Integration
- Uses OpenAI/Gemini for conversation
- Context-aware responses based on article content

## Setup Requirements
1. RSS feed URLs configured
2. AI API credentials (OpenAI/Gemini)
3. Chat platform integration (Telegram/HTTP)

## Status
✓ Published

## Quick start
1. Import `rss-chat-agent/workflow.json` into n8n.
2. Configure RSS feeds and AI credentials.
3. Start the workflow and send a test query via Telegram.

## Example
User: "Summarize the latest article about renewable energy"
Bot (excerpt):
```
AI: "In today's article, researchers show a 12% increase in solar efficiency... [source link]"
```
Response includes brief summary + citation.

## Tags
`ai-agent`, `news`, `rss`, `conversation`, `data-intelligence`
