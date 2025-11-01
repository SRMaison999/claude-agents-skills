#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Component Consistency Checker V2 - Learning Edition
Agent intelligent de vérification de la cohérence visuelle et structurelle des composants

Usage: python consistency_checker_v2.py [project_path]
"""

import os
import re
import json
import hashlib
from pathlib import Path

def read_file_content_with_fallback_encoding(file_path):
    """Lit le contenu complet d'un fichier en essayant plusieurs encodages"""
    for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    # Si tous échouent, retourner chaîne vide
    return ""

def read_json_with_fallback_encoding(file_path):
    """Lit un fichier JSON en essayant plusieurs encodages"""
    import json
    for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return json.load(f)
        except (UnicodeDecodeError, UnicodeError):
            continue
        except json.JSONDecodeError:
            return None
    return None

from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
from collections import Counter, defaultdict

@dataclass
class ConsistencyIssue:
    """Représente une incohérence détectée"""
    file_path: str
    line_number: int
    severity: str  # "critical", "important", "minor"
    issue_type: str
    category: str  # "colors", "spacing", "typography", etc.
    code_snippet: str
    description: str
    solution: str
    standard_value: str
    actual_value: str
    auto_fixable: bool
    confidence: float = 0.0

@dataclass
class ComponentGroup:
    """Groupe de composants similaires"""
    name: str
    components: List[str]
    patterns: Dict[str, Counter]
    standard_pattern: Dict[str, Any]

@dataclass
class VisualPattern:
    """Pattern visuel extrait d'un composant"""
    colors: Counter
    spacing: Counter
    typography: Counter
    borders: Counter
    shadows: Counter
    transitions: Counter
    states: Dict[str, Counter]

class ConsistencyChecker:
    """
    Agent intelligent de vérification de la cohérence entre composants similaires
    """

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.component_groups: List[ComponentGroup] = []
        self.issues: List[ConsistencyIssue] = []

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
        print("🎨 Component Consistency Checker V2 - Learning Edition")
        print("="*70)
        print(f"📁 Projet : {self.project_path.name}")
        print(f"🔧 Stack : {self.stack['framework']} + {self.stack['css_framework']}")
        print(f"🧠 Analyse #{self.project_memory.get('scan_count', 0) + 1}")

        scan_count = self.project_memory.get('scan_count', 0)
        if scan_count == 0:
            print(f"🌱 État : DÉCOUVERTE (apprentissage des patterns)")
        elif scan_count < 5:
            print(f"🌿 État : CROISSANCE (identification des standards)")
        elif scan_count < 10:
            print(f"🌳 État : MATURITÉ (détection des incohérences)")
        else:
            print(f"🎓 État : EXPERT (corrections autonomes)")

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
            "css_framework": "Unknown"
        }

        if not package_json_path.exists():
            return stack

        try:
            package_data = read_json_with_fallback_encoding(package_json_path)
            if not package_data:
                return stack

            deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}

            if 'react' in deps:
                stack['framework'] = 'React'
            elif 'vue' in deps:
                stack['framework'] = 'Vue'

            if 'tailwindcss' in deps:
                stack['css_framework'] = 'Tailwind'
            elif 'styled-components' in deps:
                stack['css_framework'] = 'Styled Components'

        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture de package.json: {e}")

        return stack

    def load_project_memory(self, project_hash: str) -> Dict[str, Any]:
        """Charge la mémoire spécifique du projet"""
        brain_dir = Path.home() / ".claude-agents" / "brain" / "consistency-checker" / project_hash
        memory_file = brain_dir / "memory.json"

        if memory_file.exists():
            try:
                memory = read_json_with_fallback_encoding(memory_file)
                if memory:
                    return memory
            except:
                pass

        return {
            "scan_count": 0,
            "last_scan": None,
            "learned_standards": {},
            "component_groups": {}
        }

    def save_project_memory(self):
        """Sauvegarde la mémoire du projet"""
        brain_dir = Path.home() / ".claude-agents" / "brain" / "consistency-checker" / self.project_hash
        brain_dir.mkdir(parents=True, exist_ok=True)

        memory_file = brain_dir / "memory.json"

        # Sauvegarder les standards appris
        self.project_memory["learned_standards"] = {}
        for group in self.component_groups:
            self.project_memory["learned_standards"][group.name] = group.standard_pattern

        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.project_memory, f, indent=2, default=str)

    def find_component_files(self) -> List[Path]:
        """Trouve tous les fichiers de composants"""
        extensions = ['.tsx', '.ts', '.jsx', '.js']

        exclude_dirs = {
            'node_modules', 'dist', 'build', '.git', 'coverage',
            '.next', 'out', '__pycache__', '.vscode', '.idea'
        }

        component_files = []

        # Chercher dans src/components ou components
        search_dirs = [
            self.project_path / "src" / "components",
            self.project_path / "components",
            self.project_path / "src"
        ]

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue

            for ext in extensions:
                for file_path in search_dir.rglob(f'*{ext}'):
                    if not any(excluded in file_path.parts for excluded in exclude_dirs):
                        # Vérifier que c'est un composant (commence par majuscule)
                        if file_path.stem[0].isupper():
                            component_files.append(file_path)

        return sorted(component_files)

    def group_similar_components(self, component_files: List[Path]) -> List[List[Path]]:
        """Groupe les composants similaires par nom"""
        groups = defaultdict(list)

        # Patterns de suffixes communs
        common_suffixes = ['Card', 'Form', 'Modal', 'List', 'Item', 'Button', 'Input', 'Table', 'Panel', 'Dialog']

        for file_path in component_files:
            component_name = file_path.stem

            # Chercher le suffixe
            for suffix in common_suffixes:
                if component_name.endswith(suffix):
                    groups[suffix].append(file_path)
                    break
            else:
                # Pas de suffixe reconnu, grouper par préfixe ou mettre dans "Other"
                groups['Other'].append(file_path)

        # Filtrer les groupes avec au moins 2 composants
        return {name: files for name, files in groups.items() if len(files) >= 2}

    def extract_tailwind_classes(self, content: str) -> List[str]:
        """Extrait toutes les classes Tailwind d'un fichier"""
        classes = []

        # Pattern pour className="..." ou className={`...`}
        patterns = [
            r'className="([^"]+)"',
            r'className={`([^`]+)`}',
            r'className=\{([^}]+)\}'
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, content):
                class_str = match.group(1)
                # Séparer les classes
                classes.extend(class_str.split())

        return classes

    def categorize_tailwind_classes(self, classes: List[str]) -> VisualPattern:
        """Catégorise les classes Tailwind par type"""
        pattern = VisualPattern(
            colors=Counter(),
            spacing=Counter(),
            typography=Counter(),
            borders=Counter(),
            shadows=Counter(),
            transitions=Counter(),
            states={
                'hover': Counter(),
                'focus': Counter(),
                'active': Counter(),
                'disabled': Counter()
            }
        )

        for cls in classes:
            # États (hover, focus, etc.)
            if ':' in cls:
                state, rest = cls.split(':', 1)
                if state in pattern.states:
                    pattern.states[state][rest] += 1
                continue

            # Colors (bg-, text-, border-color)
            if cls.startswith(('bg-', 'text-')) and not cls.startswith('text-'):
                pattern.colors[cls] += 1
            elif cls.startswith('text-') and any(c in cls for c in ['gray', 'blue', 'red', 'green', 'yellow', 'indigo', 'purple', 'pink', 'black', 'white']):
                pattern.colors[cls] += 1

            # Spacing (padding, margin)
            elif cls.startswith(('p-', 'px-', 'py-', 'pt-', 'pb-', 'pl-', 'pr-', 'm-', 'mx-', 'my-', 'mt-', 'mb-', 'ml-', 'mr-', 'gap-', 'space-')):
                pattern.spacing[cls] += 1

            # Typography
            elif cls.startswith(('text-', 'font-', 'leading-', 'tracking-')):
                pattern.typography[cls] += 1

            # Borders
            elif cls.startswith(('border', 'rounded')):
                pattern.borders[cls] += 1

            # Shadows
            elif cls.startswith('shadow'):
                pattern.shadows[cls] += 1

            # Transitions
            elif cls.startswith('transition'):
                pattern.transitions[cls] += 1

        return pattern

    def calculate_standard_pattern(self, patterns: List[VisualPattern]) -> Dict[str, Any]:
        """Calcule le pattern standard à partir des observations"""
        standard = {}

        # Agréger tous les patterns
        all_colors = Counter()
        all_spacing = Counter()
        all_typography = Counter()
        all_borders = Counter()
        all_shadows = Counter()
        all_transitions = Counter()
        all_states = {state: Counter() for state in ['hover', 'focus', 'active', 'disabled']}

        for pattern in patterns:
            all_colors.update(pattern.colors)
            all_spacing.update(pattern.spacing)
            all_typography.update(pattern.typography)
            all_borders.update(pattern.borders)
            all_shadows.update(pattern.shadows)
            all_transitions.update(pattern.transitions)
            for state in all_states:
                all_states[state].update(pattern.states[state])

        # Trouver les valeurs les plus communes (standards)
        def get_most_common(counter: Counter, top_n: int = 3) -> List[Tuple[str, int]]:
            return counter.most_common(top_n)

        standard['colors'] = get_most_common(all_colors, 5)
        standard['spacing'] = get_most_common(all_spacing, 5)
        standard['typography'] = get_most_common(all_typography, 3)
        standard['borders'] = get_most_common(all_borders, 3)
        standard['shadows'] = get_most_common(all_shadows, 2)
        standard['transitions'] = get_most_common(all_transitions, 2)
        standard['states'] = {state: get_most_common(counter, 3) for state, counter in all_states.items()}

        return standard

    def detect_deviations(self, group: ComponentGroup, file_path: Path, pattern: VisualPattern):
        """Détecte les déviations par rapport au pattern standard"""
        try:
            content = read_file_content_with_fallback_encoding(file_path)
            if not content:
                return
        except:
            return

        standard = group.standard_pattern

        # Vérifier les couleurs
        if 'colors' in standard:
            standard_colors = [cls for cls, count in standard['colors'][:3]]
            file_colors = list(pattern.colors.keys())

            for color in file_colors:
                # Si une couleur n'est pas dans le top 3 standard
                if color not in standard_colors and pattern.colors[color] > 2:
                    # Trouver la ligne
                    for i, line in enumerate(content.split('\n'), 1):
                        if color in line:
                            self.issues.append(ConsistencyIssue(
                                file_path=str(file_path.relative_to(self.project_path)),
                                line_number=i,
                                severity="minor",
                                issue_type="inconsistent_color",
                                category="colors",
                                code_snippet=line.strip()[:100],
                                description=f"Couleur '{color}' non standard pour ce groupe",
                                solution=f"Utiliser une couleur standard: {', '.join(standard_colors)}",
                                standard_value=standard_colors[0] if standard_colors else "",
                                actual_value=color,
                                auto_fixable=True,
                                confidence=75.0
                            ))
                            break

        # Vérifier les spacings
        if 'spacing' in standard:
            standard_spacing = [cls for cls, count in standard['spacing'][:3]]
            file_spacing = list(pattern.spacing.keys())

            # Détecter les espacements incohérents
            spacing_types = defaultdict(list)
            for sp in file_spacing:
                # Grouper par type (p-, px-, py-, etc.)
                prefix = sp.split('-')[0]
                spacing_types[prefix].append(sp)

            for sp_type, spacings in spacing_types.items():
                # Si plusieurs valeurs différentes pour le même type
                if len(set(spacings)) > 2:
                    for sp in spacings:
                        if sp not in standard_spacing:
                            for i, line in enumerate(content.split('\n'), 1):
                                if sp in line and 'className' in line:
                                    self.issues.append(ConsistencyIssue(
                                        file_path=str(file_path.relative_to(self.project_path)),
                                        line_number=i,
                                        severity="minor",
                                        issue_type="inconsistent_spacing",
                                        category="spacing",
                                        code_snippet=line.strip()[:100],
                                        description=f"Espacement '{sp}' incohérent avec le groupe",
                                        solution=f"Standardiser avec: {standard_spacing[0] if standard_spacing else 'p-4'}",
                                        standard_value=standard_spacing[0] if standard_spacing else "",
                                        actual_value=sp,
                                        auto_fixable=True,
                                        confidence=70.0
                                    ))
                                    break

        # Vérifier les hover states
        if 'states' in standard and 'hover' in standard['states']:
            standard_hovers = [cls for cls, count in standard['states']['hover'][:2]]
            file_hovers = list(pattern.states['hover'].keys())

            # Si le composant n'a pas de hover state mais le groupe en a
            if len(file_hovers) == 0 and len(standard_hovers) > 0:
                self.issues.append(ConsistencyIssue(
                    file_path=str(file_path.relative_to(self.project_path)),
                    line_number=1,
                    severity="important",
                    issue_type="missing_hover_state",
                    category="states",
                    code_snippet="",
                    description=f"Hover state manquant (standard du groupe: {standard_hovers[0]})",
                    solution=f"Ajouter hover:{standard_hovers[0]} aux éléments interactifs",
                    standard_value=standard_hovers[0] if standard_hovers else "",
                    actual_value="(absent)",
                    auto_fixable=False,
                    confidence=80.0
                ))

    def analyze_component_group(self, group_name: str, files: List[Path]) -> ComponentGroup:
        """Analyse un groupe de composants similaires"""
        patterns = []

        print(f"   Groupe '{group_name}' : {len(files)} composant(s)")

        for file_path in files:
            try:
                content = read_file_content_with_fallback_encoding(file_path)
                if not content:
                    continue

                classes = self.extract_tailwind_classes(content)
                pattern = self.categorize_tailwind_classes(classes)
                patterns.append(pattern)

            except Exception as e:
                print(f"      ⚠️  Erreur {file_path.name}: {e}")

        # Calculer le pattern standard du groupe
        standard_pattern = self.calculate_standard_pattern(patterns)

        # Créer le groupe
        group = ComponentGroup(
            name=group_name,
            components=[str(f.relative_to(self.project_path)) for f in files],
            patterns={'patterns': Counter()},  # Simplification
            standard_pattern=standard_pattern
        )

        # Détecter les déviations
        for file_path, pattern in zip(files, patterns):
            self.detect_deviations(group, file_path, pattern)

        return group

    def categorize_issues(self) -> Dict[str, List[ConsistencyIssue]]:
        """Catégorise les issues par niveau de confiance"""
        return {
            "auto_fix": [i for i in self.issues if i.auto_fixable and i.confidence >= 90],
            "recommend": [i for i in self.issues if i.confidence >= 70 and i.confidence < 90],
            "suggest": [i for i in self.issues if i.confidence >= 50 and i.confidence < 70],
            "ask": [i for i in self.issues if i.confidence < 50]
        }

    def generate_report(self) -> str:
        """Génère le rapport d'analyse"""
        categorized = self.categorize_issues()

        # Grouper par fichier
        issues_by_file = defaultdict(list)
        for issue in self.issues:
            issues_by_file[issue.file_path].append(issue)

        # Grouper par catégorie
        issues_by_category = defaultdict(list)
        for issue in self.issues:
            issues_by_category[issue.category].append(issue)

        report = f"""# Component Consistency Checker - Rapport

**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Projet** : {self.project_path.name}
**Stack** : {self.stack['framework']} + {self.stack['css_framework']}
**Scan** : #{self.project_memory.get('scan_count', 0) + 1}

---

## 📊 Vue d'ensemble

**Groupes de composants** : {len(self.component_groups)}
**Composants analysés** : {sum(len(g.components) for g in self.component_groups)}
**Incohérences détectées** : {len(self.issues)}

---

## 🎨 Groupes de composants

"""

        for group in self.component_groups:
            report += f"""
### {group.name} ({len(group.components)} composants)

**Composants** :
"""
            for comp in group.components:
                report += f"- {comp}\n"

            if 'colors' in group.standard_pattern:
                report += f"\n**Couleurs standard** : {', '.join([cls for cls, _ in group.standard_pattern['colors'][:3]])}\n"
            if 'spacing' in group.standard_pattern:
                report += f"**Espacements standard** : {', '.join([cls for cls, _ in group.standard_pattern['spacing'][:3]])}\n"

        report += f"""
---

## 🔍 Incohérences par catégorie

"""

        for category, issues in sorted(issues_by_category.items(), key=lambda x: -len(x[1])):
            report += f"""
### {category.title()} ({len(issues)} incohérences)

"""
            for issue in issues[:5]:
                report += f"- **{issue.file_path}:{issue.line_number}** - {issue.description}\n"

            if len(issues) > 5:
                report += f"  ... et {len(issues) - 5} autres\n"

        report += f"""
---

## 🎯 Corrections recommandées

### ✅ Corrections possibles ({len(categorized['recommend'])} issues)

"""

        for issue in categorized['recommend'][:10]:
            report += f"""
**{issue.file_path}:{issue.line_number}**
- Problème : {issue.description}
- Solution : {issue.solution}
- Confiance : {issue.confidence}%
"""

        report += f"""
---

## 📈 Statistiques

"""

        for category, issues in sorted(issues_by_category.items(), key=lambda x: -len(x[1])):
            report += f"- **{category.title()}** : {len(issues)}\n"

        report += f"""
---

**Rapport généré par Component Consistency Checker V2**
"""

        return report

    def run(self):
        """Exécute l'analyse complète"""
        print("\n🔍 Recherche des composants...")
        component_files = self.find_component_files()
        print(f"✅ {len(component_files)} composant(s) trouvé(s)\n")

        print("📊 Regroupement des composants similaires...")
        grouped_files = self.group_similar_components(component_files)
        print(f"✅ {len(grouped_files)} groupe(s) identifié(s)\n")

        print("🎨 Analyse des patterns visuels...\n")
        for group_name, files in grouped_files.items():
            group = self.analyze_component_group(group_name, files)
            self.component_groups.append(group)

        print(f"\n✅ Analyse terminée !")
        print(f"   Incohérences : {len(self.issues)}")

        # Générer rapport
        report = self.generate_report()

        # Sauvegarder rapport
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)

        report_filename = f"consistency-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        report_path = reports_dir / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n📄 Rapport : {report_path}")

        # Mettre à jour et sauvegarder la mémoire
        self.project_memory["scan_count"] += 1
        self.project_memory["last_scan"] = datetime.now().isoformat()
        self.save_project_memory()

        print(f"💾 Mémoire sauvegardée")

        # Afficher résumé
        categorized = self.categorize_issues()
        print(f"\n📊 Résumé :")
        print(f"   - Corrections possibles : {len(categorized['recommend'])}")
        print(f"   - Suggestions : {len(categorized['suggest'])}")
        print(f"   - À valider : {len(categorized['ask'])}")

        return report

def main():
    """Point d'entrée principal"""
    import sys

    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = "."

    checker = ConsistencyChecker(project_path)
    checker.run()

if __name__ == "__main__":
    main()
