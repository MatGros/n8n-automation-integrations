# n8n Automation Integrations

[![Docs validation](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/docs-validation.yml/badge.svg)](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/docs-validation.yml) [![PR template enforcer](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/pr-template-enforcer.yml/badge.svg)](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/pr-template-enforcer.yml) [![Architecture checks](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/architecture-validation.yml/badge.svg)](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/architecture-validation.yml) [![Security checks](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/security-check.yml/badge.svg)](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/security-check.yml)

Ce dépôt centralise les workflows n8n pour l'automatisation des processus.
Pour déployer ces workflows, connectez-vous à votre instance n8n personnelle.

## Quick Start
1. Créez et activez un environnement virtuel Python :
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1    # PowerShell on Windows
   pip install -r requirements.txt
   ```
2. Exécutez la suite de tests : `pytest -q`
3. Pour vérifier la documentation : `python scripts/validators/documentation_validator.py workflows`
4. Avant un PR : `pre-commit run --all-files` et `python scripts/sanitize_workflows.py workflows --dry-run`

## 📂 Structure du projet

L'organisation des fichiers suit une logique par statut de workflow :

```
n8n-automation-integrations/
├── workflows/
│   ├── active/        # Workflows actuellement actifs en production
│   ├── development/   # Workflows en cours de création ou modification
│   └── templates/     # Templates importés pour référence
├── docs/              # Documentation technique et guides
└── .qoder/            # Configuration spécifique Qoder
```

## 🤖 Inventaire des Workflows

### Actifs (`workflows/active/`)

| Workflow              | Description                                         | Fichier                                                             |
| --------------------- | --------------------------------------------------- | ------------------------------------------------------------------- |
| **Telegram Echo Bot** | Bot Telegram simple qui renvoie les messages reçus. | [`echo-bot/workflow.json`](workflows/01-communication/telegram/echo-bot/workflow.json) |

### En Développement (`workflows/development/`)

| Workflow                 | Description                                                              | Fichier                                                                                        |
| ------------------------ | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| **Gmail AI Responder**   | Analyse les emails, génère des brouillons de réponse et labelise via IA. | [`gmail-ai-auto-responder.json`](workflows/development/gmail-ai-auto-responder.json)           |
| **Social Media Creator** | Génération automatique de contenu pour réseaux sociaux (en cours).       | [`multi-platform-creator/workflow.json`](workflows/02-marketing/social-media/multi-platform-creator/workflow.json) |

### Templates (`workflows/templates/`)

| Workflow              | Description                                  | Fichier                                                                                          |
| --------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **News Chat Agent**   | Agent IA conversant sur l'actualité via RSS. | [`rss-chat-agent/workflow.json`](workflows/04-data-intelligence/news-agents/rss-chat-agent/workflow.json)                         |
| **Lead Gen Telegram** | Agent de génération de leads via Telegram.   | [`telegram-agent/workflow.json`](workflows/03-sales/lead-generation/telegram-agent/workflow.json)               |
| **Lead Gen Gemini**   | Variante Gemini de l'agent Lead Gen.         | [`lead-gen-telegram-gemini.json`](workflows/99-templates/lead-gen/lead-gen-telegram-gemini.json) |

## 📏 Conventions

- **Nom des fichiers** : `kebab-case.json` (ex: `mon-workflow-super-cool.json`)
- **Édition** : Voir le [Guide d'édition des workflows](docs/workflow-editing-guide.md) pour les bonnes pratiques de collaboration.

## 🚀 Contribution

1. **Jamais de secrets** dans le JSON (clés API, mots de passe). Utilisez les Credentials n8n.
2. Toujours tester un workflow dans `development/` avant de le passer en `active/`.
3. Mettre à jour ce README lors de l'ajout d'un nouveau workflow.

## 🧰 Developer checks
- Run the sanitization script: `python scripts/sanitize_workflows.py workflows --dry-run` (use `--force` to apply).
- Run security tests: `pytest -q` (tests live in `scripts/tests/test_security.py`).
