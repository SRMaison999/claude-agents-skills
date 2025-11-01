# INDEX - Collection d'Agents Claude

Vue d'ensemble complète de tous les agents disponibles.

**Dernière mise à jour** : 2025-10-31  
**Agents totaux** : 7  
**Agents fonctionnels** : 1  
**Agents documentés** : 7  

---

## 📊 Statut global

| # | Agent | Status | Code | Priorité | Domaine |
|---|-------|--------|------|----------|---------|
| 1 | Button Validator V2 | ✅ Fonctionnel | ✅ 800 lignes | Haute | UI/UX |
| 2 | Props & Form Validator V2 | 📝 Doc | ⏳ À faire | Haute | UI/Props |
| 3 | Dead Code Cleaner V2 | 📝 Doc | ⏳ À faire | Haute | Nettoyage |
| 4 | Code Fixer V2 | 📝 Doc | ⏳ À faire | Haute | Correction |
| 5 | Component Consistency Checker V2 | 📝 Doc | ⏳ À faire | Moyenne | Cohérence |
| 6 | Agent Coordinator V2 | 📝 Doc | ⏳ À faire | Critique | Orchestration |
| 7 | README Editor V2 | 📝 Doc | ⏳ À faire | Basse | Documentation |

---

## 🎯 Par domaine

### 🎨 UI/UX & Cohérence
- **Button Validator V2** ✅ - Boutons (fonctionnalité + style)
- **Props & Form Validator V2** 📝 - Props, Modales, Formulaires, Emojis
- **Component Consistency Checker V2** 📝 - Cohérence entre composants similaires

### 🧹 Nettoyage & Maintenance
- **Dead Code Cleaner V2** 📝 - Code mort, imports inutilisés, console.log

### 🔧 Correction & Application
- **Code Fixer V2** 📝 - Application automatique des corrections

### 🎼 Orchestration
- **Agent Coordinator V2** 📝 - Chef d'orchestre de tous les agents

### 📝 Documentation
- **README Editor V2** 📝 - Génération et maintenance README

---

## 🚀 Par priorité d'implémentation

### 🔴 Priorité HAUTE (besoin immédiat)
1. **Props & Form Validator V2** - Emojis + Props critiques
2. **Dead Code Cleaner V2** - Nettoyer le code inutile
3. **Code Fixer V2** - Appliquer les corrections

### 🟠 Priorité MOYENNE
4. **Component Consistency Checker V2** - Cohérence visuelle

### 🟢 Priorité BASSE (peut attendre)
5. **README Editor V2** - Documentation

### ⭐ Priorité CRITIQUE (infrastructure)
6. **Agent Coordinator V2** - Nécessaire pour workflow complet

---

## 📋 Fonctionnalités par agent

### Button Validator V2 ✅
```
✅ Auto-détection stack (React, Vue, Tailwind, MUI, etc.)
✅ Détection boutons sans handler
✅ Vérification cohérence Tailwind
✅ Apprentissage continu (mémoire permanente)
✅ Corrections auto si confiance >90%
✅ Rapport détaillé avec solutions
```

### Props & Form Validator V2 📝
```
- Props manquantes/inutilisées/types incorrects
- Structure modales (header, body, footer)
- Formulaires (labels, validation, messages)
- ⚠️ DÉTECTION EMOJIS STRICTE (priorité absolue)
- Cohérence visuelle Tailwind
- Apprentissage continu
```

### Dead Code Cleaner V2 📝
```
- Imports non utilisés
- Variables/fonctions jamais appelées
- Composants jamais importés
- Console.log oubliés
- Code commenté obsolète
- Props inutilisées
- Sécurité : ne touche jamais exports/routes/configs
```

### Code Fixer V2 📝
```
- Lit rapports de tous les agents
- Applique corrections auto (confiance >90%)
- Suppression emojis automatique
- Uniformisation CSS/Tailwind
- Nettoyage imports/console.log
- Backup et rollback automatiques
- Commits Git descriptifs
```

### Component Consistency Checker V2 📝
```
- Groupe composants similaires
- Analyse patterns visuels
- Détecte incohérences structurelles
- Vérifie conventions de props
- États visuels (hover, focus, disabled)
- Accessibilité cohérente
```

### Agent Coordinator V2 📝
```
- Lance agents en parallèle
- Compile rapports en rapport maître
- Priorise corrections intelligemment
- Workflow : Analyse → Compilation → Priorisation → 
  Validation → Exécution → Vérification
- Détection de conflits entre corrections
- Rapport final complet
```

### README Editor V2 📝
```
- Génère README.md principal
- README.md par dossier
- Détecte changements (deps, composants, features)
- Mise à jour automatique
- Diagrammes d'architecture (Mermaid)
- Documentation composants individuels
- Sections API/Tests/Scripts auto
```

---

## 🎯 Cas d'usage typiques

### Scénario 1 : Nouveau projet (audit initial)
```
1. Button Validator      → Détecte problèmes boutons
2. Props Validator       → Détecte emojis + props
3. Consistency Checker   → Analyse cohérence
4. Dead Code Cleaner     → Identifie code mort
5. Agent Coordinator     → Compile tout
6. Review manuel         → Valide les corrections
7. Code Fixer            → Applique corrections
```

### Scénario 2 : Maintenance régulière
```
1. Agent Coordinator --quick
   → Lance Button + Props + Dead Code
2. Review rapide
3. Code Fixer --auto
   → Applique tout ce qui est >90%
```

### Scénario 3 : Avant release
```
1. Agent Coordinator --full
   → Tous les agents + vérifications complètes
2. README Editor
   → Met à jour documentation
3. Review complet
4. Code Fixer --careful
   → Corrections graduelles avec validation
```

### Scénario 4 : Urgence (emojis détectés en prod)
```
1. Props Validator --emoji-only
2. Code Fixer --emoji-only --auto
   → Suppression immédiate tous emojis
```

---

## 🔗 Dépendances entre agents

```
Agent Coordinator (orchestrateur)
    ├─> Button Validator (analyseur)
    ├─> Props & Form Validator (analyseur)
    ├─> Component Consistency Checker (analyseur)
    ├─> Dead Code Cleaner (analyseur)
    └─> Code Fixer (exécuteur)
           └─> Lit rapports de tous les analyseurs

README Editor (indépendant)
    └─> Peut être lancé séparément ou par Coordinator
```

---

## 📈 Roadmap de développement

### Sprint 1 (Urgent)
- [ ] Coder Props & Form Validator V2
- [ ] Coder Dead Code Cleaner V2
- [ ] Coder Code Fixer V2

### Sprint 2 (Important)
- [ ] Coder Component Consistency Checker V2
- [ ] Coder Agent Coordinator V2

### Sprint 3 (Nice to have)
- [ ] Coder README Editor V2
- [ ] Route Analyzer V2
- [ ] TypeScript Validator V2

### Sprint 4 (Avancé)
- [ ] Test Generator V2
- [ ] JSDoc Generator V2
- [ ] Performance Analyzer V2

---

## 💡 Recommandations d'utilisation

### Pour démarrer
1. **Button Validator** (déjà fonctionnel)
2. Attendre **Props & Form Validator** (emojis + props)
3. Attendre **Code Fixer** (pour appliquer corrections)

### Pour être productif
1. **Agent Coordinator** devient essentiel
2. Lance tout en une commande
3. Review et validation centralisée

### Pour la qualité
1. **Consistency Checker** assure cohérence
2. Lance régulièrement (1x/semaine)
3. Corrige les dérives progressivement

---

## 🛠️ Installation et setup

### Prérequis globaux
- Python 3.7+
- Node.js (pour détecter le projet)
- Git (optionnel, pour commits auto)

### Structure recommandée
```
~/claude-agents/          # Clone du repo
├── button-validator-v2-learning/
├── props-form-validator-v2/
├── dead-code-cleaner-v2/
├── code-fixer-v2/
├── component-consistency-checker-v2/
├── agent-coordinator-v2/
└── readme-editor-v2/

~/projects/
└── travel-planner/      # Ton projet
    └── brain/           # Créé automatiquement par agents
        └── projects/    # Mémoire par projet
```

---

## 📞 Support et troubleshooting

### Agent ne détecte pas le projet
→ Vérifier présence de package.json

### Mémoire corrompue
→ Supprimer `brain/projects/{hash}/` et relancer

### Corrections trop agressives
→ Ajuster seuil dans l'agent (ligne confidence >= 90)

### Conflits entre corrections
→ Agent Coordinator les détecte automatiquement

---

## 📜 Conventions

### Nommage des agents
Format : `{nom}-v{version}`
Exemple : `button-validator-v2`

### Structure des agents
```
agent-name-v2/
├── SKILL.md              # Documentation technique
├── agent_name_v2.py      # Code Python
├── README.md             # Guide utilisateur
└── brain/                # Mémoire (créé à l'exécution)
```

### Rapports générés
Format : `{agent}-{type}-{timestamp}.md`
Exemple : `button-analysis-20251031-143022.md`

---

**Créé pour** : Maintenance automatisée et qualité du code  
**Licence** : Usage projet personnel ou équipe  
**Version INDEX** : 1.0.0
