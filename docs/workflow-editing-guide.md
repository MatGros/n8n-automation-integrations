# Guide d'édition des Workflows n8n

_Dernière mise à jour: 2026-02-19 • Audience: Contributeurs & Mainteneurs_

Ce document décrit les méthodes recommandées pour collaborer sur les workflows de ce dépôt.

## Méthode Recommandée : API n8n + Git

Pour une collaboration fluide entre humains et IA, nous privilégions l'utilisation de l'API n8n pour appliquer les modifications, couplée à Git pour le versionnement.

### Pré-requis

1. Une clé API n8n (générée dans _Settings > API_ sur votre instance).
2. L'ID du workflow à modifier.

### Processus

1. **Lecture** : L'IA lit le workflow actuel depuis le fichier JSON du dépôt ou directement via l'API n8n.
2. **Modification** : L'IA propose des changements (code JSON ou description des nœuds).
3. **Application** :
   - _Option A (Recommandée)_ : L'IA utilise l'API n8n (`PUT /workflows/{id}`) pour mettre à jour le workflow directement sur l'instance.
   - _Option B (Manuelle)_ : Vous copiez le JSON modifié, le collez dans un fichier, et l'importez manuellement dans n8n.
4. **Sauvegarde** : Une fois validé, exportez le workflow JSON mis à jour dans ce dépôt et faites un commit Git.

## Méthode Alternative : Export UI

Si vous faites des modifications visuelles importantes (ajout/déplacement de nombreux nœuds) :

1. Faites vos modifications dans l'interface web n8n.
2. Sélectionnez tous les nœuds (Ctrl+A) et copiez (Ctrl+C) OU utilisez le menu "Download" du workflow.
3. Remplacez le contenu du fichier JSON correspondant dans ce dépôt (`workflows/...`).
4. Committez les changements Git.

## Bonnes Pratiques

- **Pas de Credentials** : Assurez-vous que l'export ne contient pas de données sensibles. n8n gère cela par défaut (les credentials sont référencés par ID), mais soyez vigilants avec les valeurs "en dur" dans les nœuds.
- **Nommage** : Gardez les noms de fichiers en `kebab-case`.
- **Statut** : Déplacez le fichier dans `workflows/active` uniquement quand il est testé et fonctionnel.
