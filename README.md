# Claude Code Skills - Analyse de Code React/TypeScript

Collection de 4 skills officiels au format Anthropic pour l'analyse rigoureuse de code React/TypeScript.

> **Principe fondamental :** Ces skills suivent la règle "NEVER HALLUCINATE" - ils ne rapportent que des problèmes réellement vérifiés dans le code, jamais d'hypothèses.

## 🎯 Skills Disponibles

### 1. 🔍 code-quality-analyzer
**Analyse de qualité de code React/TypeScript**

Détecte les problèmes réels de qualité :
- ❌ Variables d'état non utilisées (useState, useRef, useCallback)
- ❌ Boutons non-fonctionnels (onClick vide ou avec console.log)
- ❌ Gestion d'erreur manquante (try/catch absents)
- ❌ Browser `confirm()` au lieu de modals personnalisées
- ❌ Actions destructives sans confirmation
- ❌ États de chargement manquants
- ❌ États vides non gérés (écran blanc si aucune donnée)
- ❌ Problèmes d'accessibilité basiques (boutons sans label)

**Format du rapport :** Chaque problème inclut le numéro de ligne exact, le code problématique, l'impact utilisateur, et une solution avec estimation de temps.

---

### 2. ♿ accessibility-checker
**Analyse d'accessibilité conforme WCAG 2.1**

Détecte les violations d'accessibilité réelles :
- ❌ ARIA labels manquants sur boutons icône-only
- ❌ HTML non-sémantique (`<div onClick>` au lieu de `<button>`)
- ❌ Navigation clavier impossible (tabIndex manquant)
- ❌ Gestion du focus manquante dans les modals
- ❌ Labels de formulaire absents ou mal associés
- ❌ Images sans alt text approprié
- ❌ Couleur comme seul indicateur (problème pour daltoniens)
- ❌ Contenu dynamique non-annoncé aux lecteurs d'écran
- ❌ Éléments disabled sans explication
- ❌ Modals sans role="dialog" ou sans fermeture Escape

**Références WCAG :** Chaque problème est lié à un critère WCAG spécifique (1.1.1, 2.1.1, 4.1.2, etc.)

---

### 3. 🎨 visual-consistency-checker
**Détection d'incohérences visuelles entre composants**

Compare les styles réels entre plusieurs fichiers :
- ⚠️ Tabs avec styles différents (pill vs underline)
- ⚠️ Boutons primaires avec tailles/padding différents
- ⚠️ Cards avec shadows ou border-radius incohérents
- ⚠️ Spacing incohérent (gap-2 vs gap-4 pour même contexte)
- ⚠️ Typographie variable (h2 avec text-2xl vs text-xl)
- ⚠️ États vides avec styles différents
- ⚠️ Indicateurs de chargement variés
- ⚠️ Icônes de tailles différentes (w-4 vs w-5 vs w-6)
- ⚠️ Formulaires stylés différemment
- ⚠️ Modals avec padding/structure différents

**Méthodologie :** Lit au minimum 2 fichiers, extrait les className exacts, et documente les différences précises avec recommandation de standardisation.

---

### 4. 🔧 refactoring-analyzer
**Analyse de refactoring et maintenabilité du code**

Identifie les opportunités de refactoring pour améliorer la maintenabilité :
- 🔄 Code dupliqué (3+ occurrences)
- 📏 Fonctions/composants trop longs (>50/300 lignes)
- 🔀 Complexité cyclomatique élevée (>5 branches)
- ⚖️ Composants avec trop de responsabilités (SRP violation)
- 🪝 Opportunités d'extraction de hooks personnalisés
- 🧩 Opportunités d'extraction de composants
- 📦 Props drilling (3+ niveaux)
- 🔢 Nombres/chaînes magiques
- 📋 Listes de paramètres longues (5+ params)
- 🤔 Logique conditionnelle complexe
- 💀 Code mort (dead code)
- ⚠️ Patterns inconsistants entre fichiers

**Méthodologie :** Mesure objectivement la complexité (lignes, branches, occurrences), fournit métriques précises avec numéros de ligne, et propose des étapes concrètes de refactoring avec estimation de temps et évaluation du risque.

---

## 📥 Installation Rapide

### Sur votre ordinateur local

```bash
# 1. Cloner le repository
git clone https://github.com/SRMaison999/claude-agents-skills.git
cd claude-agents-skills

# 2. Aller sur la branche avec les skills
git checkout claude/repo-access-setup-011CUouyieGWSxu6Dw8rT8mG

# 3. Installer dans Claude Code (script automatique)
./install-skills.sh
```

Le script copie automatiquement les skills dans `~/.claude/skills/` sur votre machine.

### Installation manuelle

```bash
mkdir -p ~/.claude/skills/
cp -r skills/* ~/.claude/skills/
```

### Vérifier l'installation

```bash
ls -la ~/.claude/skills/
# Doit afficher :
# accessibility-checker/
# code-quality-analyzer/
# visual-consistency-checker/
```

---

## 🚀 Utilisation dans Claude Code

### Demander à Claude d'utiliser un skill

```
"Utilise le skill code-quality-analyzer pour analyser src/components/Dashboard.tsx"

"Utilise le skill accessibility-checker pour vérifier l'accessibilité de LoginPage.tsx"

"Utilise le skill visual-consistency-checker pour comparer HomePage.tsx et SettingsPage.tsx"

"Utilise le skill refactoring-analyzer pour identifier les opportunités de refactoring dans src/"
```

### Exemple de rapport généré

```
Issue #1: Unused State Variable - editingUser
File: src/components/UserList.tsx
Line: 23

Code:
const [editingUser, setEditingUser] = useState<string | null>(null)
// ...
<button onClick={() => setEditingUser(user.id)}>Edit</button>

Problem: editingUser is set but never read anywhere in the component

How I verified:
- Searched entire file for "editingUser"
- Found declaration (line 23) and setter (line 156)
- No conditional rendering or modal based on editingUser
- No other usage found

User Impact: Edit button appears clickable but does nothing visible

Fix: Either implement edit modal or disable button

Effort: 2-4 hours (implement) or 5 minutes (disable)
```

---

## 📖 Format des Skills

Chaque skill suit le **format officiel Anthropic** :

```
skills/
├── code-quality-analyzer/
│   └── SKILL.md
├── accessibility-checker/
│   └── SKILL.md
└── visual-consistency-checker/
    └── SKILL.md
```

### Structure d'un SKILL.md

```markdown
---
name: mon-skill
description: Description concise du skill
---

# Mon Skill

Instructions détaillées pour Claude...

## Core Principle
**NEVER HALLUCINATE.** Only report verified issues.

## Analysis Checklist
### 1. Premier point à vérifier
- Étapes de vérification...

## How to Verify Issues
1. Read actual code
2. Search entire file
3. Check line numbers
4. Extract code snippet
5. Explain impact

## Report Format
[Format structuré du rapport]

## What NOT to Report
[Choses à éviter]
```

---

## ✅ Différence avec les anciens "agents"

| Aspect | ❌ Anciens agents Python | ✅ Nouveaux Skills Anthropic |
|--------|-------------------------|------------------------------|
| Format | Scripts Python custom | Format officiel Anthropic (SKILL.md) |
| Hallucinations | Inventaient des problèmes | NEVER HALLUCINATE - seulement du vérifié |
| Preuves | Pas de preuve | Numéros de ligne + code exact + vérification |
| Documentation | Dispersée | Instructions claires dans SKILL.md |
| Maintenance | Difficile | Format standard, facile à maintenir |
| Installation | Dépendances Python | Simple copie de fichiers markdown |

---

## 🔧 Développement

### Créer un nouveau skill

1. **Créer la structure**
   ```bash
   mkdir -p skills/mon-nouveau-skill
   ```

2. **Créer le SKILL.md**
   ```markdown
   ---
   name: mon-nouveau-skill
   description: Description courte (utilisée par Claude pour choisir)
   ---

   # Mon Nouveau Skill

   [Instructions détaillées]
   ```

3. **Tester localement**
   ```bash
   cp -r skills/mon-nouveau-skill ~/.claude/skills/
   ```

4. **Demander à Claude**
   ```
   "Utilise le skill mon-nouveau-skill pour analyser mon code"
   ```

---

## 📚 Ressources

- **[Documentation officielle Anthropic Skills](https://github.com/anthropics/skills)**
- **[Template officiel SKILL.md](https://github.com/anthropics/skills/blob/main/template-skill/SKILL.md)**
- **[Exemples de skills Anthropic](https://github.com/anthropics/skills)** (webapp-testing, artifacts-builder, mcp-server, etc.)

---

## 🤝 Contribution

Les skills sont actuellement sur la branche : **`claude/repo-access-setup-011CUouyieGWSxu6Dw8rT8mG`**

Pour contribuer :
1. Fork ce repository
2. Créer une branche feature
3. Ajouter/améliorer un skill
4. Tester avec Claude Code
5. Créer une Pull Request

---

## 📝 Licence

MIT

---

## 💡 Support

Questions ? Problèmes ? Ouvrez une issue sur GitHub !

**Important :** Ces skills fonctionnent avec Claude Code et suivent le format officiel Anthropic. Ils ne sont pas des scripts Python autonomes mais des instructions markdown que Claude lit et suit rigoureusement.
