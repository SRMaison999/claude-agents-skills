# Claude Agents - Collection d'agents intelligents

Collection d'agents d'analyse et de maintenance de code avec apprentissage continu.

## 🎯 Agents disponibles

### ✅ Button Validator V2 - Learning Edition
**Status** : Complet et fonctionnel  
**Fonction** : Analyse exhaustive des boutons (fonctionnalité + style)  
**Apprentissage** : Oui (mémoire permanente)  
**Autonomie** : Équilibrée (>90% confiance)  

**Ce qu'il fait** :
- Détecte boutons sans handler (CRITIQUE)
- Vérifie cohérence visuelle Tailwind
- Apprend tes patterns préférés
- Corrige automatiquement après apprentissage

---

### 📝 Props & Form Validator V2
**Status** : Complet et fonctionnel ✅
**Fonction** : Analyse props, modales et formulaires + détection emojis
**Règle critique** : AUCUN EMOJI dans l'application
**Code** : props_form_validator_v2.py (870+ lignes)  

**Ce qu'il fait** :
- Props manquantes/inutilisées/types incorrects
- Structure des modales (header, body, footer)
- Formulaires (labels, validation, messages d'erreur)
- **Détection stricte emojis** (priorité absolue)
- Cohérence visuelle globale

---

### 🧹 Dead Code Cleaner V2
**Status** : Complet et fonctionnel ✅
**Fonction** : Suppression du code mort et inutilisé
**Code** : dead_code_cleaner_v2.py (640+ lignes)  

**Ce qu'il fait** :
- Imports non utilisés
- Variables/fonctions jamais appelées
- Composants jamais importés
- Console.log oubliés
- Code commenté obsolète
- Props inutilisées

**Sécurité** : Ne touche JAMAIS aux exports, routes ou configs

---

### 🔧 Code Fixer V2
**Status** : Complet et fonctionnel ✅
**Fonction** : Application automatique des corrections validées
**Code** : code_fixer_v2.py (720+ lignes)  

**Ce qu'il fait** :
- Lit les rapports des autres agents
- Applique les corrections auto (confiance >90%)
- Vérifie intégrité (syntaxe, compilation, tests)
- Crée commits Git
- Rollback automatique si erreur

**Sécurité** : Backup avant modifications, validation stricte

---

## 🚀 Utilisation rapide

### Agent individuel

```bash
# Button Validator
cd button-validator-v2-learning
python button_validator_v2.py /chemin/vers/projet

# Props & Form Validator (à venir)
cd props-form-validator-v2
python props_form_validator_v2.py /chemin/vers/projet

# Dead Code Cleaner (à venir)
cd dead-code-cleaner-v2
python dead_code_cleaner_v2.py /chemin/vers/projet

# Code Fixer (à venir)
cd code-fixer-v2
python code_fixer_v2.py --auto
```

### Depuis Claude Code

```
Lance button-validator-v2-learning sur mon projet
```

```
Lance props-form-validator-v2 sur mon projet
```

```
Lance dead-code-cleaner-v2 sur mon projet
```

---

## 📊 Workflow multi-agents recommandé

### Phase 1 : Analyse (lecture seule)
1. **Button Validator** → Détecte problèmes boutons
2. **Props & Form Validator** → Détecte props/modales/forms/emojis
3. **Dead Code Cleaner** → Identifie code mort

### Phase 2 : Review
- Lire tous les rapports générés
- Prioriser les corrections
- Valider ce qui doit être corrigé

### Phase 3 : Application
- **Code Fixer** → Applique les corrections validées

### Phase 4 : Vérification
- Relancer les agents analyseurs
- Comparer les rapports (avant/après)
- Valider que tout est correct

---

## 🧠 Apprentissage continu

Tous les agents V2 utilisent un système d'apprentissage :

**Scan 1-2** : Observation, mémorisation  
**Scan 3-5** : Calcul des patterns standards  
**Scan 6-10** : Corrections partiellement autonomes  
**Scan 10+** : Expert, haute autonomie (80%+)  

La mémoire est **permanente** et **spécifique par projet**.

---

## 🎯 Règles communes

### Ce que les agents PEUVENT faire automatiquement
- ✅ Modifications CSS/Tailwind (visuelles)
- ✅ Suppression d'emojis
- ✅ Nettoyage imports/console.log
- ✅ Corrections syntaxiques simples

### Ce que les agents NE PEUVENT PAS faire automatiquement
- ❌ Modifier la logique métier
- ❌ Ajouter/supprimer des fonctions
- ❌ Restructurer le code
- ❌ Modifier les types TypeScript (sauf simple)

**Toute modification de logique nécessite validation humaine.**

---

## 📁 Structure du repo

```
claude-agents/
├── button-validator-v2-learning/
│   ├── SKILL.md
│   ├── button_validator_v2.py (800+ lignes)
│   ├── README.md
│   └── brain/ (mémoire, créée automatiquement)
│
├── props-form-validator-v2/
│   ├── SKILL.md
│   └── props_form_validator_v2.py (à venir)
│
├── dead-code-cleaner-v2/
│   ├── SKILL.md
│   └── dead_code_cleaner_v2.py (à venir)
│
├── code-fixer-v2/
│   ├── SKILL.md
│   └── code_fixer_v2.py (à venir)
│
└── README.md (ce fichier)
```

---

## 🔒 Sécurité

### Backup automatique
Tous les agents créent des backups avant modifications :
```
.agent-backup/
└── {timestamp}/
    └── fichiers_modifiés/
```

### Rollback
```bash
python code_fixer_v2.py --rollback {timestamp}
```

### Logs complets
Tous les agents génèrent des logs détaillés :
```
reports/
├── button-analysis-20251031-143022.md
├── props-analysis-20251031-153045.md
├── dead-code-report-20251031-163010.md
└── fixes-applied-20251031-173025.md
```

---

## 📖 Documentation

Chaque agent a sa propre documentation complète :
- **SKILL.md** : Documentation technique de l'agent
- **README.md** : Guide d'utilisation avec exemples
- **Code Python** : Commenté et documenté

---

## 🛠️ Prérequis

- **Python** : 3.7+
- **Projet** : package.json présent
- **Git** : Optionnel (pour commits automatiques)

**Aucune dépendance externe** (bibliothèque standard Python uniquement)

---

## 📈 Roadmap

### ✅ Agents développés et fonctionnels (v2.0.0)
- [x] Button Validator V2 ✅ COMPLET
- [x] Props & Form Validator V2 ✅ COMPLET
- [x] Dead Code Cleaner V2 ✅ COMPLET
- [x] Code Fixer V2 ✅ COMPLET
- [x] Component Consistency Checker V2 ✅ COMPLET
- [x] Agent Coordinator V2 ✅ COMPLET
- [x] README Editor V2 ✅ COMPLET

### Agents planifiés
- [ ] Route Analyzer V2
- [ ] TypeScript Validator V2
- [ ] Test Generator V2
- [ ] JSDoc Generator V2

---

## 🤝 Contribution

Ces agents sont conçus pour s'adapter à **ton projet spécifique**.

Ils apprennent de :
- Tes patterns CSS/Tailwind
- Tes conventions de nommage
- Tes préférences de structure
- Tes décisions de validation

Plus tu les utilises, plus ils deviennent précis et autonomes.

---

## 📝 Notes importantes

### Emojis
**RÈGLE ABSOLUE** : Aucun emoji dans le code UI de l'application.  
Les agents le détectent comme problème **CRITIQUE** et suppriment automatiquement.

### Apprentissage
Les 3-5 premiers scans sont pour l'observation.  
L'autonomie réelle commence après 5+ scans.

### Mémoire
La mémoire est stockée dans `brain/projects/{hash}/`.  
Ne pas supprimer sauf pour reset volontaire.

---

## 📜 Licence

Créé pour analyse et maintenance automatisée de projets web.

---

**Version** : 2.0.0
**Dernière mise à jour** : 2025-11-01
**Agents fonctionnels** : 7/7 ✅
**Agents documentés** : 7/7 ✅
**TOUS LES AGENTS SONT MAINTENANT COMPLETS ET OPÉRATIONNELS !**

---

### 🎨 Component Consistency Checker V2
**Status** : Complet et fonctionnel ✅
**Fonction** : Vérification cohérence visuelle et structurelle entre composants similaires
**Code** : consistency_checker_v2.py (710+ lignes)  

**Ce qu'il fait** :
- Groupe composants similaires (Cards, Forms, Modals, Lists)
- Analyse patterns visuels (couleurs, espacements, typography)
- Détecte incohérences structurelles
- Vérifie conventions de props
- États visuels (hover, focus, disabled, active)
- Accessibilité cohérente entre composants

---

### 🎼 Agent Coordinator V2
**Status** : Complet et fonctionnel ✅
**Fonction** : Chef d'orchestre pour coordonner tous les agents
**Code** : agent_coordinator.py (623 lignes)  

**Ce qu'il fait** :
- Lance tous les agents en parallèle
- Compile les rapports en un rapport maître
- Priorise les corrections intelligemment
- Demande validation utilisateur
- Coordonne l'exécution des corrections
- Vérifie les résultats post-exécution
- Génère rapport final complet

**Workflow** : Analyse → Compilation → Priorisation → Validation → Exécution → Vérification

---

### 📝 README Editor V2
**Status** : Complet et fonctionnel ✅
**Fonction** : Génération et maintenance automatique de documentation
**Code** : readme_editor_v2.py (590+ lignes)  

**Ce qu'il fait** :
- Génère README.md principal du projet
- Crée README.md par dossier (components, hooks, utils)
- Détecte changements (dépendances, composants, features)
- Met à jour automatiquement
- Génère diagrammes d'architecture (Mermaid)
- Documentation des composants individuels
- Sections API, Tests, Scripts auto-générées


