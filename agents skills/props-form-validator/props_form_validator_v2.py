#!/usr/bin/env python3
"""
Props & Form Validator V2 - Learning Edition
Agent intelligent d'analyse des props, modales, formulaires avec détection stricte des emojis

RÈGLE CRITIQUE : AUCUN EMOJI DANS L'APPLICATION

Usage: python props_form_validator_v2.py [project_path]
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict, field
from datetime import datetime
from collections import Counter, defaultdict

@dataclass
class Issue:
    """Représente un problème détecté"""
    file_path: str
    line_number: int
    severity: str  # "critical", "important", "minor"
    issue_type: str
    code_snippet: str
    description: str
    solution: str
    auto_fixable: bool
    confidence: float = 0.0  # 0-100

@dataclass
class ComponentInfo:
    """Informations sur un composant"""
    file_path: str
    name: str
    component_type: str  # "modal", "form", "card", "list", "other"
    props_interface: Dict[str, str]
    props_used: Set[str]
    has_form: bool = False
    has_modal_structure: bool = False
    issues: List[Issue] = field(default_factory=list)

class PropsFormValidator:
    """
    Agent intelligent d'analyse des props, modales et formulaires
    avec détection stricte des emojis
    """

    # Pattern Unicode pour détecter TOUS les emojis
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed characters
        "]+"
    )

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.components: List[ComponentInfo] = []
        self.issues: List[Issue] = []

        # Auto-détection du stack
        self.stack = self.detect_project_stack()

        # Chargement de la mémoire
        project_hash = self.get_project_hash()
        self.project_memory = self.load_project_memory(project_hash)
        self.project_hash = project_hash

        self.print_header()

    def print_header(self):
        """Affiche l'en-tête de l'analyse"""
        print("="*70)
        print("📝 Props & Form Validator V2 - Learning Edition")
        print("="*70)
        print(f"📁 Projet : {self.project_path.name}")
        print(f"🔧 Stack : {self.stack['framework']} + {self.stack['css_framework']}")
        print(f"🧠 Analyse #{self.project_memory.get('scan_count', 0) + 1}")
        print(f"⚠️  RÈGLE CRITIQUE : AUCUN EMOJI TOLÉRÉ")

        scan_count = self.project_memory.get('scan_count', 0)
        if scan_count == 0:
            print(f"🌱 État : DÉCOUVERTE (mode apprentissage)")
        elif scan_count < 5:
            print(f"🌿 État : CROISSANCE (confiance en construction)")
        elif scan_count < 10:
            print(f"🌳 État : MATURITÉ (corrections partiellement autonomes)")
        else:
            print(f"🎓 État : EXPERT (haute autonomie)")

        print("="*70)

    def get_project_hash(self) -> str:
        """Génère un hash unique pour identifier le projet"""
        project_str = str(self.project_path)
        return hashlib.md5(project_str.encode()).hexdigest()[:12]

    def detect_project_stack(self) -> Dict[str, Any]:
        """Détecte automatiquement le stack technologique du projet"""
        package_json_path = self.project_path / "package.json"

        stack = {
            "framework": "Unknown",
            "language": "JavaScript",
            "css_framework": "Unknown",
            "ui_library": None
        }

        if not package_json_path.exists():
            return stack

        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)

            deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}

            # Framework
            if 'react' in deps:
                stack['framework'] = 'React'
            elif 'vue' in deps:
                stack['framework'] = 'Vue'
            elif '@angular/core' in deps:
                stack['framework'] = 'Angular'

            # TypeScript
            if 'typescript' in deps:
                stack['language'] = 'TypeScript'

            # CSS Framework
            if 'tailwindcss' in deps:
                stack['css_framework'] = 'Tailwind'
            elif 'styled-components' in deps:
                stack['css_framework'] = 'Styled Components'
            elif '@emotion/react' in deps:
                stack['css_framework'] = 'Emotion'

            # UI Library
            if '@mui/material' in deps:
                stack['ui_library'] = 'Material-UI'
            elif 'antd' in deps:
                stack['ui_library'] = 'Ant Design'

        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture de package.json: {e}")

        return stack

    def load_project_memory(self, project_hash: str) -> Dict[str, Any]:
        """Charge la mémoire spécifique du projet"""
        brain_dir = Path.home() / ".claude-agents" / "brain" / "props-validator" / project_hash
        memory_file = brain_dir / "memory.json"

        if memory_file.exists():
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass

        return {
            "scan_count": 0,
            "last_scan": None,
            "learned_patterns": {
                "modal_structure": {},
                "form_patterns": {},
                "prop_conventions": {}
            },
            "confirmed_decisions": []
        }

    def save_project_memory(self):
        """Sauvegarde la mémoire du projet"""
        brain_dir = Path.home() / ".claude-agents" / "brain" / "props-validator" / self.project_hash
        brain_dir.mkdir(parents=True, exist_ok=True)

        memory_file = brain_dir / "memory.json"
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.project_memory, f, indent=2, default=str)

    def find_source_files(self) -> List[Path]:
        """Trouve tous les fichiers source à analyser"""
        extensions = ['.tsx', '.ts', '.jsx', '.js']

        exclude_dirs = {
            'node_modules', 'dist', 'build', '.git', 'coverage',
            '.next', 'out', '__pycache__', '.vscode', '.idea'
        }

        source_files = []
        for ext in extensions:
            for file_path in self.project_path.rglob(f'*{ext}'):
                if not any(excluded in file_path.parts for excluded in exclude_dirs):
                    source_files.append(file_path)

        return sorted(source_files)

    def detect_emojis_in_file(self, file_path: Path) -> List[Issue]:
        """Détecte TOUS les emojis dans un fichier (priorité absolue)"""
        emoji_issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                # Chercher les emojis dans le contenu visible (JSX/HTML)
                # Ignorer les commentaires
                if line.strip().startswith('//') or line.strip().startswith('/*'):
                    continue

                matches = self.EMOJI_PATTERN.finditer(line)
                for match in matches:
                    emoji = match.group()
                    emoji_issues.append(Issue(
                        file_path=str(file_path.relative_to(self.project_path)),
                        line_number=line_num,
                        severity="critical",
                        issue_type="emoji_detected",
                        code_snippet=line.strip(),
                        description=f"EMOJI DÉTECTÉ : '{emoji}' - INTERDIT dans l'application",
                        solution=f"Supprimer '{emoji}' et utiliser du texte ou une icône",
                        auto_fixable=True,
                        confidence=100.0
                    ))

        except Exception as e:
            print(f"⚠️  Erreur lecture {file_path}: {e}")

        return emoji_issues

    def extract_typescript_interface(self, content: str, component_name: str) -> Dict[str, str]:
        """Extrait l'interface TypeScript des props"""
        props_interface = {}

        # Pattern pour interface Props
        interface_pattern = rf'interface\s+{component_name}Props\s*\{{([^}}]+)\}}'
        match = re.search(interface_pattern, content, re.DOTALL)

        if match:
            props_block = match.group(1)
            # Extraire chaque prop : name: type
            prop_pattern = r'(\w+)(\??):\s*([^;\n]+)'
            for prop_match in re.finditer(prop_pattern, props_block):
                prop_name = prop_match.group(1)
                is_optional = prop_match.group(2) == '?'
                prop_type = prop_match.group(3).strip()
                props_interface[prop_name] = {
                    'type': prop_type,
                    'optional': is_optional
                }

        return props_interface

    def extract_props_usage(self, content: str) -> Set[str]:
        """Extrait les props réellement utilisées dans le composant"""
        used_props = set()

        # Pattern pour destructuration des props
        # const { prop1, prop2 } = props
        destructure_pattern = r'const\s*\{([^}]+)\}\s*=\s*props'
        match = re.search(destructure_pattern, content)
        if match:
            props_str = match.group(1)
            props_list = [p.strip() for p in props_str.split(',')]
            used_props.update(props_list)

        # Pattern pour props directement : function Component({ prop1, prop2 })
        func_pattern = r'function\s+\w+\s*\(\s*\{([^}]+)\}'
        match = re.search(func_pattern, content)
        if match:
            props_str = match.group(1)
            props_list = [p.strip().split(':')[0].strip() for p in props_str.split(',')]
            used_props.update(props_list)

        # Arrow function
        arrow_pattern = r'const\s+\w+\s*=\s*\(\s*\{([^}]+)\}\s*\)\s*=>'
        match = re.search(arrow_pattern, content)
        if match:
            props_str = match.group(1)
            props_list = [p.strip().split(':')[0].strip() for p in props_str.split(',')]
            used_props.update(props_list)

        return used_props

    def analyze_modal_structure(self, file_path: Path, content: str) -> List[Issue]:
        """Analyse la structure des modales"""
        issues = []

        # Vérifier si c'est une modale (nom contient Modal ou Dialog)
        if 'modal' not in file_path.name.lower() and 'dialog' not in file_path.name.lower():
            return issues

        component_name = file_path.stem

        # Vérifier la présence de props essentielles
        has_is_open = re.search(r'\bisOpen\b|\bopen\b|\bshow\b', content)
        has_on_close = re.search(r'\bonClose\b|\bhandleClose\b', content)

        if not has_is_open:
            issues.append(Issue(
                file_path=str(file_path.relative_to(self.project_path)),
                line_number=1,
                severity="critical",
                issue_type="missing_modal_prop",
                code_snippet="",
                description=f"Modale {component_name} manque prop 'isOpen' ou 'open'",
                solution="Ajouter prop 'isOpen: boolean' pour contrôler l'affichage",
                auto_fixable=False,
                confidence=95.0
            ))

        if not has_on_close:
            issues.append(Issue(
                file_path=str(file_path.relative_to(self.project_path)),
                line_number=1,
                severity="critical",
                issue_type="missing_modal_prop",
                code_snippet="",
                description=f"Modale {component_name} manque prop 'onClose'",
                solution="Ajouter prop 'onClose: () => void' pour gérer la fermeture",
                auto_fixable=False,
                confidence=95.0
            ))

        # Vérifier structure : header, body, footer
        has_header = re.search(r'<.*?[Hh]eader.*?>', content) or re.search(r'className=".*?modal-header.*?"', content)
        has_body = re.search(r'<.*?[Bb]ody.*?>', content) or re.search(r'className=".*?modal-body.*?"', content)

        if not has_header:
            issues.append(Issue(
                file_path=str(file_path.relative_to(self.project_path)),
                line_number=1,
                severity="important",
                issue_type="modal_structure",
                code_snippet="",
                description=f"Modale {component_name} manque section header",
                solution="Ajouter un header avec titre et bouton de fermeture",
                auto_fixable=False,
                confidence=85.0
            ))

        return issues

    def analyze_form_structure(self, file_path: Path, content: str) -> List[Issue]:
        """Analyse la structure des formulaires"""
        issues = []

        # Détecter si le fichier contient un formulaire
        has_form_tag = re.search(r'<form', content)
        has_input = re.search(r'<input|<textarea|<select', content)

        if not (has_form_tag or has_input):
            return issues

        # Trouver tous les inputs
        input_pattern = r'<input[^>]*>'
        inputs = re.finditer(input_pattern, content)

        lines = content.split('\n')

        for input_match in inputs:
            input_tag = input_match.group()

            # Vérifier si input a un label associé
            # Chercher dans les lignes autour
            input_pos = input_match.start()
            line_num = content[:input_pos].count('\n') + 1

            # Vérifier si il y a un label avant ou un aria-label
            has_label = 'aria-label=' in input_tag or 'id=' in input_tag

            # Chercher label dans les 3 lignes précédentes
            start_line = max(0, line_num - 4)
            end_line = min(len(lines), line_num + 1)
            surrounding_lines = '\n'.join(lines[start_line:end_line])

            has_label_tag = '<label' in surrounding_lines.lower()

            if not (has_label or has_label_tag):
                issues.append(Issue(
                    file_path=str(file_path.relative_to(self.project_path)),
                    line_number=line_num,
                    severity="important",
                    issue_type="missing_label",
                    code_snippet=input_tag,
                    description="Input sans label associé (problème d'accessibilité)",
                    solution="Ajouter <label> ou aria-label pour l'accessibilité",
                    auto_fixable=False,
                    confidence=90.0
                ))

        # Vérifier bouton submit
        if has_form_tag:
            has_submit = re.search(r'type=["\']submit["\']|<button[^>]*type=["\']submit["\']', content)
            if not has_submit:
                issues.append(Issue(
                    file_path=str(file_path.relative_to(self.project_path)),
                    line_number=1,
                    severity="important",
                    issue_type="missing_submit",
                    code_snippet="",
                    description="Formulaire sans bouton submit",
                    solution="Ajouter <button type='submit'> pour soumettre le formulaire",
                    auto_fixable=False,
                    confidence=85.0
                ))

        return issues

    def analyze_component_props(self, file_path: Path, content: str) -> List[Issue]:
        """Analyse les props du composant"""
        issues = []

        component_name = file_path.stem

        # Extraire interface
        props_interface = self.extract_typescript_interface(content, component_name)

        # Extraire usage
        props_used = self.extract_props_usage(content)

        if not props_interface:
            return issues

        # Détecter props définies mais jamais utilisées
        for prop_name, prop_info in props_interface.items():
            if prop_name not in props_used and not prop_info['optional']:
                # Vérifier si la prop est utilisée ailleurs dans le code (props.propName)
                if f'props.{prop_name}' not in content and f'{{{prop_name}}}' not in content:
                    issues.append(Issue(
                        file_path=str(file_path.relative_to(self.project_path)),
                        line_number=1,
                        severity="minor",
                        issue_type="unused_prop",
                        code_snippet=f"{prop_name}: {prop_info['type']}",
                        description=f"Prop '{prop_name}' définie mais jamais utilisée",
                        solution=f"Supprimer la prop ou la rendre optionnelle si inutilisée",
                        auto_fixable=False,
                        confidence=70.0
                    ))

        return issues

    def analyze_file(self, file_path: Path):
        """Analyse complète d'un fichier"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return

        # 1. PRIORITÉ ABSOLUE : Détecter les emojis
        emoji_issues = self.detect_emojis_in_file(file_path)
        self.issues.extend(emoji_issues)

        # 2. Analyser les modales
        modal_issues = self.analyze_modal_structure(file_path, content)
        self.issues.extend(modal_issues)

        # 3. Analyser les formulaires
        form_issues = self.analyze_form_structure(file_path, content)
        self.issues.extend(form_issues)

        # 4. Analyser les props
        props_issues = self.analyze_component_props(file_path, content)
        self.issues.extend(props_issues)

    def categorize_issues(self) -> Dict[str, List[Issue]]:
        """Catégorise les issues par niveau de confiance"""
        return {
            "auto_fix": [i for i in self.issues if i.auto_fixable and i.confidence >= 90],
            "recommend": [i for i in self.issues if i.confidence >= 80 and i.confidence < 90],
            "suggest": [i for i in self.issues if i.confidence >= 60 and i.confidence < 80],
            "ask": [i for i in self.issues if i.confidence < 60]
        }

    def generate_report(self) -> str:
        """Génère le rapport d'analyse"""
        categorized = self.categorize_issues()

        # Grouper par fichier
        issues_by_file = defaultdict(list)
        for issue in self.issues:
            issues_by_file[issue.file_path].append(issue)

        # Compter par sévérité
        critical = [i for i in self.issues if i.severity == "critical"]
        important = [i for i in self.issues if i.severity == "important"]
        minor = [i for i in self.issues if i.severity == "minor"]

        # Compter les emojis
        emoji_count = len([i for i in self.issues if i.issue_type == "emoji_detected"])

        report = f"""# Props & Form Validator - Rapport d'analyse

**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Projet** : {self.project_path.name}
**Stack** : {self.stack['framework']} + {self.stack['css_framework']}
**Scan** : #{self.project_memory.get('scan_count', 0) + 1}

---

## 📊 Vue d'ensemble

**Fichiers analysés** : {len(issues_by_file)}
**Issues totales** : {len(self.issues)}

### Par sévérité
- ❌ **CRITIQUES** : {len(critical)}
- ⚠️  **IMPORTANTES** : {len(important)}
- ℹ️  **MINEURES** : {len(minor)}

### Par type
"""

        if emoji_count > 0:
            report += f"""
⚠️⚠️⚠️ **ALERTE CRITIQUE** ⚠️⚠️⚠️
**{emoji_count} EMOJI(S) DÉTECTÉ(S)** - INTERDIT dans l'application !
Suppression automatique recommandée (confiance 100%)

"""

        issue_types = defaultdict(int)
        for issue in self.issues:
            issue_types[issue.issue_type] += 1

        for issue_type, count in sorted(issue_types.items(), key=lambda x: -x[1]):
            report += f"- {issue_type.replace('_', ' ').title()} : {count}\n"

        report += f"""
---

## 🎯 Actions recommandées

### ✅ Corrections automatiques ({len(categorized['auto_fix'])} issues)
Confiance ≥90% - Peut être appliqué automatiquement

"""

        for issue in categorized['auto_fix'][:10]:  # Top 10
            report += f"""
**{issue.file_path}:{issue.line_number}** [{issue.severity.upper()}]
- Type : {issue.issue_type}
- Problème : {issue.description}
- Solution : {issue.solution}
- Confiance : {issue.confidence}%
"""

        if len(categorized['auto_fix']) > 10:
            report += f"\n... et {len(categorized['auto_fix']) - 10} autres corrections automatiques\n"

        report += f"""
---

## 📁 Issues par fichier

"""

        # Top 10 fichiers avec le plus d'issues
        sorted_files = sorted(issues_by_file.items(), key=lambda x: -len(x[1]))

        for file_path, file_issues in sorted_files[:10]:
            critical_count = len([i for i in file_issues if i.severity == "critical"])
            important_count = len([i for i in file_issues if i.severity == "important"])
            minor_count = len([i for i in file_issues if i.severity == "minor"])

            report += f"""
### {file_path} ({len(file_issues)} issues)
- ❌ Critiques : {critical_count}
- ⚠️  Importantes : {important_count}
- ℹ️  Mineures : {minor_count}

"""

            for issue in file_issues[:3]:  # Top 3 issues du fichier
                report += f"""  **Ligne {issue.line_number}** [{issue.severity}] {issue.description}
  → Solution : {issue.solution}
"""

        report += f"""
---

## 📝 Notes

- Emojis : {emoji_count} détecté(s) - SUPPRESSION IMMÉDIATE requise
- Props inutilisées : À nettoyer pour réduire la complexité
- Labels manquants : Impact sur l'accessibilité

---

**Rapport généré par Props & Form Validator V2**
"""

        return report

    def run(self):
        """Exécute l'analyse complète"""
        print("\n🔍 Recherche des fichiers source...")
        source_files = self.find_source_files()
        print(f"✅ {len(source_files)} fichiers trouvés\n")

        print("📝 Analyse en cours...")
        for i, file_path in enumerate(source_files, 1):
            if i % 10 == 0:
                print(f"   Progression : {i}/{len(source_files)}")
            self.analyze_file(file_path)

        print(f"✅ Analyse terminée !\n")

        # Générer rapport
        report = self.generate_report()

        # Sauvegarder rapport
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)

        report_filename = f"props-form-analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        report_path = reports_dir / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"📄 Rapport : {report_path}")

        # Mettre à jour et sauvegarder la mémoire
        self.project_memory["scan_count"] += 1
        self.project_memory["last_scan"] = datetime.now().isoformat()
        self.save_project_memory()

        print(f"💾 Mémoire sauvegardée")

        # Afficher résumé
        categorized = self.categorize_issues()
        emoji_count = len([i for i in self.issues if i.issue_type == "emoji_detected"])

        print(f"\n📊 Résumé :")
        print(f"   Issues : {len(self.issues)}")
        if emoji_count > 0:
            print(f"   ⚠️⚠️⚠️  EMOJIS : {emoji_count} ⚠️⚠️⚠️")
        print(f"   - Corrections auto : {len(categorized['auto_fix'])}")
        print(f"   - Recommandations : {len(categorized['recommend'])}")
        print(f"   - Suggestions : {len(categorized['suggest'])}")
        print(f"   - Validation requise : {len(categorized['ask'])}")

        return report

def main():
    """Point d'entrée principal"""
    import sys

    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = "."

    validator = PropsFormValidator(project_path)
    validator.run()

if __name__ == "__main__":
    main()
