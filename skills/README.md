# Skills Anthropic pour Claude Code

Collection de 3 skills officiels au format Anthropic pour l'analyse de code React/TypeScript.

## 🎯 Skills Disponibles

### 1. code-quality-analyzer 🔍
**Analyse de qualité de code React/TypeScript**

Détecte :
- Variables d'état non utilisées
- Boutons non-fonctionnels
- Gestion d'erreur manquante
- Browser `confirm()` au lieu de modals personnalisées
- Actions destructives sans confirmation
- États de chargement manquants
- États vides non gérés
- Problèmes d'accessibilité basiques

### 2. accessibility-checker ♿
**Analyse d'accessibilité conforme WCAG**

Détecte :
- ARIA labels manquants
- HTML non-sémantique
- Navigation clavier
- Gestion du focus
- Labels de formulaire
- Alt text sur images
- Couleur comme seul indicateur
- Contenu dynamique non-annoncé
- Éléments disabled sans explication
- Accessibilité des modals

### 3. visual-consistency-checker 🎨
**Détection d'incohérences visuelles**

Compare :
- Styles de tabs
- Styles de boutons
- Cards/containers
- Spacing (gap, padding, margin)
- Typographie
- États vides
- Indicateurs de chargement
- Tailles d'icônes
- Éléments de formulaire
- Styles de modals

## 📥 Installation

### Méthode 1 : Script automatique (recommandé)

```bash
# Cloner le repo si pas encore fait
git clone https://github.com/SRMaison999/claude-agents-skills.git
cd claude-agents-skills

# Récupérer la branche avec les skills
git checkout claude/repo-access-setup-011CUouyieGWSxu6Dw8rT8mG

# Exécuter le script d'installation
./install-skills.sh
```

### Méthode 2 : Installation manuelle

```bash
# Copier les skills dans Claude Code
mkdir -p ~/.claude/skills/
cp -r skills/* ~/.claude/skills/
```

### Vérifier l'installation

```bash
ls -la ~/.claude/skills/
# Devrait afficher :
# accessibility-checker/
# code-quality-analyzer/
# visual-consistency-checker/
```

## 🚀 Utilisation

### Dans Claude Code

Demandez à Claude d'utiliser un skill :

```
"Utilise le skill code-quality-analyzer pour analyser src/components/MyComponent.tsx"

"Utilise le skill accessibility-checker pour vérifier l'accessibilité de cette page"

"Utilise le skill visual-consistency-checker pour comparer les styles entre HomePage.tsx et SettingsPage.tsx"
```

### Format des rapports

Tous les skills suivent le même principe :

✅ **NEVER HALLUCINATE** - Seulement des problèmes vérifiés
✅ Format de rapport structuré avec :
  - Numéro de ligne exact
  - Code snippet du problème
  - Explication de l'impact utilisateur
  - Solution proposée avec exemple de code
  - Estimation du temps de correction

## 📖 Format des Skills

Chaque skill suit le format officiel Anthropic :

```
skills/
├── nom-du-skill/
│   └── SKILL.md
```

Le fichier `SKILL.md` contient :
- YAML frontmatter (name, description)
- Instructions détaillées en markdown
- Checklist d'analyse
- Exemples de rapports
- Principes de vérification

## 🔧 Développement

### Créer un nouveau skill

1. Créer un dossier dans `skills/`
2. Créer un fichier `SKILL.md` avec :

```markdown
---
name: mon-skill
description: Description courte du skill
---

# Mon Skill

Instructions détaillées...

## Core Principle

**NEVER HALLUCINATE.** ...

## Analysis Checklist

### 1. Premier point
- Vérification...

## Report Format

...
```

3. Copier dans `~/.claude/skills/`

## 📚 Ressources

- [Documentation officielle Anthropic Skills](https://github.com/anthropics/skills)
- [Format SKILL.md](https://github.com/anthropics/skills/blob/main/template-skill/SKILL.md)

## 🤝 Contribution

Les skills sont dans la branche : `claude/repo-access-setup-011CUouyieGWSxu6Dw8rT8mG`

Pour contribuer :
1. Fork le repo
2. Créer une branche
3. Ajouter/modifier un skill
4. Pull request

## 📝 Licence

MIT
