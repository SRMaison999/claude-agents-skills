# Button Validator V2 - Learning Edition 🧠

Agent intelligent d'analyse de boutons avec apprentissage continu pour applications React/Vue/Angular + TypeScript/JavaScript.

## 🎯 Caractéristiques

- ✅ **Auto-détection** du stack (React, Vue, Tailwind, MUI, etc.)
- ✅ **Apprentissage continu** (s'améliore à chaque scan)
- ✅ **Mémoire permanente** (patterns et préférences sauvegardés)
- ✅ **Autonomie équilibrée** (corrections auto si confiance >90%)
- ✅ **Mémoire hybride** (projet + globale)
- ✅ **Universel** (fonctionne sur tout projet web)

## 📦 Installation

```bash
# Cloner le dossier
cd button-validator-v2-learning

# Aucune dépendance externe nécessaire (Python 3.7+)
# L'agent utilise uniquement la bibliothèque standard Python
```

## 🚀 Utilisation

### Commande basique

```bash
python button_validator_v2.py /chemin/vers/votre/projet
```

### Exemple

```bash
# Analyser le projet dans le dossier actuel
python button_validator_v2.py .

# Analyser un projet spécifique
python button_validator_v2.py ~/projects/travel-planner-app
```

### Depuis Claude Code

```
Lance button-validator-v2-learning sur mon projet
```

ou

```
Utilise le skill button-validator-v2-learning pour analyser les boutons
de mon application et me dire quels problèmes tu trouves
```

## 📊 Workflow typique

### Premier scan (Découverte)

```bash
$ python button_validator_v2.py .

======================================================================
🧠 Button Validator V2 - Learning Edition
======================================================================
📁 Projet : travel-planner
🔧 Stack : react + tailwind
🧠 Analyse #1
🌱 État : DÉCOUVERTE (mode apprentissage)
======================================================================

🔍 Démarrage de l'analyse...

📄 47 fichiers à analyser
🔘 52 boutons trouvés

🧠 Analyse en cours...

🧠 Pattern standard appris : bg-blue-600
   Confiance : 73.1%
   Basé sur 38/52 observations

✅ Analyse terminée !
📄 Rapport : reports/button-analysis-20251031-143022.md
💾 Mémoire sauvegardée

📊 Résumé :
   Boutons : 52
   Issues : 8
   - Corrections auto : 0 (mode apprentissage)
   - Recommandations : 0
   - Suggestions : 8
   - Validation requise : 0
```

### Deuxième scan (Validation)

```bash
$ python button_validator_v2.py .

======================================================================
🧠 Button Validator V2 - Learning Edition
======================================================================
📁 Projet : travel-planner
🔧 Stack : react + tailwind
🧠 Analyse #2
🌿 État : CROISSANCE (confiance en construction)
======================================================================

🔍 Démarrage de l'analyse...

📄 50 fichiers à analyser
🔘 58 boutons trouvés (+6 nouveaux)

🧠 Analyse en cours...

✅ Analyse terminée !
📄 Rapport : reports/button-analysis-20251031-153045.md
💾 Mémoire sauvegardée

📊 Résumé :
   Boutons : 58
   Issues : 5
   - Corrections auto : 0
   - Recommandations : 3 (confiance 70-85%)
   - Suggestions : 2
   - Validation requise : 0
```

### Dixième scan (Expert)

```bash
$ python button_validator_v2.py .

======================================================================
🧠 Button Validator V2 - Learning Edition
======================================================================
📁 Projet : travel-planner
🔧 Stack : react + tailwind
🧠 Analyse #10
🎓 État : EXPERT (haute autonomie)
======================================================================

🔍 Démarrage de l'analyse...

📄 52 fichiers à analyser
🔘 64 boutons trouvés

🧠 Analyse en cours...

✅ Analyse terminée !
📄 Rapport : reports/button-analysis-20251110-091522.md
💾 Mémoire sauvegardée

📊 Résumé :
   Boutons : 64
   Issues : 3
   - Corrections auto : 2 (appliquées automatiquement ✅)
   - Recommandations : 1
   - Suggestions : 0
   - Validation requise : 0
```

## 📁 Structure des fichiers générés

```
votre-projet/
├── reports/                          # Rapports d'analyse
│   ├── button-analysis-20251031-143022.md
│   ├── button-analysis-20251031-153045.md
│   └── button-analysis-20251110-091522.md
└── brain/                           # Mémoire de l'agent
    └── projects/
        └── {project-hash}/
            └── memory.json          # Patterns, préférences, historique
```

## 🧠 Exemple de rapport

```markdown
# 🔍 Button Validator V2 - Analyse #5

**Date** : 2025-10-31 15:30:45
**Projet** : travel-planner

---

## 🧠 État de l'apprentissage

**Stack détecté** :
- Framework : react (typescript)
- CSS : tailwind
- UI Libraries : Aucune
- Icônes : lucide
- State : zustand

**Mémoire** :
- Scans effectués : 5
- Patterns appris : 1
- Préférences confirmées : 0
- Confiance moyenne : 85.3%

**Pattern bouton primaire appris** :
- Couleur : `bg-blue-600`
- Hover : `hover:bg-blue-700`
- Confiance : 91.5%
- Observations : 53/58

---

## 📊 Résumé de l'analyse

- 🔘 **Boutons analysés** : 58
- ❌ **Problèmes critiques** : 0
- ⚠️  **Problèmes importants** : 0
- ℹ️  **Améliorations suggérées** : 3

**Corrections autonomes** :
- ✅ Auto-correction (confiance ≥90%) : 2
- ⚠️  Recommandation (70-89%) : 1
- 💬 Suggestion (50-69%) : 0
- ❓ Validation requise (<50% ou critique) : 0

---

## ✅ CORRECTIONS AUTOMATIQUES (confiance ≥90%)

Ces corrections peuvent être appliquées automatiquement :

1. **inconsistent_color** - `src/components/teams/TeamCard.tsx:45`
   - Couleur bg-blue-500 vs standard bg-blue-600 (92% des cas)
   - Solution : Remplacer bg-blue-500 par bg-blue-600
   - Confiance : 92%

2. **missing_hover** - `src/components/stages/StageForm.tsx:120`
   - Hover state manquant (standard : hover:bg-blue-700)
   - Solution : Ajouter hover:bg-blue-700 aux classes
   - Confiance : 91%

---

## ⚠️ RECOMMANDATIONS (confiance 70-89%)

Ces corrections sont fortement recommandées :

1. **missing_transition** - `src/components/personnel/PersonnelModal.tsx:78`
   - Transition manquante pour hover state
   - Solution : Ajouter transition-colors aux classes
   - Confiance : 82%
```

## 🎯 Évolution de l'apprentissage

| Scans | Phase | Capacités | Autonomie |
|-------|-------|-----------|-----------|
| 1-2 | 🌱 Découverte | Observe, mémorise | 0% |
| 3-5 | 🌿 Croissance | Suggère, apprend | 30% |
| 6-10 | 🌳 Maturité | Corrige (>90%) | 60% |
| 10+ | 🎓 Expert | Proactif, optimise | 80%+ |

## 📋 Commandes utiles

### Voir la mémoire du projet

```bash
cat brain/projects/*/memory.json | python -m json.tool
```

### Lister tous les rapports

```bash
ls -lh reports/
```

### Comparer deux rapports

```bash
diff reports/button-analysis-20251031-143022.md \
     reports/button-analysis-20251031-153045.md
```

### Réinitialiser la mémoire (si besoin)

```bash
rm -rf brain/projects/{hash}/
```

## ⚙️ Configuration avancée

### Ajuster le seuil d'autonomie

Modifier dans `button_validator_v2.py` :

```python
# Ligne ~450
if issue.confidence >= 90 and issue.auto_fixable:
    # Changer 90 en 95 pour être plus conservateur
    # ou 85 pour plus d'autonomie
```

### Ajouter des patterns custom

Les patterns sont appris automatiquement, mais vous pouvez les forcer dans la mémoire :

```json
// brain/projects/{hash}/memory.json
{
  "patterns": {
    "primary_button_standard": {
      "background": "bg-indigo-600",
      "hover": "hover:bg-indigo-700",
      "confidence": 100
    }
  }
}
```

## 🔒 Sécurité

### Ce que l'agent PEUT corriger automatiquement

- ✅ Classes CSS/Tailwind (visuelles seulement)
- ✅ Ajout de hover states
- ✅ Ajout de transitions
- ✅ Standardisation de couleurs

### Ce que l'agent NE PEUT PAS corriger auto

- ❌ Logique métier (handlers)
- ❌ Modification de fonctions
- ❌ Restructuration de code
- ❌ Suppression de code

**Toutes les modifications de logique nécessitent validation humaine**

## 🐛 Dépannage

### "Aucun fichier trouvé"

L'agent cherche dans `src/components`, `src/app`, `components`, ou `app`.

Si votre structure est différente :

```python
# Modifier ligne ~250 dans button_validator_v2.py
structure["components_dir"] = "votre/dossier/custom"
```

### "Pattern pas détecté"

Il faut au moins 10 boutons pour apprendre un pattern.

Si vous avez moins de 10 boutons, le pattern ne sera pas appris automatiquement.

### "Confiance trop faible"

Faites plus de scans ! L'agent apprend avec le temps.

Après 5-10 scans, la confiance devrait être >80%.

## 💡 Conseils d'utilisation

1. **Laisser apprendre** : Les 3 premiers scans sont pour l'observation
2. **Scanner régulièrement** : Plus de scans = meilleure précision
3. **Être cohérent** : Gardez vos patterns CSS constants
4. **Vérifier les auto-fixes** : Même avec confiance >90%, vérifier les premiers mois

## 📖 Documentation complète

Voir `SKILL.md` pour la documentation technique complète.

## 🤝 Support

Cet agent est conçu pour s'améliorer avec l'usage. Si vous rencontrez des problèmes :

1. Vérifiez que votre projet a un `package.json`
2. Assurez-vous d'avoir des boutons à analyser
3. Faites au moins 3 scans pour que l'apprentissage commence
4. Consultez les rapports générés pour comprendre ce qui est détecté

## 📜 Licence

Créé pour analyse universelle de boutons avec apprentissage continu.

---

**Version** : 2.0.0  
**Date** : 2025-10-31  
**Python** : 3.7+
