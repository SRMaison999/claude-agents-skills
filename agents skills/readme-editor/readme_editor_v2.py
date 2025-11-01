#!/usr/bin/env python3
"""
README Editor V2 - Documentation Generator
Agent intelligent de génération et maintenance automatique de documentation README

Usage: python readme_editor_v2.py [project_path]
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, asdict, field
from datetime import datetime
from collections import Counter, defaultdict

@dataclass
class ProjectAnalysis:
    """Analyse complète du projet"""
    project_name: str
    version: str
    description: str
    framework: str
    ui_library: Optional[str]
    css_framework: str
    state_management: Optional[str]
    build_tool: str
    dependencies: Dict[str, str]
    dev_dependencies: Dict[str, str]
    scripts: Dict[str, str]
    folder_structure: Dict[str, Any]
    component_count: int
    page_count: int
    hook_count: int
    util_count: int
    features: List[str]

class READMEEditor:
    """
    Agent intelligent de génération et maintenance de documentation
    """

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.analysis: Optional[ProjectAnalysis] = None

        self.print_header()

    def print_header(self):
        """Affiche l'en-tête"""
        print("="*70)
        print("📝 README Editor V2 - Documentation Generator")
        print("="*70)
        print(f"📁 Projet : {self.project_path.name}")
        print("="*70)

    def read_package_json(self) -> Dict[str, Any]:
        """Lit le package.json"""
        package_json_path = self.project_path / "package.json"

        if not package_json_path.exists():
            return {}

        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Erreur lecture package.json: {e}")
            return {}

    def detect_framework(self, deps: Dict[str, str]) -> str:
        """Détecte le framework utilisé"""
        if 'react' in deps:
            if 'next' in deps:
                return 'Next.js'
            return 'React'
        elif 'vue' in deps:
            return 'Vue'
        elif '@angular/core' in deps:
            return 'Angular'
        elif 'svelte' in deps:
            return 'Svelte'
        return 'Unknown'

    def detect_ui_library(self, deps: Dict[str, str]) -> Optional[str]:
        """Détecte la librairie UI"""
        if '@mui/material' in deps:
            return 'Material-UI'
        elif 'antd' in deps:
            return 'Ant Design'
        elif '@chakra-ui/react' in deps:
            return 'Chakra UI'
        elif '@headlessui/react' in deps:
            return 'Headless UI'
        return None

    def detect_css_framework(self, deps: Dict[str, str]) -> str:
        """Détecte le framework CSS"""
        if 'tailwindcss' in deps:
            return 'Tailwind CSS'
        elif 'styled-components' in deps:
            return 'Styled Components'
        elif '@emotion/react' in deps:
            return 'Emotion'
        elif 'sass' in deps:
            return 'Sass'
        return 'CSS'

    def detect_state_management(self, deps: Dict[str, str]) -> Optional[str]:
        """Détecte la solution de state management"""
        if 'zustand' in deps:
            return 'Zustand'
        elif 'redux' in deps or '@reduxjs/toolkit' in deps:
            return 'Redux'
        elif 'mobx' in deps:
            return 'MobX'
        elif 'recoil' in deps:
            return 'Recoil'
        elif 'jotai' in deps:
            return 'Jotai'
        return None

    def detect_build_tool(self, deps: Dict[str, str]) -> str:
        """Détecte l'outil de build"""
        if 'vite' in deps:
            return 'Vite'
        elif 'webpack' in deps:
            return 'Webpack'
        elif 'next' in deps:
            return 'Next.js (built-in)'
        elif 'parcel' in deps:
            return 'Parcel'
        return 'Unknown'

    def analyze_folder_structure(self) -> Dict[str, Any]:
        """Analyse la structure des dossiers"""
        structure = {}

        src_dir = self.project_path / "src"
        if not src_dir.exists():
            src_dir = self.project_path

        # Dossiers principaux
        main_folders = ['components', 'pages', 'hooks', 'utils', 'stores', 'contexts', 'services', 'api', 'lib']

        for folder in main_folders:
            folder_path = src_dir / folder
            if folder_path.exists():
                # Compter les fichiers
                files = list(folder_path.rglob('*.*'))
                files = [f for f in files if f.suffix in ['.ts', '.tsx', '.js', '.jsx']]
                structure[folder] = {
                    'count': len(files),
                    'path': str(folder_path.relative_to(self.project_path))
                }

        return structure

    def count_components(self) -> int:
        """Compte le nombre de composants"""
        count = 0
        search_dirs = [
            self.project_path / "src" / "components",
            self.project_path / "components"
        ]

        for search_dir in search_dirs:
            if search_dir.exists():
                files = list(search_dir.rglob('*.tsx')) + list(search_dir.rglob('*.jsx'))
                count += len(files)

        return count

    def count_pages(self) -> int:
        """Compte le nombre de pages"""
        count = 0
        search_dirs = [
            self.project_path / "src" / "pages",
            self.project_path / "pages",
            self.project_path / "app"
        ]

        for search_dir in search_dirs:
            if search_dir.exists():
                files = list(search_dir.rglob('*.tsx')) + list(search_dir.rglob('*.jsx'))
                count += len(files)

        return count

    def count_hooks(self) -> int:
        """Compte le nombre de hooks"""
        count = 0
        search_dirs = [
            self.project_path / "src" / "hooks",
            self.project_path / "hooks"
        ]

        for search_dir in search_dirs:
            if search_dir.exists():
                files = list(search_dir.rglob('*.ts')) + list(search_dir.rglob('*.js'))
                count += len(files)

        return count

    def count_utils(self) -> int:
        """Compte le nombre de fichiers utils"""
        count = 0
        search_dirs = [
            self.project_path / "src" / "utils",
            self.project_path / "utils",
            self.project_path / "src" / "lib",
            self.project_path / "lib"
        ]

        for search_dir in search_dirs:
            if search_dir.exists():
                files = list(search_dir.rglob('*.ts')) + list(search_dir.rglob('*.js'))
                count += len(files)

        return count

    def detect_main_features(self) -> List[str]:
        """Détecte les fonctionnalités principales en analysant les composants"""
        features = set()

        # Analyser les noms de dossiers dans components
        components_dir = self.project_path / "src" / "components"
        if not components_dir.exists():
            components_dir = self.project_path / "components"

        if components_dir.exists():
            for folder in components_dir.iterdir():
                if folder.is_dir() and not folder.name.startswith('.'):
                    # Convertir en feature lisible
                    feature_name = folder.name.replace('_', ' ').replace('-', ' ').title()
                    features.add(f"Gestion des {feature_name}")

        # Analyser les pages
        pages_dir = self.project_path / "src" / "pages"
        if not pages_dir.exists():
            pages_dir = self.project_path / "pages"

        if pages_dir.exists():
            for file in pages_dir.rglob('*.tsx'):
                if file.stem not in ['_app', '_document', 'index']:
                    feature_name = file.stem.replace('_', ' ').replace('-', ' ').title()
                    features.add(feature_name)

        return sorted(list(features))[:10]  # Top 10

    def analyze_project(self) -> ProjectAnalysis:
        """Analyse complète du projet"""
        print("\n🔍 Analyse du projet...")

        package_data = self.read_package_json()

        deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}

        analysis = ProjectAnalysis(
            project_name=package_data.get('name', self.project_path.name),
            version=package_data.get('version', '1.0.0'),
            description=package_data.get('description', ''),
            framework=self.detect_framework(deps),
            ui_library=self.detect_ui_library(deps),
            css_framework=self.detect_css_framework(deps),
            state_management=self.detect_state_management(deps),
            build_tool=self.detect_build_tool(deps),
            dependencies=package_data.get('dependencies', {}),
            dev_dependencies=package_data.get('devDependencies', {}),
            scripts=package_data.get('scripts', {}),
            folder_structure=self.analyze_folder_structure(),
            component_count=self.count_components(),
            page_count=self.count_pages(),
            hook_count=self.count_hooks(),
            util_count=self.count_utils(),
            features=self.detect_main_features()
        )

        print(f"✅ Analyse terminée")
        print(f"   Framework : {analysis.framework}")
        print(f"   CSS : {analysis.css_framework}")
        print(f"   Composants : {analysis.component_count}")
        print(f"   Pages : {analysis.page_count}")

        return analysis

    def generate_folder_tree(self) -> str:
        """Génère l'arbre des dossiers"""
        tree = "src/\n"

        for folder, info in sorted(self.analysis.folder_structure.items()):
            count = info['count']
            tree += f"├── {folder}/".ljust(30) + f"  # {count} fichier(s)\n"

        return tree

    def generate_mermaid_architecture(self) -> str:
        """Génère un diagramme d'architecture Mermaid"""
        diagram = "```mermaid\ngraph TD\n"

        # Nœuds principaux
        diagram += "    A[Application] --> B[Components]\n"

        if 'pages' in self.analysis.folder_structure:
            diagram += "    A --> C[Pages]\n"

        if 'hooks' in self.analysis.folder_structure:
            diagram += "    B --> D[Custom Hooks]\n"

        if 'stores' in self.analysis.folder_structure or self.analysis.state_management:
            diagram += "    A --> E[State Management]\n"

        if 'api' in self.analysis.folder_structure or 'services' in self.analysis.folder_structure:
            diagram += "    A --> F[API/Services]\n"

        if 'utils' in self.analysis.folder_structure:
            diagram += "    A --> G[Utils]\n"

        diagram += "```\n"

        return diagram

    def generate_main_readme(self) -> str:
        """Génère le README principal"""
        a = self.analysis

        readme = f"""# {a.project_name}

{a.description if a.description else 'Application web moderne'}

![Version](https://img.shields.io/badge/version-{a.version}-blue)
"""

        # Badges framework
        if 'react' in a.dependencies:
            react_version = a.dependencies['react'].replace('^', '').replace('~', '')
            readme += f"![React](https://img.shields.io/badge/react-{react_version}-blue)\n"

        if 'typescript' in a.dependencies or 'typescript' in a.dev_dependencies:
            readme += f"![TypeScript](https://img.shields.io/badge/typescript-yes-blue)\n"

        readme += f"""
---

## 🎯 Fonctionnalités

"""

        if a.features:
            for feature in a.features:
                readme += f"- {feature}\n"
        else:
            readme += "- Interface utilisateur moderne et responsive\n"
            readme += "- Gestion des données optimisée\n"

        readme += f"""
---

## 🚀 Démarrage rapide

### Prérequis

- Node.js 18+
- npm ou yarn

### Installation

```bash
git clone <repository_url>
cd {a.project_name}
npm install
```

### Lancement

```bash
npm run dev
```

"""

        # Détecter le port
        if 'dev' in a.scripts:
            if 'vite' in a.scripts['dev']:
                readme += "L'application sera accessible sur `http://localhost:5173`\n"
            elif 'next' in a.scripts['dev']:
                readme += "L'application sera accessible sur `http://localhost:3000`\n"

        readme += f"""
---

## 🏗️ Architecture

### Structure des dossiers

```
{self.generate_folder_tree()}```

### Technologies utilisées

**Frontend :**
- {a.framework}
"""

        if a.ui_library:
            readme += f"- {a.ui_library}\n"

        readme += f"- {a.css_framework}\n"

        if a.state_management:
            readme += f"\n**State Management :**\n- {a.state_management}\n"

        readme += f"""
**Build Tool :**
- {a.build_tool}

"""

        # Diagramme Mermaid
        readme += f"""### Diagramme d'architecture

{self.generate_mermaid_architecture()}
---

## 📦 Scripts disponibles

"""

        for script, command in a.scripts.items():
            readme += f"- `npm run {script}` : {command}\n"

        readme += f"""
---

## 📊 Statistiques

- **Composants** : {a.component_count}
- **Pages** : {a.page_count}
- **Custom Hooks** : {a.hook_count}
- **Utils** : {a.util_count}

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit les changements (`git commit -m 'Ajout amelioration'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

---

## 📝 Licence

Ce projet est sous licence MIT.

---

**README généré automatiquement par README Editor V2**
*Dernière mise à jour : {datetime.now().strftime('%Y-%m-%d')}*
"""

        return readme

    def generate_folder_readme(self, folder_name: str, folder_path: Path) -> str:
        """Génère un README pour un dossier spécifique"""
        files = list(folder_path.rglob('*.tsx')) + list(folder_path.rglob('*.ts'))
        files = [f for f in files if not f.name.startswith('.')]

        readme = f"""# {folder_name.title()}

Ce dossier contient {len(files)} fichier(s).

## Fichiers

"""

        for file in sorted(files):
            relative_path = file.relative_to(folder_path)
            readme += f"- `{relative_path}` : {file.stem}\n"

        readme += f"""
---

*README généré automatiquement par README Editor V2*
"""

        return readme

    def run(self):
        """Exécute la génération de documentation"""
        # Analyser le projet
        self.analysis = self.analyze_project()

        # Générer README principal
        print("\n📝 Génération du README principal...")
        main_readme = self.generate_main_readme()

        readme_path = self.project_path / "README.md"

        # Vérifier si README existe déjà
        if readme_path.exists():
            backup_path = self.project_path / f"README.backup.{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
            print(f"⚠️  README existant sauvegardé : {backup_path.name}")
            readme_path.rename(backup_path)

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(main_readme)

        print(f"✅ README principal généré : {readme_path}")

        # Générer README par dossier (optionnel)
        generate_folder_readmes = input("\nGénérer README pour chaque dossier ? [o/N] : ")

        if generate_folder_readmes.lower() in ['o', 'oui', 'y', 'yes']:
            print("\n📁 Génération des README de dossiers...")

            for folder_name, info in self.analysis.folder_structure.items():
                folder_path = self.project_path / info['path']

                if folder_path.exists() and info['count'] > 0:
                    folder_readme = self.generate_folder_readme(folder_name, folder_path)

                    folder_readme_path = folder_path / "README.md"

                    with open(folder_readme_path, 'w', encoding='utf-8') as f:
                        f.write(folder_readme)

                    print(f"   ✅ {folder_name}/README.md")

        print(f"\n✅ Documentation générée avec succès !")

def main():
    """Point d'entrée principal"""
    import sys

    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = "."

    editor = READMEEditor(project_path)
    editor.run()

if __name__ == "__main__":
    main()
