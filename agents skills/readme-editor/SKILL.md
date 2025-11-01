# README Editor V2 - Documentation Generator

Agent intelligent de génération et maintenance automatique de documentation README.

**Version** : 2.0.0  
**Type** : Documentation Generator + Maintainer  
**Autonomie** : Équilibrée (génère auto, demande validation)  
**Mémoire** : Par projet (style et structure apprises)  

---

## 🎯 Mission

Générer et maintenir automatiquement la documentation :
1. **README.md principal** du projet
2. **README.md par dossier** (components, utils, etc.)
3. **Mise à jour automatique** lors des changements
4. **Documentation des composants** individuels
5. **Architecture et diagrammes** (Mermaid)

---

## 📝 Génération du README principal

### Étape 1 : Analyse du projet

```python
def analyze_project_structure(project_path: Path) -> ProjectAnalysis:
    """Analyse complète du projet pour générer le README"""
    
    analysis = ProjectAnalysis()
    
    # 1. Lire package.json
    package_json = read_package_json(project_path)
    analysis.project_name = package_json.get("name")
    analysis.version = package_json.get("version")
    analysis.description = package_json.get("description")
    analysis.dependencies = package_json.get("dependencies", {})
    
    # 2. Détecter le stack technique
    analysis.framework = detect_framework(analysis.dependencies)
    analysis.ui_library = detect_ui_library(analysis.dependencies)
    analysis.css_framework = detect_css_framework(analysis.dependencies)
    analysis.state_management = detect_state_management(analysis.dependencies)
    analysis.build_tool = detect_build_tool(analysis.dependencies)
    
    # 3. Analyser la structure des dossiers
    analysis.folder_structure = analyze_folder_structure(project_path)
    
    # 4. Compter les composants
    analysis.component_count = count_components(project_path)
    analysis.page_count = count_pages(project_path)
    
    # 5. Détecter les features principales
    analysis.features = detect_main_features(project_path)
    
    # 6. Analyser les scripts disponibles
    analysis.scripts = package_json.get("scripts", {})
    
    return analysis
```

### Étape 2 : Générer le contenu

**Structure standard générée :**

```markdown
# {Project Name}

{Description automatique basée sur l'analyse}

![Version](https://img.shields.io/badge/version-{version}-blue)
![React](https://img.shields.io/badge/react-{version}-blue)
![TypeScript](https://img.shields.io/badge/typescript-{version}-blue)

---

## 🎯 Fonctionnalités

{Liste générée automatiquement depuis l'analyse des composants}

- Gestion des équipes
- Suivi des étapes
- Calendrier global
- Import/Export de données
- etc.

---

## 🚀 Démarrage rapide

### Prérequis

- Node.js {detected_version}+
- npm ou yarn

### Installation

```bash
git clone {repository_url}
cd {project_name}
npm install
```

### Lancement

```bash
npm run dev
```

L'application sera accessible sur `http://localhost:{port}`

---

## 🏗️ Architecture

### Structure des dossiers

```
{Arbre généré automatiquement}
src/
├── components/
│   ├── teams/          # Composants équipes (3)
│   ├── stages/         # Composants étapes (4)
│   ├── participants/   # Composants participants (5)
│   └── personnel/      # Base de personnel (7)
├── hooks/              # Custom hooks (3)
├── stores/             # State management (2)
└── utils/              # Utilitaires (4)
```

### Technologies utilisées

{Détection automatique depuis package.json}

**Frontend :**
- React {version}
- TypeScript
- Tailwind CSS

**State Management :**
- Zustand

**Build Tool :**
- Vite

**Icônes :**
- Lucide React

---

## 📦 Composants principaux

{Génération automatique depuis l'analyse des composants}

### Teams Management
**Fichiers** : `src/components/teams/`
**Composants** : TeamCard, TeamList, TeamForm, TeamManager
**Description** : Gestion complète des équipes avec création, édition et suppression

### Stage Management  
**Fichiers** : `src/components/stages/`
**Composants** : StageCard, StageList, StageForm, StageImportModal
**Description** : Gestion des étapes avec import automatique et schémas de travail

### Participants
**Fichiers** : `src/components/participants/`
**Composants** : ParticipantCard, ParticipantList, ParticipantManager
**Description** : Gestion des participants avec import depuis base de personnel

---

## 🎨 Design System

{Détection automatique des patterns Tailwind}

**Couleurs principales :**
- Primary : `bg-blue-600`
- Secondary : `bg-gray-200`
- Danger : `bg-red-600`
- Success : `bg-green-600`

**Espacements standards :**
- Padding : `p-4`, `p-6`
- Margin : `mb-2`, `mb-4`

**Typographie :**
- Titres : `text-xl font-semibold`
- Texte : `text-sm text-gray-600`

---

## 📖 Documentation détaillée

{Génération automatique des liens vers docs des composants}

- [📅 Calendrier](./docs/calendar.md)
- [📁 Projets](./docs/projects.md)
- [🗺️ Étapes](./docs/stages.md)
- [👥 Équipes](./docs/teams.md)

---

## 🧪 Tests

{Détection automatique de la présence de tests}

```bash
npm run test        # Lancer les tests
npm run test:watch  # Mode watch
npm run coverage    # Rapport de couverture
```

**Couverture actuelle** : {detected_coverage}%

---

## 🛠️ Scripts disponibles

{Extraction depuis package.json}

| Script | Description |
|--------|-------------|
| `npm run dev` | Démarre le serveur de développement |
| `npm run build` | Build de production |
| `npm run preview` | Preview du build |
| `npm run lint` | Lint du code |

---

## 📝 Convention de commits

{Détection automatique si conventional commits utilisé}

Ce projet utilise [Conventional Commits](https://www.conventionalcommits.org/).

Format : `type(scope): description`

Types : feat, fix, docs, style, refactor, test, chore

---

## 🤝 Contribution

{Génération standard ou personnalisable}

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'feat: Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📜 Licence

{Extraction depuis package.json ou détection fichier LICENSE}

{license_type}

---

## 👥 Auteurs

{Extraction depuis package.json}

- **{author_name}** - {author_email}

---

## 🙏 Remerciements

{Section optionnelle, personnalisable}

---

**Dernière mise à jour** : {timestamp}
**Généré automatiquement par** : README Editor V2
```

---

## 📁 README par dossier

### Génération automatique pour chaque dossier majeur

```python
def generate_folder_readme(folder_path: Path) -> str:
    """Génère un README pour un dossier spécifique"""
    
    # Analyser le contenu du dossier
    components = find_components_in_folder(folder_path)
    hooks = find_hooks_in_folder(folder_path)
    utils = find_utils_in_folder(folder_path)
    
    readme_content = f"""# {folder_path.name}

{generate_folder_description(folder_path)}

---

## 📂 Contenu

**Composants** : {len(components)}
**Hooks** : {len(hooks)}
**Utilitaires** : {len(utils)}

---

## 📋 Fichiers

"""
    
    # Liste des fichiers avec description
    for component in components:
        readme_content += f"""
### {component.name}

**Fichier** : `{component.file_name}`
**Type** : {component.type}
**Props** : {len(component.props)}

{component.description}

**Usage** :
```tsx
<{component.name} 
  {generate_props_example(component.props)}
/>
```
"""
    
    return readme_content
```

**Exemple généré pour `/src/components/teams/` :**

```markdown
# teams

Composants de gestion des équipes de production.

---

## 📂 Contenu

**Composants** : 4
**Types** : 1

---

## 📋 Fichiers

### TeamManager

**Fichier** : `TeamManager.tsx`
**Type** : Manager Component
**Props** : 1

Composant principal de gestion des équipes. Gère la liste, l'ajout, la modification et la suppression d'équipes.

**Usage** :
```tsx
<TeamManager projectId="abc123" />
```

**Props** :
- `projectId` (string, required) : ID du projet actif

---

### TeamList

**Fichier** : `TeamList.tsx`
**Type** : Display Component
**Props** : 3

Affiche la liste des équipes avec possibilité de tri et filtrage.

**Usage** :
```tsx
<TeamList 
  teams={teams}
  onEdit={handleEdit}
  onDelete={handleDelete}
/>
```

**Props** :
- `teams` (Team[], required) : Liste des équipes
- `onEdit` ((id: string) => void, required) : Callback édition
- `onDelete` ((id: string) => void, required) : Callback suppression

---

### TeamCard

**Fichier** : `TeamCard.tsx`
**Type** : Display Component
**Props** : 4

Carte d'affichage individuelle d'une équipe.

**Usage** :
```tsx
<TeamCard 
  team={team}
  onEdit={handleEdit}
  onDelete={handleDelete}
  isSelected={false}
/>
```

---

### TeamForm

**Fichier** : `TeamForm.tsx`
**Type** : Form Component
**Props** : 3

Formulaire de création/édition d'équipe.

**Usage** :
```tsx
<TeamForm 
  team={existingTeam}
  onSubmit={handleSubmit}
  onCancel={handleCancel}
/>
```

---

## 🔗 Dépendances

**Stores** :
- `useProjectStore` (state management)

**Hooks** :
- `useTeamValidation` (validation formulaire)

**Types** :
- `Team` (types.ts)

---

**Dernière mise à jour** : 2025-10-31
```

---

## 🔄 Mise à jour automatique

### Détection des changements

```python
def detect_readme_updates_needed(project_path: Path) -> List[UpdateNeeded]:
    """Détecte si le README nécessite des mises à jour"""
    
    updates = []
    
    # 1. Lire le README actuel
    current_readme = read_current_readme(project_path)
    
    # 2. Analyser le projet actuel
    current_state = analyze_project_structure(project_path)
    
    # 3. Comparer
    
    # Nouvelle dépendance ?
    if current_state.dependencies != extract_dependencies_from_readme(current_readme):
        updates.append(UpdateNeeded(
            section="technologies",
            reason="Nouvelle dépendance ajoutée",
            action="Mettre à jour la liste des technologies"
        ))
    
    # Nouveau composant ?
    readme_component_count = extract_component_count(current_readme)
    if current_state.component_count != readme_component_count:
        updates.append(UpdateNeeded(
            section="components",
            reason=f"Nombre de composants changé ({readme_component_count} → {current_state.component_count})",
            action="Mettre à jour la liste des composants"
        ))
    
    # Nouvelle feature ?
    current_features = extract_features_from_code(project_path)
    readme_features = extract_features_from_readme(current_readme)
    new_features = set(current_features) - set(readme_features)
    
    if new_features:
        updates.append(UpdateNeeded(
            section="features",
            reason=f"{len(new_features)} nouvelles fonctionnalités détectées",
            action=f"Ajouter : {', '.join(new_features)}"
        ))
    
    return updates
```

### Application des mises à jour

**Mode automatique (confiance >90%) :**
- Ajout de dépendances
- Mise à jour du nombre de composants
- Mise à jour du timestamp

**Mode validation (confiance <90%) :**
- Ajout de nouvelles features (description nécessaire)
- Modification de la description du projet
- Restructuration de sections

---

## 📊 Diagrammes automatiques

### Génération de diagrammes Mermaid

**Diagramme d'architecture :**

```python
def generate_architecture_diagram(project_structure: ProjectStructure) -> str:
    """Génère un diagramme d'architecture Mermaid"""
    
    diagram = """```mermaid
graph TD
    A[App.tsx] --> B[Router]
    B --> C[ProjectSelector]
    B --> D[CalendarView]
    B --> E[TeamManager]
    B --> F[StageManager]
    
    E --> E1[TeamList]
    E --> E2[TeamForm]
    E1 --> E3[TeamCard]
    
    F --> F1[StageList]
    F --> F2[StageForm]
    F1 --> F3[StageCard]
    
    G[useProjectStore] --> C
    G --> E
    G --> F
```"""
    
    return diagram
```

**Diagramme de flux de données :**

```python
def generate_data_flow_diagram() -> str:
    """Génère un diagramme de flux de données"""
    
    return """```mermaid
sequenceDiagram
    participant U as User
    participant TM as TeamManager
    participant Store as ProjectStore
    participant API as Backend
    
    U->>TM: Créer équipe
    TM->>Store: dispatch(createTeam)
    Store->>API: POST /teams
    API-->>Store: Team créée
    Store-->>TM: État mis à jour
    TM-->>U: Confirmation
```"""
```

---

## 🎯 Sections spéciales

### Pour applications avec API

**Section API générée automatiquement :**

```markdown
## 📡 API

### Endpoints disponibles

{Détection automatique depuis le code}

**Teams**
- `GET /api/teams` - Liste des équipes
- `POST /api/teams` - Créer une équipe
- `PUT /api/teams/:id` - Modifier une équipe
- `DELETE /api/teams/:id` - Supprimer une équipe

**Stages**
- `GET /api/stages` - Liste des étapes
- `POST /api/stages` - Créer une étape

### Format des données

{Extraction depuis les types TypeScript}

**Team**
```typescript
{
  id: string;
  name: string;
  members: string[];
  createdAt: Date;
}
```
```

### Pour projets avec tests

```markdown
## 🧪 Tests

**Coverage** : {calculated}%

### Tests par composant

| Composant | Tests | Coverage |
|-----------|-------|----------|
| TeamCard | 5 | 100% |
| TeamForm | 8 | 95% |
| TeamList | 6 | 90% |

### Lancer les tests

```bash
npm run test              # Tous les tests
npm run test TeamCard     # Tests spécifiques
npm run coverage          # Rapport complet
```
```

---

## 🚀 Utilisation

### Génération initiale

```bash
python readme_editor_v2.py /chemin/vers/projet --generate
```

**Génère** :
- README.md principal
- README.md par dossier important
- Diagrammes d'architecture

### Mise à jour

```bash
python readme_editor_v2.py /chemin/vers/projet --update
```

**Détecte et applique** :
- Nouvelles dépendances
- Nouveaux composants
- Nouvelles features
- Changements de structure

### Mode watch

```bash
python readme_editor_v2.py /chemin/vers/projet --watch
```

**Surveille et met à jour automatiquement**

---

## 📋 Configuration

**Fichier `.readme-config.json` :**

```json
{
  "style": "detailed",
  "sections": {
    "features": true,
    "architecture": true,
    "api": true,
    "tests": true,
    "diagrams": true
  },
  "auto_update": true,
  "generate_folder_readmes": true,
  "language": "fr"
}
```

---

**Version** : 2.0.0  
**Créé pour** : Documentation automatique et à jour
