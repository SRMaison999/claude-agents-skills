# Component Consistency Checker V2 - Learning Edition

Agent intelligent de vérification de la cohérence visuelle et structurelle des composants.

**Version** : 2.0.0  
**Type** : Universal + Self-Learning  
**Autonomie** : Équilibrée (auto-correction si confiance >90%)  
**Mémoire** : Hybride (projet + globale) - Permanente  

---

## 🎯 Mission

Assurer la cohérence absolue entre composants similaires :
1. **Cohérence visuelle** (Tailwind, couleurs, espacements)
2. **Structure des composants** (patterns, organisation)
3. **Props et interfaces** (conventions de nommage)
4. **Styles des états** (hover, focus, disabled, loading)
5. **Accessibilité** (ARIA, labels, navigation clavier)

---

## 🎨 Détection des incohérences visuelles

### Étape 1 : Grouper les composants similaires

**Critères de similarité :**
- Nom similaire (TeamCard, ParticipantCard, StageCard)
- Fonction similaire (tous des "cards")
- Structure similaire (même éléments JSX)
- Contexte d'usage similaire

**Groupes détectés automatiquement :**
```
Groupe 1 : Cards
- TeamCard.tsx
- ParticipantCard.tsx  
- StageCard.tsx
- PersonnelCard.tsx

Groupe 2 : Forms
- TeamForm.tsx
- ParticipantForm.tsx
- StageForm.tsx

Groupe 3 : Modals
- ImportModal.tsx
- ExportModal.tsx
- DeleteConfirmModal.tsx

Groupe 4 : Lists
- TeamList.tsx
- ParticipantList.tsx
- StageList.tsx
```

### Étape 2 : Analyser les patterns visuels

**Pour chaque groupe, extraire :**

```python
def extract_visual_patterns(component_group: List[Component]):
    """Extrait les patterns visuels d'un groupe de composants"""
    
    patterns = {
        "colors": {},           # Couleurs utilisées
        "spacing": {},          # Espacements (padding, margin)
        "typography": {},       # Tailles de police, poids
        "borders": {},          # Border radius, width
        "shadows": {},          # Box shadows
        "transitions": {},      # Transitions CSS
        "layout": {},           # Flex, grid
        "states": {             # États interactifs
            "hover": {},
            "focus": {},
            "disabled": {},
            "active": {}
        }
    }
    
    for component in component_group:
        # Extraire toutes les classes Tailwind
        tailwind_classes = extract_tailwind_classes(component)
        
        # Catégoriser par type
        for cls in tailwind_classes:
            if cls.startswith('bg-'):
                patterns["colors"][cls] = patterns["colors"].get(cls, 0) + 1
            elif cls.startswith(('p-', 'px-', 'py-', 'm-', 'mx-', 'my-')):
                patterns["spacing"][cls] = patterns["spacing"].get(cls, 0) + 1
            elif cls.startswith(('text-', 'font-')):
                patterns["typography"][cls] = patterns["typography"].get(cls, 0) + 1
            elif cls.startswith(('rounded', 'border')):
                patterns["borders"][cls] = patterns["borders"].get(cls, 0) + 1
            elif cls.startswith('shadow'):
                patterns["shadows"][cls] = patterns["shadows"].get(cls, 0) + 1
            elif cls.startswith('transition'):
                patterns["transitions"][cls] = patterns["transitions"].get(cls, 0) + 1
            elif cls.startswith('hover:'):
                state = cls.replace('hover:', '')
                patterns["states"]["hover"][state] = patterns["states"]["hover"].get(state, 0) + 1
    
    return patterns
```

### Étape 3 : Calculer le pattern standard

**Pattern majoritaire = standard du groupe**

```python
def calculate_standard_pattern(patterns: dict) -> dict:
    """Calcule le pattern standard à partir des observations"""
    
    standard = {}
    
    for category, values in patterns.items():
        if isinstance(values, dict) and values:
            # Trouver la valeur la plus utilisée
            most_common = max(values.items(), key=lambda x: x[1])
            
            standard[category] = {
                "value": most_common[0],
                "occurrences": most_common[1],
                "total": sum(values.values()),
                "confidence": (most_common[1] / sum(values.values())) * 100
            }
    
    return standard
```

### Étape 4 : Détecter les déviations

**Exemples d'incohérences détectées :**

**Incohérence 1 : Couleurs différentes**
```tsx
// TeamCard.tsx
<div className="bg-white border border-gray-200 rounded-lg p-4">

// ParticipantCard.tsx  
<div className="bg-white border border-gray-300 rounded-lg p-4">
//                              ^^^^^^^^^ DIFFÉRENT

// StageCard.tsx
<div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
//       ^^^^^^^^^ DIFFÉRENT
```

**Rapport :**
```
⚠️ INCOHÉRENCE VISUELLE - Cards
Standard détecté : bg-white border-gray-200 (80% des cas)

Déviations :
1. ParticipantCard.tsx:12
   - Utilise : border-gray-300
   - Standard : border-gray-200
   - Confiance standard : 80%
   - Correction auto : OUI

2. StageCard.tsx:8
   - Utilise : bg-gray-50
   - Standard : bg-white
   - Confiance standard : 80%
   - Correction auto : OUI
```

**Incohérence 2 : Espacements différents**
```tsx
// TeamCard.tsx
<div className="p-4">
  <h3 className="mb-2">

// ParticipantCard.tsx
<div className="p-6">
//       ^^^ DIFFÉRENT
  <h3 className="mb-4">
//          ^^^ DIFFÉRENT
```

**Incohérence 3 : States manquants**
```tsx
// TeamCard.tsx
<button className="bg-blue-600 hover:bg-blue-700 transition-colors">
//                              ^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^ OK

// ParticipantCard.tsx
<button className="bg-blue-600">
//                              ^^ MANQUE hover et transition
```

---

## 📐 Vérification de la structure

### Étape 1 : Analyser la structure JSX

**Pour chaque groupe, identifier la structure commune :**

```python
def analyze_jsx_structure(component: Component) -> ComponentStructure:
    """Analyse la structure JSX d'un composant"""
    
    structure = {
        "root_element": None,        # div, section, article
        "has_header": False,
        "has_body": False,
        "has_footer": False,
        "has_image": False,
        "has_icon": False,
        "button_count": 0,
        "input_count": 0,
        "hierarchy": []              # Ordre des éléments
    }
    
    # Parser le JSX
    jsx_tree = parse_jsx(component.content)
    
    # Extraire structure
    structure["root_element"] = jsx_tree.root.tag
    
    # Chercher sections communes
    for node in jsx_tree.descendants:
        if is_header_element(node):
            structure["has_header"] = True
        elif is_body_element(node):
            structure["has_body"] = True
        elif is_footer_element(node):
            structure["has_footer"] = True
        elif node.tag in ['img', 'Image']:
            structure["has_image"] = True
        elif is_icon_component(node):
            structure["has_icon"] = True
        elif node.tag == 'button':
            structure["button_count"] += 1
        elif node.tag == 'input':
            structure["input_count"] += 1
    
    # Construire hiérarchie
    structure["hierarchy"] = [child.tag for child in jsx_tree.root.children]
    
    return structure
```

### Étape 2 : Comparer les structures

**Structure standard d'une Card :**
```
Standard détecté (85% des Cards) :
- Root : <div>
- Hiérarchie : [header, body, footer]
- Header : Image/Icon + Titre
- Body : Description + Metadata
- Footer : Boutons d'action (2 boutons)
```

**Déviations détectées :**
```
⚠️ STRUCTURE INCOHÉRENTE - StageCard

Standard attendu :
  <div>
    <header>
      <Icon />
      <h3>Titre</h3>
    </header>
    <body>
      <p>Description</p>
      <div>Metadata</div>
    </body>
    <footer>
      <button>Action 1</button>
      <button>Action 2</button>
    </footer>
  </div>

Trouvé dans StageCard :
  <div>
    <h3>Titre</h3>        ← Manque header wrapper
    <p>Description</p>
    <button>Action</button>  ← Manque footer wrapper
  </div>

Problèmes :
- Pas de header structuré
- Pas de footer structuré
- Un seul bouton au lieu de 2

Recommandation : Restructurer pour correspondre au standard
Correction auto : NON (restructuration manuelle nécessaire)
```

---

## 🏷️ Vérification des Props

### Étape 1 : Analyser les interfaces similaires

**Pour les composants d'un même groupe :**

```python
def compare_prop_interfaces(component_group: List[Component]):
    """Compare les interfaces de props entre composants similaires"""
    
    interfaces = {}
    
    for component in component_group:
        interface = extract_props_interface(component)
        interfaces[component.name] = interface
    
    # Identifier les props communes
    common_props = find_common_props(interfaces)
    
    # Identifier les variations
    variations = find_prop_variations(interfaces, common_props)
    
    return {
        "common": common_props,
        "variations": variations
    }
```

**Exemple de comparaison :**

```tsx
// TeamCard.tsx
interface TeamCardProps {
  team: Team;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  isSelected?: boolean;
}

// ParticipantCard.tsx
interface ParticipantCardProps {
  participant: Participant;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  isActive?: boolean;        // ← DIFFÉRENT (isSelected vs isActive)
}

// StageCard.tsx
interface StageCardProps {
  stage: Stage;
  handleEdit: (id: string) => void;    // ← DIFFÉRENT (onEdit vs handleEdit)
  handleDelete: (id: string) => void;  // ← DIFFÉRENT
  // Manque état boolean
}
```

**Rapport d'incohérence :**
```
⚠️ CONVENTIONS DE PROPS INCOHÉRENTES - Cards

Standard détecté :
- Objet principal : {type}
- Actions : onEdit, onDelete
- État optionnel : isSelected

Déviations :

1. ParticipantCard - Convention différente
   Utilise : isActive
   Standard : isSelected
   Recommandation : Renommer pour cohérence
   
2. StageCard - Multiples problèmes
   - Utilise : handleEdit au lieu de onEdit
   - Utilise : handleDelete au lieu de onDelete
   - Manque : prop d'état (isSelected/isActive)
   Recommandation : Aligner sur le standard du groupe
```

---

## ♿ Vérification de l'accessibilité

### Étape 1 : Vérifier les éléments interactifs

```python
def check_accessibility_consistency(component_group: List[Component]):
    """Vérifie la cohérence de l'accessibilité entre composants"""
    
    issues = []
    
    for component in component_group:
        # Boutons
        buttons = find_buttons(component)
        for button in buttons:
            if not has_accessible_name(button):
                issues.append(AccessibilityIssue(
                    component=component.name,
                    element="button",
                    issue="missing_accessible_name",
                    severity="important"
                ))
        
        # Images
        images = find_images(component)
        for image in images:
            if not has_alt_text(image):
                issues.append(AccessibilityIssue(
                    component=component.name,
                    element="img",
                    issue="missing_alt_text",
                    severity="critical"
                ))
        
        # Navigation clavier
        if not supports_keyboard_navigation(component):
            issues.append(AccessibilityIssue(
                component=component.name,
                issue="keyboard_navigation_missing",
                severity="important"
            ))
    
    return issues
```

---

## 🎭 Vérification des états visuels

### États à vérifier pour chaque composant interactif

**1. Hover**
```python
def check_hover_consistency(component_group: List[Component]):
    """Vérifie que tous les composants ont des hover states cohérents"""
    
    hover_patterns = {}
    
    for component in component_group:
        hover_classes = extract_hover_classes(component)
        hover_patterns[component.name] = hover_classes
    
    # Calculer le pattern standard
    standard_hover = calculate_most_common(hover_patterns)
    
    # Détecter déviations
    for component_name, hover_classes in hover_patterns.items():
        if hover_classes != standard_hover:
            issues.append(HoverInconsistency(
                component=component_name,
                current=hover_classes,
                expected=standard_hover
            ))
```

**2. Focus**
```python
def check_focus_states(component_group: List[Component]):
    """Vérifie que tous les composants ont des focus states"""
    
    for component in component_group:
        interactive_elements = find_interactive_elements(component)
        
        for element in interactive_elements:
            if not has_focus_styles(element):
                issues.append(FocusIssue(
                    component=component.name,
                    element=element,
                    severity="important",
                    description="Focus state manquant (accessibilité)"
                ))
```

**3. Disabled**
```python
def check_disabled_states(component_group: List[Component]):
    """Vérifie cohérence des états disabled"""
    
    disabled_patterns = {}
    
    for component in component_group:
        buttons = find_buttons(component)
        for button in buttons:
            if supports_disabled_state(button):
                disabled_styles = extract_disabled_styles(button)
                disabled_patterns[component.name] = disabled_styles
    
    # Standard : disabled:opacity-50 disabled:cursor-not-allowed
    standard_disabled = calculate_standard_disabled(disabled_patterns)
    
    # Vérifier cohérence
    for component_name, disabled_styles in disabled_patterns.items():
        if disabled_styles != standard_disabled:
            issues.append(DisabledInconsistency(
                component=component_name,
                current=disabled_styles,
                expected=standard_disabled
            ))
```

---

## 📊 Rapport de cohérence

### Structure du rapport

```markdown
# Component Consistency Checker Report - Analyse #X

## 📊 Vue d'ensemble

**Groupes analysés** : 4
**Composants analysés** : 15
**Incohérences détectées** : 23
- CRITIQUES : 3
- IMPORTANTES : 8
- MINEURES : 12

---

## 🎨 GROUPE 1 : Cards (4 composants)

**Standard détecté** (basé sur 80% des composants) :
- Background : bg-white
- Border : border border-gray-200
- Padding : p-4
- Rounded : rounded-lg
- Shadow : shadow-sm
- Hover : hover:shadow-md transition-shadow

### ⚠️ Incohérences visuelles

**1. ParticipantCard - Border incorrecte**
- Ligne : 12
- Utilise : border-gray-300
- Standard : border-gray-200
- Confiance : 80%
- Correction auto : OUI

**2. StageCard - Background différente**
- Ligne : 8
- Utilise : bg-gray-50
- Standard : bg-white
- Confiance : 80%
- Correction auto : OUI

### 🏗️ Incohérences structurelles

**1. StageCard - Structure non standard**
- Manque : Header wrapper structuré
- Manque : Footer wrapper structuré
- Correction auto : NON (restructuration requise)

### 🏷️ Incohérences de props

**1. StageCard - Nommage incohérent**
- Utilise : handleEdit, handleDelete
- Standard : onEdit, onDelete
- Recommandation : Renommer pour cohérence groupe

---

## 📝 GROUPE 2 : Forms (3 composants)

**Standard détecté** :
- Labels : Obligatoires pour tous les champs
- Validation : Messages d'erreur sous les champs
- Submit button : bg-blue-600 text-white px-4 py-2

### ⚠️ Incohérences

**1. ParticipantForm - Labels manquants**
- 2 champs sur 5 sans label
- Impact : Accessibilité compromise
- Correction auto : NON (texte de label nécessaire)

**2. StageForm - Bouton submit incohérent**
- Utilise : bg-blue-500 px-3 py-1
- Standard : bg-blue-600 px-4 py-2
- Correction auto : OUI (confiance 85%)

---

## 🎭 États visuels

### Hover states manquants : 5 composants
1. ParticipantCard.tsx:45 - Bouton "Modifier"
2. StageCard.tsx:67 - Bouton "Supprimer"
3. TeamForm.tsx:120 - Bouton "Annuler"

Standard hover : hover:bg-blue-700 transition-colors
Correction auto : OUI (confiance 90%)

### Focus states manquants : 3 composants
1. ImportModal.tsx - Boutons non accessibles au clavier
2. TeamForm.tsx - Inputs sans focus visible
3. StageList.tsx - Items cliquables sans focus

Standard focus : focus:outline-none focus:ring-2 focus:ring-blue-500
Correction auto : OUI (confiance 95%)

---

## 📈 Recommandations d'amélioration

### Court terme (corrections auto possibles)
1. Uniformiser couleurs borders (12 corrections)
2. Ajouter hover states manquants (5 corrections)
3. Ajouter focus states (3 corrections)
4. Uniformiser espacements (8 corrections)

### Moyen terme (nécessite validation)
1. Renommer props pour cohérence (3 composants)
2. Ajouter labels manquants (2 formulaires)
3. Restructurer StageCard selon standard

### Long terme (architecture)
1. Créer composant Card réutilisable
2. Créer composant Form réutilisable
3. Centraliser les styles dans un design system
```

---

## 💾 Apprentissage continu

### Ce que l'agent apprend

**Scan 1-2 : Observation**
- Identifier les groupes de composants similaires
- Observer les patterns utilisés
- Pas de corrections

**Scan 3-5 : Standardisation**
- Calculer les patterns majoritaires par groupe
- Établir les standards
- Commencer les suggestions

**Scan 6+ : Correction autonome**
- Appliquer standards avec confiance >90%
- Détecter nouvelles déviations proactivement
- Suggérer optimisations architecturales

---

## 🚀 Utilisation

```bash
python component_consistency_checker_v2.py /chemin/vers/projet
```

**Depuis Claude Code :**
```
Lance component-consistency-checker-v2 sur mon projet
```

---

**Version** : 2.0.0  
**Créé pour** : Cohérence visuelle et structurelle absolue
