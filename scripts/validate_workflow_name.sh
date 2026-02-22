#!/bin/bash

# Script de validation du nommage et de l'emplacement d'un workflow
# Usage: ./validate_workflow_name.sh <nom-du-fichier> <chemin-de-destination>

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <nom-du-fichier> <chemin-de-destination>"
    exit 1
fi

FILENAME=$1
DEST_PATH=$2

# 1. Vérification de l'extension
if [[ "$FILENAME" != *.json ]]; then
    echo "❌ Erreur: Le fichier doit avoir l'extension .json"
    exit 1
fi

# 2. Vérification du kebab-case (nom de base sans extension ni suffixe de statut)
BASENAME=$(basename "$FILENAME" .json)
# Suppression des suffixes autorisés (ex: _PUB_20260221)
CLEAN_NAME=$(echo "$BASENAME" | sed -E 's/_(PUB|DEV|DRF|DEP|ARC)_[0-9]{8}$//')

if ! [[ "$CLEAN_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "❌ Erreur: Le nom de base '$CLEAN_NAME' ne respecte pas la convention kebab-case (minuscules, chiffres, tirets)."
    exit 1
fi

# 3. Vérification du chemin de destination
if [[ "$DEST_PATH" != workflows/* ]]; then
    echo "❌ Erreur: Le chemin de destination doit commencer par 'workflows/'"
    exit 1
fi

# 4. Vérification de la catégorie (doit commencer par un numéro)
CATEGORY=$(echo "$DEST_PATH" | cut -d'/' -f2)
if ! [[ "$CATEGORY" =~ ^[0-9]{2}-[a-z0-9-]+$ ]]; then
    echo "❌ Erreur: La catégorie '$CATEGORY' ne respecte pas le format attendu (ex: 01-communication)."
    exit 1
fi

# 5. Vérification des sous-dossiers (kebab-case)
IFS='/' read -ra PATH_PARTS <<< "$DEST_PATH"
for i in "${!PATH_PARTS[@]}"; do
    if [ $i -gt 1 ]; then # Ignorer 'workflows' et la catégorie
        PART="${PATH_PARTS[$i]}"
        if ! [[ "$PART" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
            echo "❌ Erreur: Le sous-dossier '$PART' ne respecte pas la convention kebab-case."
            exit 1
        fi
    fi
done

echo "✅ Validation réussie: Le nommage et l'emplacement sont conformes aux règles."
exit 0
