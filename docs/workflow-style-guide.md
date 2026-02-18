# Workflow Style Guide

Purpose
---
Centralise les conventions visuelles et rédactionnelles appliquées aux workflows du dépôt. Ce guide sert de référence rapide pour la création, la revue et l'automatisation de la documentation.

Principes clés
---
- Lisibilité d'abord : un reviewer doit comprendre le flux principal sans ouvrir chaque node.
- Predictibilité : noms explicites, étapes numérotées, outputs clairs.
- Réutilisabilité : privilégier de petits workflows composables (<20 nodes) et extraire les sous‑processus.

1) Sections obligatoires dans `README.md` (MUST)
- `Description` — 1‑2 phrases, objectif métier.
- `Purpose` — pourquoi ce workflow existe.
- `Trigger` — type d'événement / fréquence / exemples.
- `Process` — étapes numérotées, explication courte par étape.
- `Output` — artefacts produits (messages, DB rows, drafts).
- `Setup Requirements` — credentials, variables d'environnement, permissions.

2) Checklist documentaire (à inclure dans PR)
- [ ] Description, Purpose, Trigger, Process, Output, Setup présents
- [ ] README contient un `Quick start` (import + credential example)
- [ ] JSON valide et `name` présent dans `workflow.json`
- [ ] Tous les nodes importants ont un `name`
- [ ] README respecte le style-guide (naming + color mapping)

3) Node naming (conventions)
- Format : `verb-resource[-detail]` en `kebab-case` — ex. `fetch-gmail`, `classify-email`, `create-draft`.
- Préférer l'action précise : `send-notification-email` > `send-email`.
- Ne pas utiliser noms techniques internes (ex. `node-1`) comme `name`.

4) Color mapping (visual guidance)
- Bleu — Fetch / IO (HTTP, IMAP, DB)
- Vert — Logic / Transformation
- Jaune — Storage / Persistence
- Rouge — Error / Alerting
- Orange — Triggers
- Violet — AI / LLM calls
- Cyan — Communication (Slack, Email, Telegram)

Conseil : ajoutez une légende dans le README pour workflows complexes.

5) Layout & best practices
- Flux principal → gauche vers droite.
- Grouper nodes liés verticalement (entrée, traitement, sortie).
- Séparer les chemins d'erreur visuellement et documenter le comportement de reprise.

6) Error handling
- Documenter la stratégie (retry, backoff, DLQ, alerting).
- Node d'alerte (ex: `notify-on-error`) doit clairement indiquer la cible (Slack/email).

7) Examples (README `Process` snippet)
```
1. `fetch-gmail` — watch inbox and return message payloads
2. `classify-email` — call AI model to decide if reply required (returns `needsReply` boolean)
3. `create-draft` — generate draft with templated prompt and save to Gmail
```

8) Enforcement & CI
- `scripts/validators/documentation_validator.py` valide la présence des sections, la présence du champ `name` dans `workflow.json`, la présence d'un `Quick start`, et que `Process` contient au moins 2 étapes.
- Ajouter un test unitaire dans `scripts/tests/test_documentation.py`.

9) Quick start (for contributors)
- Importer un workflow de `workflows/.../workflow.json` dans une instance n8n locale.
- Remplir `Gmail OAuth2` / `Telegram` credentials en local.
- Exécuter :
  ```bash
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1    # Windows PowerShell
  pip install -r requirements.txt
  pytest -q
  ```

10) Screenshots & examples
- Ajoutez un petit `Example` (code block or sample output) dans README pour les workflows complexes.
- Inclure au moins une capture d'écran (`assets/`) pour les workflows UI‑heavy.

11) Quick rules for contributors
- Toujours exécuter `pytest` avant d'ouvrir une PR.
- Lancer `scripts/sanitize_workflows.py --dry-run` avant commit si vous modifiez workflows.
- Utiliser le template `workflow-checklist.md` pour PRs qui ajoutent/modifient workflows.

Références
- `docs/workflow-checklist.md` — checklist à joindre aux PRs
- `scripts/validators/documentation_validator.py` — règles automatiques

---

Examples and short templates are available in `workflows/` — use them as canonical patterns.
