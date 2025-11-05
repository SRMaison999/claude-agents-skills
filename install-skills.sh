#!/bin/bash

# Script d'installation des Skills Anthropic dans Claude Code
# Usage: ./install-skills.sh

set -e

echo "🚀 Installation des Skills Anthropic pour Claude Code"
echo ""

# Vérifier que le dossier skills existe
if [ ! -d "skills" ]; then
    echo "❌ Erreur: Le dossier 'skills/' n'existe pas"
    echo "   Assurez-vous d'être dans le répertoire claude-agents-skills"
    exit 1
fi

# Créer le dossier ~/.claude/skills/ si nécessaire
echo "📁 Création du dossier ~/.claude/skills/ ..."
mkdir -p ~/.claude/skills/

# Copier les skills
echo "📦 Copie des skills ..."
cp -r skills/* ~/.claude/skills/

# Vérifier l'installation
echo ""
echo "✅ Installation terminée !"
echo ""
echo "📊 Skills installés :"
ls -1 ~/.claude/skills/
echo ""
echo "📖 Les skills disponibles :"
echo "  • code-quality-analyzer    - Analyse de qualité de code React/TypeScript"
echo "  • accessibility-checker    - Analyse d'accessibilité (WCAG)"
echo "  • visual-consistency-checker - Détection d'incohérences visuelles"
echo ""
echo "🎯 Pour utiliser un skill dans Claude Code :"
echo "   Demandez à Claude : 'Utilise le skill code-quality-analyzer pour analyser ce fichier'"
echo ""
