# Button Validator V2 - Learning Edition 🧠

Agent intelligent d'analyse de boutons avec apprentissage continu, auto-détection de frameworks et mémoire hybride.

**Version :** 2.0.0  
**Type :** Universal + Self-Learning  
**Autonomie :** Équilibrée (auto-correction si confiance >90%)  
**Mémoire :** Hybride (projet + globale) - Permanente  

---

## 🎯 Mission

Analyser exhaustivement tous les boutons d'une application web en :
1. **Auto-détectant** le stack technologique (frameworks, librairies, CSS)
2. **Apprenant** continuellement des patterns et préférences du projet
3. **S'améliorant** à chaque analyse (augmentation de la précision)
4. **Corrigeant** automatiquement les problèmes évidents (confiance >90%)
5. **Mémorisant** les décisions pour devenir de plus en plus pertinent

---

## 🧠 Système d'apprentissage

### Niveaux de confiance

| Confiance | Comportement | Exemple |
|-----------|-------------|---------|
| **95-100%** | ✅ Correction automatique sans demander | Pattern utilisé dans 98% des cas, confirmé 10+ fois |
| **90-94%** | ✅ Correction automatique + notification | Pattern majoritaire, confirmé 5+ fois |
| **70-89%** | ⚠️ Proposition forte, demande confirmation rapide | Pattern fréquent mais quelques exceptions |
| **50-69%** | 💬 Suggestion, nécessite validation | Pattern détecté mais incertain |
| **<50%** | ❓ Question, demande clarification | Pas de pattern clair détecté |

### Mémoire hybride

**Mémoire PROJET (spécifique)** :
- Patterns CSS/Tailwind préférés
- Conventions de nommage
- Structure de composants
- Décisions passées (accepté/rejeté)
- Exceptions confirmées

**Mémoire GLOBALE (universelle)** :
- Best practices générales
- Patterns courants par framework
- Anti-patterns universels
- Erreurs communes à éviter

---

## 📋 Processus complet

### Phase 1 : Auto-détection (1ère exécution)

L'agent détecte automatiquement :
- Framework (React, Vue, Angular, Svelte, Next.js)
- Langage (JavaScript, TypeScript)
- UI Libraries (Material-UI, Ant Design, Chakra, Radix, etc.)
- Icon Libraries (Lucide, React Icons, Heroicons, Font Awesome)
- CSS Framework (Tailwind, Styled-Components, Emotion, CSS Modules)
- State Management (Zustand, Redux, MobX, Recoil, Jotai)
- Build Tool (Vite, Webpack, Turbopack)

**Action** : Lit `package.json` et analyse la structure du projet

### Phase 2 : Génération des patterns de détection

Selon le stack détecté, l'agent génère des patterns adaptés :

**Exemple pour React + Tailwind + Lucide + Zustand** :
```
Patterns générés :
- HTML: <button>, <input type="button">
- React: Composants avec onClick
- Lucide: <Trash2 onClick...>, <Plus onClick...>
- Tailwind: Analyse des classes bg-, hover:, transition-
```

### Phase 3 : Scan et extraction

L'agent scanne tous les fichiers `.tsx`, `.jsx`, `.ts`, `.js` et extrait :
- Type de bouton (HTML, composant, icône, élément cliquable)
- Handler (onClick, onPress, onSubmit)
- Classes CSS/Tailwind
- Texte/label
- Props (disabled, type, aria-label)

### Phase 4 : Analyse avec mémoire

**Premier scan (apprentissage)** :
- Observe les patterns
- Stocke dans buffer temporaire
- Après 10+ observations → calcule pattern standard
- **Aucune correction** (confiance = 0%)

**Scans suivants (validation & amélioration)** :
- Compare avec patterns appris
- Détecte incohérences
- Calcule score de confiance
- Applique corrections selon autonomie

### Phase 5 : Corrections graduées

**Confiance >90%** → Correction automatique
```
✅ Correction appliquée automatiquement :
   inconsistent_color dans TeamCard.tsx:45
   bg-blue-500 → bg-blue-600 (confiance 94%)
```

**Confiance 70-89%** → Recommandation forte
```
⚠️  Recommandation (valider SVP) :
   missing_hover dans StageForm.tsx:120
   Ajouter hover:bg-blue-700 (confiance 82%)
   [O]ui / [N]on / [T]oujours / [J]amais ?
```

**Confiance <70%** → Suggestion simple
```
💬 Suggestion :
   Uniformiser le padding (confiance 65%)
```

### Phase 6 : Apprentissage continu

**Apprend de tes décisions** :
- ✅ Accepté → Confiance +10%
- ❌ Rejeté → Confiance -10%
- 💬 "Toujours" → Confiance = 100%, préférence enregistrée
- 🚫 "Jamais" → Confiance = 0%, exception enregistrée

**Détecte le drift** :
```
🔔 Alerte : Nouveau pattern détecté !
   8 nouveaux boutons avec bg-indigo-600
   Au lieu de bg-blue-600 (standard actuel)
   
   Changement de couleur primaire ?
   [Oui, mettre à jour] [Non, exception locale]
```

---

## 💻 Code complet de l'agent

Voir le fichier `button_validator_v2.py` (~1000 lignes) qui inclut :

**Classes principales** :
- `ButtonValidatorLearning` : Agent principal
- `ButtonInfo` : Données d'un bouton
- `ButtonIssue` : Problème détecté

**Méthodes clés** :
- `detect_project_stack()` : Auto-détection
- `load_project_memory()` : Chargement mémoire
- `analyze_button_with_memory()` : Analyse intelligente
- `learn_from_analysis()` : Apprentissage
- `apply_auto_fixes()` : Corrections autonomes
- `generate_learning_report()` : Rapport évolutif

---

## 🚀 Utilisation

### Commande directe
```bash
python button_validator_v2.py /chemin/vers/projet
```

### Depuis Claude Code
```
Lance button-validator-v2-learning sur mon projet
```

### Workflow typique

**Scan #1** (Découverte)
```
🆕 Première analyse - Mode apprentissage
📄 47 boutons trouvés
🧠 Pattern appris : bg-blue-600 (confiance 70%)
📊 0 corrections (phase d'observation)
```

**Scan #2** (Validation)
```
📚 Mémoire chargée - 1 scan précédent
🔘 52 boutons (+5 nouveaux)
🧠 Pattern confirmé : bg-blue-600 (confiance 85%)
⚠️  3 recommandations de correction
```

**Scan #5** (Maturité)
```
🎓 Analyse #5 - Agent mature
✅ 2 corrections automatiques appliquées
⚠️  1 recommandation (validation nécessaire)
🧠 Confiance moyenne : 92%
📈 Évolution : -5 issues critiques depuis scan #1
```

**Scan #10+** (Expert)
```
🏆 Agent expert - Haute autonomie
✅ 8 corrections auto (confiance >90%)
💡 Suggestion : Créer composant Button réutilisable
📊 80% d'autonomie atteinte
```

---

## 📊 Structure de la mémoire

```
brain/
└── projects/
    └── {project-hash}/
        └── memory.json
            {
              "project_path": "/path/to/project",
              "scan_count": 5,
              "patterns": {
                "primary_button_standard": {
                  "background": "bg-blue-600",
                  "hover": "hover:bg-blue-700",
                  "confidence": 94.0,
                  "occurrences": 47
                },
                "custom_button_components": ["Button", "ActionButton"]
              },
              "preferences": {
                "use_transitions": false,
                "color_exceptions": ["bg-red-600"]
              },
              "corrections_history": [
                {
                  "timestamp": "2025-10-31T14:30:00",
                  "issue_type": "inconsistent_color",
                  "decision": "accept"
                }
              ],
              "confidence_scores": {
                "inconsistent_color_fix": 95,
                "missing_hover_fix": 85
              }
            }
```

---

## 🎯 Évolution de l'agent

| Phase | Scans | Capacités | Autonomie |
|-------|-------|-----------|-----------|
| 🌱 **Découverte** | 1-2 | Observe, mémorise | 0% |
| 🌿 **Croissance** | 3-5 | Suggère, apprend | 30% |
| 🌳 **Maturité** | 6-10 | Corrige (confiance >90%) | 60% |
| 🎓 **Expert** | 10+ | Proactif, optimise | 80%+ |

---

## 💡 Fonctionnalités avancées

### Détection de drift
Alerte quand les patterns changent significativement

### Suggestions proactives
Après 5+ scans avec patterns stables :
- Créer composants réutilisables
- Mettre en place design system
- Optimisations architecturales

### Rapport évolutif
Compare automatiquement avec analyses précédentes :
```
📈 Évolution depuis dernière analyse
   Boutons : +5
   Critiques : -3 ✅
   Importants : -2 ✅
   Mineurs : +1
```

### Gestion des exceptions
Mémorise tes choix spécifiques :
```
Exception apprise :
- Boutons de danger gardent bg-red-600 (pas standardisation)
- Pas de transitions sur ce projet (préférence utilisateur)
```

---

## 🔒 Limites et sécurité

### Corrections automatiques AUTORISÉES
- ✅ Classes CSS/Tailwind (visuelles)
- ✅ Ajout hover/transition
- ✅ Standardisation couleurs

### Corrections INTERDITES (toujours validation)
- ❌ Logique métier (handlers)
- ❌ Modification fonctions
- ❌ Restructuration code
- ❌ Suppression code

---

## 📋 Commandes de gestion

### Voir la mémoire du projet
```bash
cat brain/projects/*/memory.json | jq
```

### Statistiques d'apprentissage
```bash
python stats.py
```

### Reset mémoire (si nécessaire)
```bash
rm -rf brain/projects/{hash}/
```

---

## 🎓 Conseils d'utilisation

1. **Laisser apprendre** : Les 3 premiers scans sont pour l'observation
2. **Être cohérent** : Répondre systématiquement aux questions de validation
3. **Utiliser "Toujours/Jamais"** : Accélère l'apprentissage
4. **Scanner régulièrement** : Plus de scans = meilleure précision
5. **Vérifier les auto-fixes** : Même avec confiance >90%, vérifier le premier mois

---

## 📈 Métriques de succès

**Objectifs après 10 scans** :
- ✅ Autonomie >80%
- ✅ Confiance moyenne >90%
- ✅ 0% faux positifs
- ✅ Temps d'analyse <2 min
- ✅ Détection drift fonctionnelle

---

**Créé pour :** Analyse universelle de boutons avec apprentissage continu  
**Version :** 2.0.0  
**Date :** 2025-10-31
