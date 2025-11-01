#!/usr/bin/env python3
"""
README Editor V3 - Générateur de documentation

Analyse le projet et génère/met à jour :
- README.md principal (racine)
- README.md par dossier (components/, utils/)
- README-UPDATE.md dans session/3-DOCUMENTATION/

Usage:
    python readme_editor_v3.py /path/to/project --session /path/to/session
"""

import sys
import io
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from collections import Counter

# Forcer UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

class READMEEditorV3:
    """
    Générateur de documentation intelligent
    """

    def __init__(self, project_path: Path, session_path: Path):
        self.project_path = project_path
        self.session_path = session_path
        self.package_data = {}
        self.stats = {}
        self.readmes_created = []
        self.readmes_updated = []

    def read_package_json(self) -> Dict[str, Any]:
        """Lit le package.json"""
        package_file = self.project_path / "package.json"

        if not package_file.exists():
            return {}

        try:
            with open(package_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def analyze_project(self):
        """Analyse le projet"""

        self.package_data = self.read_package_json()

        # Compter les fichiers
        src_dir = self.project_path / "src"
        if not src_dir.exists():
            src_dir = self.project_path

        self.stats = {
            "components": len(list(src_dir.glob("**/components/**/*.tsx"))) + len(list(src_dir.glob("**/components/**/*.jsx"))),
            "pages": len(list(src_dir.glob("**/pages/**/*.tsx"))) + len(list(src_dir.glob("**/pages/**/*.jsx"))),
            "hooks": len(list(src_dir.glob("**/hooks/**/*.ts"))) + len(list(src_dir.glob("**/hooks/**/*.js"))),
            "utils": len(list(src_dir.glob("**/utils/**/*.ts"))) + len(list(src_dir.glob("**/utils/**/*.js"))),
        }

    def generate_main_readme(self) -> str:
        """Génère le README principal"""

        name = self.package_data.get("name", self.project_path.name)
        version = self.package_data.get("version", "1.0.0")
        description = self.package_data.get("description", "")

        deps = self.package_data.get("dependencies", {})
        framework = "React" if "react" in deps else "Unknown"
        css = "Tailwind CSS" if "tailwindcss" in deps else "CSS"

        readme = f"""# {name}

{description if description else "Application moderne"}

**Version** : {version}

---

## 🚀 Technologies

- **Framework** : {framework}
- **Styling** : {css}
- **Build Tool** : Vite

---

## 📊 Statistiques

- **Composants** : {self.stats.get('components', 0)}
- **Pages** : {self.stats.get('pages', 0)}
- **Custom Hooks** : {self.stats.get('hooks', 0)}
- **Utils** : {self.stats.get('utils', 0)}

---

## 🏗️ Installation

```bash
# Cloner le projet
git clone <repository_url>
cd {name}

# Installer les dépendances
npm install

# Lancer en développement
npm run dev
```

---

## 📝 Scripts disponibles

"""

        for script, command in self.package_data.get("scripts", {}).items():
            readme += f"- `npm run {script}` : {command}\n"

        readme += f"""
---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit les changements (`git commit -m 'Ajout amelioration'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

---

**Dernière mise à jour** : {datetime.now().strftime('%Y-%m-%d')}
"""

        return readme

    def generate_folder_readme(self, folder_name: str) -> str:
        """Génère un README pour un dossier"""

        readme = f"""# {folder_name.title()}

Ce dossier contient les {folder_name}.

---

**Dernière mise à jour** : {datetime.now().strftime('%Y-%m-%d')}
"""

        return readme

    def update_readmes(self):
        """Met à jour les README"""

        # README principal
        main_readme_path = self.project_path / "README.md"

        if main_readme_path.exists():
            self.readmes_updated.append("README.md")
        else:
            self.readmes_created.append("README.md")

        readme_content = self.generate_main_readme()

        with open(main_readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        print(f"✅ README.md principal {'mis à jour' if main_readme_path in self.readmes_updated else 'créé'}")

        # README par dossier
        src_dir = self.project_path / "src"
        if src_dir.exists():
            for folder_name in ["components", "utils", "hooks"]:
                folder_path = src_dir / folder_name
                if folder_path.exists() and folder_path.is_dir():
                    readme_path = folder_path / "README.md"

                    if readme_path.exists():
                        self.readmes_updated.append(f"src/{folder_name}/README.md")
                    else:
                        self.readmes_created.append(f"src/{folder_name}/README.md")

                    folder_readme = self.generate_folder_readme(folder_name)

                    with open(readme_path, 'w', encoding='utf-8') as f:
                        f.write(folder_readme)

                    print(f"✅ README.md {folder_name} {'mis à jour' if readme_path in self.readmes_updated else 'créé'}")

    def generate_update_report(self) -> str:
        """Génère le rapport README-UPDATE.md"""

        report = f"""# Mise à jour documentation - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Projet** : {self.project_path.name}
**Session** : {self.session_path.name}

---

## 📊 Vue d'ensemble

**README créés** : {len(self.readmes_created)}
**README mis à jour** : {len(self.readmes_updated)}

---

## 📄 Fichiers modifiés

"""

        if self.readmes_created:
            report += "### Nouveaux README\n\n"
            for readme in self.readmes_created:
                report += f"- {readme}\n"
            report += "\n"

        if self.readmes_updated:
            report += "### README mis à jour\n\n"
            for readme in self.readmes_updated:
                report += f"- {readme}\n"
            report += "\n"

        report += f"""---

**Rapport généré par README Editor V3**
*Session : {self.session_path.name}*
"""

        return report

    def run(self):
        """Lance le processus complet"""

        print("=" * 80)
        print("📝 README EDITOR V3")
        print("=" * 80)
        print(f"📁 Projet  : {self.project_path.name}")
        print(f"🆔 Session : {self.session_path.name}")
        print("=" * 80)
        print()

        # 1. Analyser le projet
        print("🔍 Analyse du projet...\n")
        self.analyze_project()

        # 2. Mettre à jour les README
        print("📝 Mise à jour des README...\n")
        self.update_readmes()

        # 3. Générer le rapport
        report = self.generate_update_report()

        # 4. Sauvegarder le rapport
        doc_dir = self.session_path / "3-DOCUMENTATION"
        doc_dir.mkdir(parents=True, exist_ok=True)

        report_path = doc_dir / "README-UPDATE.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n📄 Rapport : {report_path.relative_to(self.session_path)}")
        print()

def main():
    """Point d'entrée"""

    if len(sys.argv) < 4 or sys.argv[2] != "--session":
        print("Usage: python readme_editor_v3.py /path/to/project --session /path/to/session")
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()
    session_path = Path(sys.argv[3]).resolve()

    if not project_path.exists():
        print(f"❌ Projet introuvable : {project_path}")
        sys.exit(1)

    if not session_path.exists():
        print(f"❌ Session introuvable : {session_path}")
        sys.exit(1)

    editor = READMEEditorV3(project_path, session_path)
    editor.run()

if __name__ == "__main__":
    main()
