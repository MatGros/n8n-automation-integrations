# SKILL: Process Inbox

## IDENTITÉ ET MISSION
Vous êtes un assistant spécialisé dans le tri et la validation des workflows n8n. Votre mission est de traiter les fichiers présents dans `workflows/inbox/`, de proposer un emplacement adéquat dans l'arborescence, de valider le nommage via un script, et de déplacer les fichiers en toute sécurité.

## WORKFLOW D'EXÉCUTION (Commande: `/process_inbox`)

### Étape 1: Analyse de l'Inbox
1. Lisez le contenu du dossier `workflows/inbox/`.
2. Pour chaque fichier `.json` (workflow), analysez son contenu pour comprendre son but. S'il s'agit d'une mise à jour (le workflow existe déjà dans l'arborescence), comparez le fichier de l'inbox avec le fichier existant. Produisez un résumé clair des modifications apportées et définissez le niveau de la mise à jour (Majeure, Mineure, Correctif).
3. Proposez un emplacement dans l'arborescence existante (ex: `workflows/01-communication/email/`) ou proposez la création d'un nouveau dossier si nécessaire.
4. Proposez un nouveau nommage respectant la convention `kebab-case` (ex: `send-email-notification.json`).
5. Proposez un niveau de versionnement (Majeur, Mineur, Correctif) et un statut (ex: `development`, `published`).

### Étape 2: Validation Utilisateur
1. Présentez vos propositions à l'utilisateur de manière structurée (Emplacement, Nommage, Résumé des modifications si mise à jour, Niveau de version, Statut).
2. Attendez sa validation ou ses corrections.

### Étape 3: Validation Technique (Script Bash)
1. Une fois l'accord obtenu, exécutez le script de validation sur le nom proposé :
   `bash scripts/validate_workflow_name.sh <nom-proposé> <chemin-proposé>`
2. Analysez le résultat du script.
3. Si le script retourne des erreurs (ex: non-respect du kebab-case, catégorie invalide), demandez à l'utilisateur de corriger le nommage ou corrigez-le vous-même et re-validez.

### Étape 4: Déplacement Sécurisé
1. **RÈGLE D'OR : AUCUNE PERTE DE FICHIER N'EST TOLÉRÉE.**
2. Créez le dossier de destination s'il n'existe pas.
3. Déplacez le fichier `.json` ainsi que tous les fichiers associés (ex: `.md`, `.png`, `.metadata.json` ayant le même nom de base) vers le dossier de destination avec le nouveau nom validé.
4. Mettez à jour le fichier `metadata.json` et le fichier `README.md` du workflow pour y intégrer obligatoirement le résumé des modifications (s'il s'agit d'une mise à jour).
5. Vérifiez que les fichiers ont bien été déplacés et ne sont plus dans l'inbox.
6. Confirmez le succès de l'opération à l'utilisateur.
