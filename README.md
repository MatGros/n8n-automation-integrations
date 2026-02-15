# n8n Automation Integrations

Ce dépôt centralise les workflows n8n pour l'automatisation des processus.
Instance n8n cible : [https://n8n.srv830801.hstgr.cloud](https://n8n.srv830801.hstgr.cloud)

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
| **Telegram Echo Bot** | Bot Telegram simple qui renvoie les messages reçus. | [`telegram-echo-bot.json`](workflows/active/telegram-echo-bot.json) |

### En Développement (`workflows/development/`)

| Workflow                 | Description                                                              | Fichier                                                                                        |
| ------------------------ | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| **Gmail AI Responder**   | Analyse les emails, génère des brouillons de réponse et labelise via IA. | [`gmail-ai-auto-responder.json`](workflows/development/gmail-ai-auto-responder.json)           |
| **Social Media Creator** | Génération automatique de contenu pour réseaux sociaux (en cours).       | [`social-media-content-creator.json`](workflows/development/social-media-content-creator.json) |

### Templates (`workflows/templates/`)

| Workflow              | Description                                  | Fichier                                                                                          |
| --------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **News Chat Agent**   | Agent IA conversant sur l'actualité via RSS. | [`chat-with-the-news.json`](workflows/templates/chat-with-the-news.json)                         |
| **Lead Gen Telegram** | Agent de génération de leads via Telegram.   | [`lead-gen-agent-telegram.json`](workflows/templates/lead-gen-agent-telegram.json)               |
| **Lead Gen Gemini**   | Variante Gemini de l'agent Lead Gen.         | [`lead-gen-agent-telegram-gemini.json`](workflows/templates/lead-gen-agent-telegram-gemini.json) |

## 📏 Conventions

- **Nom des fichiers** : `kebab-case.json` (ex: `mon-workflow-super-cool.json`)
- **Édition** : Voir le [Guide d'édition des workflows](docs/workflow-editing-guide.md) pour les bonnes pratiques de collaboration.

## 🚀 Contribution

1. **Jamais de secrets** dans le JSON (clés API, mots de passe). Utilisez les Credentials n8n.
2. Toujours tester un workflow dans `development/` avant de le passer en `active/`.
3. Mettre à jour ce README lors de l'ajout d'un nouveau workflow.
