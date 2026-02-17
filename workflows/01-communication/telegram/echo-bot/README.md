# Telegram Echo Bot

## Description
Simple Telegram bot that echoes back the messages it receives.

## Purpose
Demonstrates basic Telegram trigger integration with n8n and message handling.

## Trigger
- **Type**: Telegram Trigger
- **Event**: Message received

## Output
- **Type**: Text message sent back to the user
- **Format**: `message: [original message content]`

## Setup Requirements
1. Create a Telegram bot via @BotFather
2. Configure Telegram API credentials in n8n
3. Set up webhook for message reception

## Status
✅ Active

## Quick start
1. Import `echo-bot/workflow.json` into your n8n instance.
2. Add `Telegram` credentials in n8n (use `.env` placeholders).
3. Activate the workflow and send a test message to the bot.

## Tags
`telegram`, `bot`, `communication`, `simple`
