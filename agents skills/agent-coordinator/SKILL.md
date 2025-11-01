# Agent Coordinator V2 - Orchestration Edition

Chef d'orchestre intelligent pour gérer et coordonner tous les agents d'analyse et de correction.

**Version** : 2.0.0  
**Type** : Orchestrator + Decision Maker  
**Autonomie** : Supervisée (valide avant exécution)  
**Mémoire** : Globale (coordonne toutes les mémoires agents)  

---

## 🎯 Mission

Orchestrer l'exécution de tous les agents pour un workflow optimal :
1. **Planifier** l'ordre d'exécution des agents
2. **Lancer** les agents analyseurs en parallèle
3. **Compiler** tous les rapports
4. **Prioriser** les corrections à appliquer
5. **Coordonner** l'application des corrections
6. **Valider** les résultats finaux

---

## 🎼 Workflow orchestré

### Phase 1 : Analyse initiale (parallèle)

**Agents lancés simultanément :**

```python
async def run_analysis_phase(self, project_path: str):
    """Lance tous les agents analyseurs en parallèle"""
    
    agents_to_run = [
        "button-validator-v2",
        "props-form-validator-v2",
        "component-consistency-checker-v2",
        "dead-code-cleaner-v2"
    ]
    
    # Lancer en parallèle
    tasks = [
        run_agent_async(agent, project_path)
        for agent in agents_to_run
    ]
    
    # Attendre que tous terminent
    results = await asyncio.gather(*tasks)
    
    return results
```

**Temps estimé** : 2-5 minutes (selon taille projet)

**Output** :
- `button-analysis-{timestamp}.md`
- `props-form-analysis-{timestamp}.md`
- `consistency-report-{timestamp}.md`
- `dead-code-report-{timestamp}.md`

---

### Phase 2 : Compilation des rapports

**Fusionner tous les rapports en un seul :**

```python
def compile_reports(self, reports: List[AgentReport]) -> MasterReport:
    """Compile tous les rapports en un rapport maître"""
    
    master_report = MasterReport()
    
    # Collecter toutes les issues
    all_issues = []
    for report in reports:
        all_issues.extend(report.issues)
    
    # Grouper par fichier
    issues_by_file = defaultdict(list)
    for issue in all_issues:
        issues_by_file[issue.file_path].append(issue)
    
    # Grouper par sévérité
    critical = [i for i in all_issues if i.severity == "critical"]
    important = [i for i in all_issues if i.severity == "important"]
    minor = [i for i in all_issues if i.severity == "minor"]
    
    master_report.issues_by_file = issues_by_file
    master_report.critical_count = len(critical)
    master_report.important_count = len(important)
    master_report.minor_count = len(minor)
    master_report.total_issues = len(all_issues)
    
    return master_report
```

**Rapport maître généré :**

```markdown
# Master Analysis Report - Coordination #X

**Date** : 2025-10-31 15:30:45
**Projet** : travel-planner
**Agents exécutés** : 4
**Fichiers analysés** : 52
**Issues totales** : 47

---

## 📊 Vue d'ensemble par sévérité

- ❌ **CRITIQUES** : 8
  - Emojis : 5
  - Props manquantes : 2
  - Boutons sans handler : 1

- ⚠️ **IMPORTANTES** : 15
  - Labels manquants : 4
  - Hover states manquants : 6
  - Focus states manquants : 3
  - Structure incohérente : 2

- ℹ️ **MINEURES** : 24
  - Code mort : 12
  - Incohérences visuelles : 8
  - Props inutilisées : 4

---

## 📁 Issues par fichier (Top 5)

### 1. TeamCard.tsx (8 issues)
- ❌ Emoji dans bouton (ligne 45)
- ⚠️ Hover state manquant (ligne 67)
- ℹ️ Import inutilisé (ligne 2)
- ℹ️ Console.log oublié (ligne 89)
- ℹ️ Props inutilisée (isHighlighted)

### 2. StageForm.tsx (6 issues)
- ❌ Prop manquante (onSubmit)
- ⚠️ Labels manquants (2 champs)
- ℹ️ Border incohérente
- ℹ️ Padding incohérent

### 3. ParticipantModal.tsx (5 issues)
...

---

## 🎯 Corrections possibles en automatique

**Total corrections auto** : 32 (68% des issues)
- Confiance >95% : 24 corrections
- Confiance 90-95% : 8 corrections

**Détails** :
- Suppression emojis : 5 (100%)
- Nettoyage imports : 12 (100%)
- Console.log : 4 (100%)
- Uniformisation CSS : 8 (90-95%)
- Ajout hover states : 3 (90%)
```

---

### Phase 3 : Priorisation intelligente

**L'agent décide de l'ordre optimal :**

```python
def prioritize_issues(self, all_issues: List[Issue]) -> PrioritizedPlan:
    """Priorise les corrections selon impact et risque"""
    
    plan = PrioritizedPlan()
    
    # Règle 1 : Critiques d'abord
    critical = [i for i in all_issues if i.severity == "critical"]
    
    # Règle 2 : Parmi critiques, auto-fixable d'abord
    critical_auto = [i for i in critical if i.auto_fixable and i.confidence >= 90]
    critical_manual = [i for i in critical if not i.auto_fixable or i.confidence < 90]
    
    # Règle 3 : Emojis en priorité absolue (impact UX)
    emoji_issues = [i for i in critical_auto if i.issue_type == "emoji"]
    
    # Règle 4 : Props manquantes nécessitent validation
    missing_props = [i for i in critical_manual if i.issue_type == "missing_prop"]
    
    # Construire le plan
    plan.add_phase("Phase 1 : Suppressions emojis (AUTO)", emoji_issues)
    plan.add_phase("Phase 2 : Nettoyage code mort (AUTO)", dead_code_auto)
    plan.add_phase("Phase 3 : Uniformisation styles (AUTO >90%)", style_auto)
    plan.add_phase("Phase 4 : Props manquantes (VALIDATION)", missing_props)
    plan.add_phase("Phase 5 : Améliorations mineures (OPTIONNEL)", minor_issues)
    
    return plan
```

**Plan d'exécution généré :**

```markdown
# Plan d'exécution recommandé

## Phase 1 : Critiques auto (2 min)
✅ Peut être exécuté automatiquement

**Actions** :
1. Supprimer 5 emojis (confiance 100%)
2. Nettoyer 12 imports inutilisés (confiance 100%)
3. Supprimer 4 console.log (confiance 100%)

**Impact** : 21 corrections / 0 risque
**Commande** : `code-fixer --phase 1 --auto`

---

## Phase 2 : Uniformisation CSS (1 min)
✅ Peut être exécuté automatiquement

**Actions** :
1. Uniformiser 8 couleurs de borders
2. Ajouter 3 hover states manquants
3. Corriger 4 espacements

**Impact** : 15 corrections / risque minime
**Confiance moyenne** : 92%
**Commande** : `code-fixer --phase 2 --auto`

---

## Phase 3 : Props manquantes (VALIDATION REQUISE)
⚠️ Nécessite intervention humaine

**Actions** :
1. TeamCard - Ajouter prop onDelete
   Valeur suggérée : handleDeleteTeam
   Validation requise : Confirmer le handler correct
   
2. StageForm - Ajouter prop onSubmit
   Valeur suggérée : handleSubmitStage
   Validation requise : Confirmer le handler correct

**Impact** : 2 corrections critiques
**Commande** : Review manuel puis `code-fixer --phase 3`

---

## Phase 4 : Améliorations mineures (OPTIONNEL)
💡 Peut attendre / Faible priorité

**Actions** :
- Supprimer 4 props inutilisées
- Renommer 3 handlers pour cohérence
- Restructurer 1 composant

**Impact** : Amélioration qualité code
**Commande** : `code-fixer --phase 4` (après validation)

---

## Résumé

✅ **Auto** : 36 corrections (77%)
⚠️ **Validation** : 2 corrections (4%)
💡 **Optionnel** : 9 améliorations (19%)

**Temps estimé total** : 5-10 minutes
```

---

### Phase 4 : Demande de validation

**L'agent présente le plan et demande confirmation :**

```python
def request_user_validation(self, plan: PrioritizedPlan):
    """Demande validation utilisateur avant exécution"""
    
    print("\n" + "="*70)
    print("🎼 AGENT COORDINATOR - Plan d'exécution")
    print("="*70)
    
    print(f"\n📊 Analyse terminée : {plan.total_issues} issues détectées\n")
    
    # Afficher résumé
    print("✅ Corrections automatiques disponibles : {plan.auto_count}")
    print(f"   - Emojis : {plan.emoji_count}")
    print(f"   - Code mort : {plan.dead_code_count}")
    print(f"   - Styles : {plan.style_count}")
    print(f"   Confiance moyenne : {plan.avg_confidence:.1f}%")
    
    print(f"\n⚠️  Validations requises : {plan.manual_count}")
    print(f"   - Props manquantes : {plan.missing_props_count}")
    print(f"   - Restructurations : {plan.refactor_count}")
    
    print(f"\n💡 Améliorations optionnelles : {plan.optional_count}")
    
    print("\n" + "-"*70)
    print("OPTIONS :")
    print("  [1] Exécuter TOUT automatiquement (phases 1-2)")
    print("  [2] Exécuter phase par phase (avec confirmation)")
    print("  [3] Voir le rapport détaillé complet")
    print("  [4] Exécuter uniquement les emojis")
    print("  [5] Annuler")
    print("-"*70)
    
    choice = input("\nVotre choix : ")
    
    return choice
```

---

### Phase 5 : Exécution coordonnée

**Selon le choix utilisateur :**

```python
async def execute_plan(self, plan: PrioritizedPlan, mode: str):
    """Exécute le plan selon le mode choisi"""
    
    if mode == "full_auto":
        # Exécuter phases 1-2 automatiquement
        await execute_phase(plan.phase_1)  # Emojis, imports, console
        await execute_phase(plan.phase_2)  # Styles CSS
        
        print("\n✅ Phases automatiques terminées")
        print("⚠️  Phase 3 nécessite votre validation")
        
    elif mode == "step_by_step":
        # Demander confirmation pour chaque phase
        for phase in plan.phases:
            print(f"\n📋 Phase : {phase.name}")
            print(f"   Corrections : {len(phase.issues)}")
            print(f"   Confiance : {phase.avg_confidence:.1f}%")
            
            confirm = input("   Exécuter ? [O/n] : ")
            
            if confirm.lower() in ['o', 'oui', 'y', 'yes', '']:
                await execute_phase(phase)
                print(f"   ✅ Phase terminée")
            else:
                print(f"   ⏭️  Phase ignorée")
    
    elif mode == "emoji_only":
        # Juste les emojis
        emoji_phase = plan.get_phase_by_type("emoji")
        await execute_phase(emoji_phase)
```

---

### Phase 6 : Vérification post-exécution

**Après corrections, relancer les agents pour valider :**

```python
async def verify_corrections(self, project_path: str, original_report: MasterReport):
    """Vérifie que les corrections ont été correctement appliquées"""
    
    print("\n🔍 Vérification des corrections...")
    
    # Relancer les agents
    new_results = await self.run_analysis_phase(project_path)
    new_report = self.compile_reports(new_results)
    
    # Comparer avec rapport original
    comparison = compare_reports(original_report, new_report)
    
    print(f"\n📊 Résultats de la vérification :")
    print(f"   Issues résolues : {comparison.resolved_count}")
    print(f"   Issues restantes : {comparison.remaining_count}")
    print(f"   Nouvelles issues : {comparison.new_count}")
    
    if comparison.new_count > 0:
        print(f"\n⚠️  ATTENTION : {comparison.new_count} nouvelles issues détectées")
        print(f"   Vérification recommandée")
    
    if comparison.remaining_count == 0:
        print(f"\n🎉 Succès ! Toutes les issues ont été résolues")
    
    return comparison
```

---

### Phase 7 : Rapport final

```markdown
# Coordination Report - Final

## 🎯 Objectif initial
- Issues détectées : 47
- Corrections planifiées : 47

## ✅ Exécution
- Phase 1 (Emojis) : ✅ Terminée - 5/5 corrections
- Phase 2 (Code mort) : ✅ Terminée - 12/12 corrections
- Phase 3 (Styles) : ✅ Terminée - 8/8 corrections
- Phase 4 (Props) : ⚠️ Validation manuelle - 2/2 corrections
- Phase 5 (Optionnel) : ⏭️ Ignorée

## 📊 Résultats
- ✅ Issues résolues : 27 (57%)
- ⏳ En attente validation : 2 (4%)
- ⏭️ Reportées : 18 (38%)

## 🔍 Vérification post-exécution
- Nouvelle analyse lancée : ✅
- Issues résolues confirmées : 27
- Nouvelles issues : 0
- Issues restantes : 20

## 📈 Amélioration
- Avant : 47 issues
- Après : 20 issues
- **Réduction : 57%**

## ⏱️ Temps total
- Analyse initiale : 3 min 24s
- Compilation rapports : 12s
- Exécution corrections : 1 min 45s
- Vérification finale : 2 min 50s
- **Total : 8 min 11s**

## 💡 Recommandations
1. Valider les 2 props manquantes (Phase 4)
2. Relancer coordination après validation
3. Considérer les 18 améliorations optionnelles
```

---

## 🤖 Intelligence de coordination

### Détection de conflits

**L'agent détecte les corrections qui peuvent entrer en conflit :**

```python
def detect_conflicts(self, issues: List[Issue]) -> List[Conflict]:
    """Détecte les conflits potentiels entre corrections"""
    
    conflicts = []
    
    # Même fichier, même ligne
    issues_by_location = defaultdict(list)
    for issue in issues:
        key = f"{issue.file_path}:{issue.line_number}"
        issues_by_location[key].append(issue)
    
    # Chercher conflits
    for location, location_issues in issues_by_location.items():
        if len(location_issues) > 1:
            conflicts.append(Conflict(
                location=location,
                issues=location_issues,
                resolution_strategy="apply_in_order"
            ))
    
    return conflicts
```

### Optimisation de l'ordre

**Optimise l'ordre pour minimiser les effets de bord :**

1. **Suppressions avant ajouts**
2. **Modifications simples avant restructurations**
3. **Changements visuels avant changements structurels**

---

## 🚀 Utilisation

### Mode complet (recommandé)

```bash
python agent_coordinator_v2.py /chemin/vers/projet --full
```

**Fait tout** : Analyse + Compilation + Exécution + Vérification

### Mode analyse seulement

```bash
python agent_coordinator_v2.py /chemin/vers/projet --analyze-only
```

**Génère le plan sans exécuter**

### Mode custom

```bash
python agent_coordinator_v2.py /chemin/vers/projet \
  --agents button,props,consistency \
  --auto-execute \
  --skip-verification
```

**Depuis Claude Code :**
```
Lance agent-coordinator-v2 en mode complet sur mon projet
```

---

## 📋 Configuration

**Fichier `coordinator-config.json` :**

```json
{
  "agents": {
    "button-validator": {
      "enabled": true,
      "timeout": 300,
      "priority": 1
    },
    "props-form-validator": {
      "enabled": true,
      "timeout": 300,
      "priority": 1
    },
    "component-consistency-checker": {
      "enabled": true,
      "timeout": 600,
      "priority": 2
    },
    "dead-code-cleaner": {
      "enabled": true,
      "timeout": 300,
      "priority": 1
    }
  },
  "execution": {
    "parallel_analysis": true,
    "auto_fix_threshold": 90,
    "backup_before_fixes": true,
    "run_verification": true
  },
  "notification": {
    "on_completion": true,
    "on_error": true,
    "slack_webhook": null
  }
}
```

---

**Version** : 2.0.0  
**Créé pour** : Orchestration intelligente de tous les agents
