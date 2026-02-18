# n8n Automation Integrations

[![Docs validation](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/docs-validation.yml/badge.svg)](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/docs-validation.yml) [![Architecture checks](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/architecture-validation.yml/badge.svg)](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/architecture-validation.yml) [![Security checks](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/security-check.yml/badge.svg)](https://github.com/MatGros/n8n-automation-integrations/actions/workflows/security-check.yml)

Un dépôt professionnel et hautement organisé centralisant les workflows n8n pour l'automatisation d'entreprise. Architecture scalable par domaine métier, documentation complète, et tests automatisés.

**🎯 Objectif:** Servir de référence pour construire, documenter et déployer des workflows n8n complexes.

---

## 📋 Table des matières

- [Quick Start](#-quick-start)
- [Structure du projet](#-structure-du-projet)
- [Workflows existants](#-workflows-existants)
- [Documentation](#-documentation)
- [Conventions](#-conventions)
- [Contribution](#-contribution)
- [Tests et validation](#-tests-et-validation)

---

## 🚀 Quick Start

### Installation & Setup

```bash
# 1. Clone le repo
git clone https://github.com/MatGros/n8n-automation-integrations.git
cd n8n-automation-integrations

# 2. Créez un environnement virtuel Python
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # PowerShell on Windows
source .venv/bin/activate        # Linux/macOS

# 3. Installez les dépendances
pip install -r requirements.txt

# 4. Exécutez les tests
pytest -q
```

### Importer un workflow

1. Accédez à votre instance n8n
2. Menu → Import → Import JSON
3. Sélectionnez le fichier `workflow.json` du dossier désiré
4. Configurez les credentials via n8n
5. Testez et activez

Voir [Deployment Guide](docs/deployment-guide.md) pour plus de détails.

---

## 📂 Structure du projet

La structure est **organisée par domaine métier** pour faciliter la découverte et la maintenance:

```
n8n-automation-integrations/
├── workflows/                      # 15 catégories + templates
│   ├── 01-communication/           # Email, Telegram, Slack, Discord
│   ├── 02-marketing/               # Social media, SEO, Campaigns
│   ├── 03-sales/                   # Lead gen, CRM, Proposals
│   ├── 04-data-intelligence/       # News agents, Data processing, ML
│   ├── 05-iot/                     # Sensors, MQTT, Smart home
│   ├── 06-industry-4.0/            # Manufacturing, Supply chain, PLC
│   ├── 07-edge-computing/          # Edge analytics, Local AI
│   ├── 08-blockchain/              # Smart contracts, NFT, DeFi
│   ├── 09-robotics/                # Robot control, Vision, ROS
│   ├── 10-cloud-infrastructure/    # AWS, Azure, GCP, Kubernetes
│   ├── 11-cybersecurity/           # Threat detection, Vulnerability
│   ├── 12-healthcare/              # Patient monitoring, HL7/FHIR
│   ├── 13-energy/                  # Smart grid, Renewable, Consumption
│   ├── 14-agriculture/             # Precision farming, Weather, Crops
│   ├── 15-transportation/          # Fleet management, Route optimization
│   └── 99-templates/               # Reusable templates and examples
├── docs/                           # Documentation complète
│   ├── by-industry/                # Guides par industrie
│   ├── by-technology/              # Guides par technologie
│   └── *.md                        # Style guides, best practices
├── scripts/                        # Automation et tests
│   ├── tests/                      # pytest suite
│   ├── validators/                 # Code validators
│   └── sanitize_workflows.py       # Security cleanup
├── archive/                        # Legacy workflows
└── README.md (this file)
```

**Détail complet:** Voir [workflows/README.md](workflows/README.md)

---

## 🤖 Workflows existants

### Production

| Workflow | Catégorie | Description | Fichier |
|----------|-----------|-------------|---------|
| **Echo Bot** | 01-communication/telegram | Bot Telegram simple | [View](workflows/01-communication/telegram/echo-bot/) |
| **Gmail AI Responder** | 01-communication/email | Analyse emails + réponses IA | [View](workflows/01-communication/email/gmail-ai-responder/) |
| **Social Media Creator** | 02-marketing/social-media | Contenu multi-plateforme | [View](workflows/02-marketing/social-media/multi-platform-creator/) |

### Templates & Références

| Workflow | Catégorie | Description | Type |
|----------|-----------|-------------|------|
| **RSS Chat Agent** | 04-data-intelligence/news-agents | IA conversante sur actualité | Template |
| **Lead Gen Agent** | 03-sales/lead-generation | Génération de leads via Telegram | Template |
| **Lead Gen Gemini** | 99-templates/lead-gen | Variante avec Gemini | Template |

**Note:** Voir [workflows/README.md](workflows/README.md) pour la liste complète et mise à jour.

---

## 📚 Documentation

Documentation complète couvrant tous les domaines:

### Par industrie

- **[IoT Guide](docs/by-industry/iot-guide.md)** — MQTT, CoAP, LoRaWAN, sensor patterns
- **[Industry 4.0 Guide](docs/by-industry/industry-4.0-guide.md)** — PLC, SCADA, OEE, Supply chain
- **[Healthcare Guide](docs/by-industry/healthcare-guide.md)** — HL7/FHIR, medical devices, compliance
- **[Energy Guide](docs/by-industry/energy-guide.md)** — Smart grid, renewable energy, consumption monitoring

### Par technologie

- **[MQTT Integration](docs/by-technology/mqtt-integration.md)** — Broker setup, QoS levels, patterns
- **[Blockchain Integration](docs/by-technology/blockchain-integration.md)** — Smart contracts, NFTs, DeFi, Web3
- **[Kubernetes Automation](docs/by-technology/kubernetes-automation.md)** — K8s API, Helm, GitOps, auto-scaling
- **[Edge Computing](docs/by-technology/edge-computing.md)** — Edge patterns, local AI, data sync

### Guides essentiels

- **[Workflow Style Guide](docs/workflow-style-guide.md)** — 7 couleurs, nommage, layout
- **[Color Reference](docs/color-reference.md)** — Codes couleur hexadécimaux et usage
- **[Security Best Practices](docs/security-best-practices.md)** — Secrets, sanitization, credential management
- **[Deployment Guide](docs/deployment-guide.md)** — Setup n8n, import, testing strategy
- **[CI/CD Setup](docs/ci-cd-setup.md)** — GitHub Actions, automated tests, deployment
- **[Contributing Guide](docs/contributing.md)** — Development workflow, PR checklist, style guide
- **[Workflow Editing Guide](docs/workflow-editing-guide.md)** — API vs UI editing best practices
- **[Workflow Checklist](docs/workflow-checklist.md)** — PR validation checklist

---

## 📏 Conventions

### Nommage

- **Fichiers/dossiers:** `kebab-case` (ex: `gmail-ai-responder`, `echo-bot`)
- **Nodes:** `verb-resource` (ex: `fetch-gmail`, `classify-email`)
- **Workflows:** Noms explicites avec contexte de domaine

### Structure fichiers

```
category/subcategory/workflow-name/
├── workflow.json       # REQUIS - Fichier n8n importable
├── README.md           # REQUIS - Documentation complète
├── template.json       # OPTIONNEL - Version template
├── test.json           # OPTIONNEL - Cas de test
├── config.json         # OPTIONNEL - Configuration
├── CHANGELOG.md        # OPTIONNEL - Historique versions
├── test-data/          # OPTIONNEL - Payloads test
└── docs/               # OPTIONNEL - Documentation additionelle
```

### Couleurs de nodes

| Couleur | Code | Usage | Exemples |
|---------|------|-------|----------|
| 🔵 Bleu | 1 | Fetch / IO | HTTP, DB, IMAP, File |
| 🟢 Vert | 2 | Logic / Transform | If/Switch, Code, Format |
| 🟡 Jaune | 3 | Storage / Persist | DB write, File, S3 |
| 🔴 Rouge | 4 | Error / Alert | Try/Catch, Error handler |
| 🟠 Orange | 5 | Triggers | Webhook, Cron, Event |
| 🟣 Violet | 6 | AI / LLM | OpenAI, Claude, Models |
| 🔵 Cyan | 7 | Communication | Slack, Email, Telegram |

Voir [Color Reference](docs/color-reference.md) pour détails complets.

---

## 🚀 Contribution

### Avant de créer un PR

1. **Lisez les guides**
   - [Contributing Guide](docs/contributing.md)
   - [Workflow Style Guide](docs/workflow-style-guide.md)
   - [Workflow Checklist](docs/workflow-checklist.md)

2. **Respectez les règles**
   - ❌ Jamais de secrets/API keys dans le JSON
   - ✅ Utilisez les Credentials n8n
   - ✅ Nommez en `kebab-case`
   - ✅ Créez `workflow.json` + `README.md`
   - ✅ Testez avant PR

3. **Checklist PR**
   - [ ] `workflow.json` valide et parseable
   - [ ] `README.md` avec toutes sections requises
   - [ ] Pas de données sensibles
   - [ ] Nommage en kebab-case
   - [ ] Tests de sécurité passent
   - [ ] Tests d'architecture passent

### Ajouter un workflow

```bash
# 1. Créez le dossier
mkdir -p workflows/XX-category/subcategory/my-workflow
cd workflows/XX-category/subcategory/my-workflow

# 2. Exportez depuis n8n (Ctrl+A → Ctrl+C) et sauvegardez en workflow.json

# 3. Créez README.md (utilisez le template de workflows/README.md)

# 4. Testez
python scripts/sanitize_workflows.py workflows --dry-run
pytest -q

# 5. Commitez
git add workflows/
git commit -m "feat(XX-category): add my-workflow"
```

---

## 🧪 Tests et validation

### Tests locaux

```bash
# Tous les tests
pytest -q

# Tests sécurité uniquement
pytest scripts/tests/test_security.py -v

# Tests structure uniquement
python scripts/tests/test_workflow_structure.py

# Validation avant commit
python scripts/sanitize_workflows.py workflows --dry-run
```

### CI/CD

Les tests s'exécutent automatiquement via GitHub Actions:

- ✅ **Security checks** — VPS URLs, credentials, IPs, emails
- ✅ **Architecture checks** — Structure, nommage, READMEs
- ✅ **Documentation checks** — Sections requises, descriptions

Badges en haut du README montrent le status.

---

## 📖 Ressources supplémentaires

- **Architecture complète:** [workflows/README.md](workflows/README.md)
- **Tous les styles:** [docs/workflow-style-guide.md](docs/workflow-style-guide.md)
- **Projets archive:** [archive/README.md](archive/README.md)
- **Sécurité:** [docs/security-best-practices.md](docs/security-best-practices.md)
- **Historique projet:** [CHANGELOG.md](CHANGELOG.md) (coming soon)

---

## 📝 License

MIT - Libre d'utilisation

## 👨‍💻 Auteur

MatGros & Contributors

---

**Dernière mise à jour:** 2026-02-18 | **Status:** ✅ Production-ready
