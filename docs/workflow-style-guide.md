# Workflow Style Guide

Purpose: centralise les conventions visuelles et rédactionnelles pour tous les workflows du repository. Utilisez ce guide comme référence pour la création, la revue et la maintenance des workflows.

## 1. Principes généraux
- Lisibilité avant tout — un workflow doit expliquer son comportement sans lire le code.
- Nommer les nodes avec des verbes d'action (`fetch-emails`, `parse-json`, `send-notification`).
- Garder les workflows < 20 nodes quand possible; scinder en sous-workflows si nécessaire.

## 2. Sections obligatoires dans `README.md`
Chaque workflow DOIT contenir au minimum les sections suivantes (niveau `##`):
- `Description` — court résumé (1-2 phrases)
- `Purpose` — objectif métier
- `Trigger` — type d'événement / fréquence
- `Process` — étapes principales (numérotées)
- `Output` — ce qui est produit
- `Setup Requirements` — credentials / secrets / config

## 3. Color mapping (7 couleurs)
- Bleu — Data fetch / IO (HTTP, IMAP, DB)
- Vert — Logic / Transformation
- Jaune — Storage / Persistence
- Rouge — Error / Alerting
- Orange — Triggers
- Violet — AI / LLM / Model calls
- Cyan — Communication (Slack, Email, Telegram)

> Example: `HTTP Request` (blue) → `JSON Parse` (green) → `DB Insert` (yellow)

## 4. Node naming conventions
- Use kebab-case, verbs first: `fetch-gmail`, `classify-text`, `create-draft`.
- Avoid generic names: prefer `send-notification-email` > `send-email` (be explicit).
- Node `name` should be human-readable (shown in UI) and correspond to the primary action.

## 5. Node descriptions
- Each complex node (logic, AI, transformations) SHOULD include a brief comment/description in the workflow JSON `parameters` or documented in README `Process`.

Example snippet (README `Process`):

1. `fetch-gmail` — watch inbox and return message payloads
2. `classify-email` — call AI to decide if reply needed (returns `needsReply` boolean)
3. `create-draft` — create draft reply using templated prompt

## 6. Layout & ordering
- Left → Right flow for data pipelines and synchronous flows.
- Triggers on the far-left; outputs on the far-right.
- Group related nodes vertically and use separators (comments in README) for sections.

## 7. Error handling
- Always include an explicit error path for critical flows (notify + retry or dead-letter).
- Document error handling in `Process` and mark nodes that send alerts.

## 8. Documentation checklist (to include in README / PR)
- [ ] `Description` present
- [ ] `Purpose` present
- [ ] `Trigger` present
- [ ] `Process` steps documented
- [ ] `Output` declared
- [ ] `Setup Requirements` documented
- [ ] Example `Quick start` included

## 9. Examples
### Good README excerpt
```
## Purpose
Automate triage of incoming support emails and create draft responses.

## Trigger
- Type: Gmail Watch
- Event: New email

## Output
- Draft replies in Gmail
- Ticket created in Helpdesk system
```

## 10. Reference links
- `docs/workflow-checklist.md` — validation checklist (used by CI)
- `scripts/validators/documentation_validator.py` — validator automatique

---

Keep this guide concise — link to examples in `workflows/` for concrete patterns.
