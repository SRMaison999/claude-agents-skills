#!/usr/bin/env python3
"""
Dead Code Cleaner V2 - Learning Edition
Agent intelligent de nettoyage de code mort avec apprentissage continu

SÉCURITÉ : Ne touche JAMAIS aux exports, routes ou configs

Usage: python dead_code_cleaner_v2.py [project_path]
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
from collections import defaultdict, Counter

@dataclass
class DeadCodeIssue:
    """Représente du code mort détecté"""
    file_path: str
    line_number: int
    severity: str  # "critical", "important", "minor"
    issue_type: str
    code_snippet: str
    description: str
    solution: str
    auto_fixable: bool
    confidence: float = 0.0

@dataclass
class FileAnalysis:
    """Analyse d'un fichier"""
    file_path: str
    imports: List[str]
    exports: List[str]
    functions: List[str]
    variables: List[str]
    components: List[str]
    console_logs: List[int]  # Line numbers
    commented_code: List[int]  # Line numbers
    issues: List[DeadCodeIssue] = field(default_factory=list)

class DeadCodeCleaner:
    """
    Agent intelligent de nettoyage de code mort avec apprentissage continu
    """

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.files_analysis: Dict[str, FileAnalysis] = {}
        self.issues: List[DeadCodeIssue] = []

        # Auto-détection du stack
        self.stack = self.detect_project_stack()

        # Chargement de la mémoire
        project_hash = self.get_project_hash()
        self.project_memory = self.load_project_memory(project_hash)
        self.project_hash = project_hash

        # Graphe d'imports (pour détecter code mort)
        self.import_graph: Dict[str, Set[str]] = defaultdict(set)

        self.print_header()

    def print_header(self):
        """Affiche l'en-tête de l'analyse"""
        print("="*70)
        print("🧹 Dead Code Cleaner V2 - Learning Edition")
        print("="*70)
        print(f"📁 Projet : {self.project_path.name}")
        print(f"🔧 Stack : {self.stack['framework']}")
        print(f"🧠 Analyse #{self.project_memory.get('scan_count', 0) + 1}")

        scan_count = self.project_memory.get('scan_count', 0)
        if scan_count == 0:
            print(f"🌱 État : DÉCOUVERTE (mode apprentissage)")
        elif scan_count < 5:
            print(f"🌿 État : CROISSANCE (confiance en construction)")
        elif scan_count < 10:
            print(f"🌳 État : MATURITÉ (suppressions partiellement autonomes)")
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
            "language": "JavaScript"
        }

        if not package_json_path.exists():
            return stack

        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)

            deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}

            if 'react' in deps:
                stack['framework'] = 'React'
            elif 'vue' in deps:
                stack['framework'] = 'Vue'
            elif '@angular/core' in deps:
                stack['framework'] = 'Angular'

            if 'typescript' in deps:
                stack['language'] = 'TypeScript'

        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture de package.json: {e}")

        return stack

    def load_project_memory(self, project_hash: str) -> Dict[str, Any]:
        """Charge la mémoire spécifique du projet"""
        brain_dir = Path.home() / ".claude-agents" / "brain" / "dead-code-cleaner" / project_hash
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
            "safe_to_remove": [],
            "never_remove": [],
            "learned_patterns": {}
        }

    def save_project_memory(self):
        """Sauvegarde la mémoire du projet"""
        brain_dir = Path.home() / ".claude-agents" / "brain" / "dead-code-cleaner" / self.project_hash
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

    def extract_imports(self, content: str) -> List[str]:
        """Extrait tous les imports d'un fichier"""
        imports = []

        # import X from 'module'
        pattern1 = r"import\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]"
        for match in re.finditer(pattern1, content):
            imports.append(match.group(1))

        # import { X, Y } from 'module'
        pattern2 = r"import\s*\{([^}]+)\}\s*from\s+['\"]([^'\"]+)['\"]"
        for match in re.finditer(pattern2, content):
            items = match.group(1).split(',')
            for item in items:
                name = item.strip().split(' as ')[0].strip()
                imports.append(name)

        # import * as X from 'module'
        pattern3 = r"import\s+\*\s+as\s+(\w+)\s+from"
        for match in re.finditer(pattern3, content):
            imports.append(match.group(1))

        return imports

    def extract_exports(self, content: str) -> List[str]:
        """Extrait tous les exports d'un fichier"""
        exports = []

        # export const X
        pattern1 = r"export\s+(?:const|let|var|function|class)\s+(\w+)"
        for match in re.finditer(pattern1, content):
            exports.append(match.group(1))

        # export { X, Y }
        pattern2 = r"export\s*\{([^}]+)\}"
        for match in re.finditer(pattern2, content):
            items = match.group(1).split(',')
            for item in items:
                name = item.strip().split(' as ')[0].strip()
                exports.append(name)

        # export default X
        pattern3 = r"export\s+default\s+(\w+)"
        for match in re.finditer(pattern3, content):
            exports.append(match.group(1))

        return exports

    def extract_functions(self, content: str) -> List[str]:
        """Extrait toutes les fonctions déclarées"""
        functions = []

        # function name()
        pattern1 = r"function\s+(\w+)\s*\("
        for match in re.finditer(pattern1, content):
            functions.append(match.group(1))

        # const name = function()
        pattern2 = r"const\s+(\w+)\s*=\s*function"
        for match in re.finditer(pattern2, content):
            functions.append(match.group(1))

        # const name = () =>
        pattern3 = r"const\s+(\w+)\s*=\s*\([^)]*\)\s*=>"
        for match in re.finditer(pattern3, content):
            functions.append(match.group(1))

        return functions

    def extract_variables(self, content: str) -> List[str]:
        """Extrait toutes les variables déclarées"""
        variables = []

        # const/let/var name =
        pattern = r"(?:const|let|var)\s+(\w+)\s*="
        for match in re.finditer(pattern, content):
            var_name = match.group(1)
            # Exclure les fonctions (déjà extraites)
            if not re.search(rf"{var_name}\s*=\s*(?:function|\([^)]*\)\s*=>)", content):
                variables.append(var_name)

        return variables

    def extract_components(self, content: str) -> List[str]:
        """Extrait tous les composants React"""
        components = []

        # Composants en PascalCase (React convention)
        # const ComponentName = () =>
        pattern1 = r"(?:const|function)\s+([A-Z]\w+)\s*=?\s*(?:\([^)]*\))?\s*(?:=>|{)"
        for match in re.finditer(pattern1, content):
            components.append(match.group(1))

        return components

    def find_console_logs(self, content: str) -> List[int]:
        """Trouve toutes les lignes avec console.log"""
        lines_with_console = []

        for i, line in enumerate(content.split('\n'), 1):
            if 'console.log' in line or 'console.warn' in line or 'console.error' in line:
                # Ignorer si dans un commentaire
                stripped = line.strip()
                if not (stripped.startswith('//') or stripped.startswith('/*')):
                    lines_with_console.append(i)

        return lines_with_console

    def find_commented_code(self, content: str) -> List[int]:
        """Trouve le code commenté (potentiellement obsolète)"""
        commented_lines = []
        lines = content.split('\n')

        in_block_comment = False
        block_start = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Bloc de commentaires
            if '/*' in stripped and '*/' not in stripped:
                in_block_comment = True
                block_start = i
            elif '*/' in stripped:
                in_block_comment = False
                # Si le bloc contient du code (détection basique)
                block_lines = lines[block_start-1:i]
                block_text = '\n'.join(block_lines)
                if any(keyword in block_text for keyword in ['const ', 'let ', 'var ', 'function ', 'return ', '{']):
                    commented_lines.append(block_start)

            # Commentaire de ligne avec du code
            if stripped.startswith('//'):
                # Détecter si c'est du code commenté vs un vrai commentaire
                code_line = stripped[2:].strip()
                if any(keyword in code_line for keyword in ['const ', 'let ', 'var ', 'function ', 'return ', '<', '{']):
                    commented_lines.append(i)

        return commented_lines

    def analyze_file(self, file_path: Path) -> FileAnalysis:
        """Analyse complète d'un fichier"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return FileAnalysis(
                file_path=str(file_path.relative_to(self.project_path)),
                imports=[], exports=[], functions=[],
                variables=[], components=[], console_logs=[], commented_code=[]
            )

        analysis = FileAnalysis(
            file_path=str(file_path.relative_to(self.project_path)),
            imports=self.extract_imports(content),
            exports=self.extract_exports(content),
            functions=self.extract_functions(content),
            variables=self.extract_variables(content),
            components=self.extract_components(content),
            console_logs=self.find_console_logs(content),
            commented_code=self.find_commented_code(content)
        )

        # Analyser les imports non utilisés
        for imported in analysis.imports:
            # Vérifier si utilisé dans le fichier
            # Pattern simple : chercher le nom dans le code (hors import line)
            lines = content.split('\n')
            used = False

            for line in lines:
                if line.strip().startswith('import'):
                    continue
                if imported in line:
                    used = True
                    break

            if not used:
                analysis.issues.append(DeadCodeIssue(
                    file_path=analysis.file_path,
                    line_number=1,
                    severity="minor",
                    issue_type="unused_import",
                    code_snippet=f"import {imported}",
                    description=f"Import '{imported}' non utilisé",
                    solution=f"Supprimer l'import de '{imported}'",
                    auto_fixable=True,
                    confidence=95.0
                ))

        # Analyser console.log
        for line_num in analysis.console_logs:
            analysis.issues.append(DeadCodeIssue(
                file_path=analysis.file_path,
                line_number=line_num,
                severity="minor",
                issue_type="console_log",
                code_snippet="console.log(...)",
                description=f"Console.log oublié (ligne {line_num})",
                solution="Supprimer ou remplacer par un logger approprié",
                auto_fixable=True,
                confidence=100.0
            ))

        # Analyser code commenté
        for line_num in analysis.commented_code:
            analysis.issues.append(DeadCodeIssue(
                file_path=analysis.file_path,
                line_number=line_num,
                severity="minor",
                issue_type="commented_code",
                code_snippet="// code commented",
                description=f"Code commenté (potentiellement obsolète) ligne {line_num}",
                solution="Supprimer si obsolète, sinon décommenter",
                auto_fixable=False,
                confidence=70.0
            ))

        return analysis

    def build_import_graph(self):
        """Construit le graphe des dépendances entre fichiers"""
        for file_path, analysis in self.files_analysis.items():
            for export in analysis.exports:
                # Chercher qui importe cet export
                for other_file, other_analysis in self.files_analysis.items():
                    if file_path == other_file:
                        continue
                    if export in other_analysis.imports:
                        self.import_graph[file_path].add(other_file)

    def find_unused_components(self):
        """Trouve les composants jamais importés ailleurs"""
        all_components = set()
        all_imports = set()

        for analysis in self.files_analysis.values():
            all_components.update(analysis.components)
            all_imports.update(analysis.imports)

        # Composants jamais importés
        unused_components = all_components - all_imports

        for comp_name in unused_components:
            # Trouver dans quel fichier il est défini
            for file_path, analysis in self.files_analysis.items():
                if comp_name in analysis.components:
                    # Vérifier qu'il n'est pas exporté (important!)
                    if comp_name not in analysis.exports:
                        self.issues.append(DeadCodeIssue(
                            file_path=file_path,
                            line_number=1,
                            severity="minor",
                            issue_type="unused_component",
                            code_snippet=f"const {comp_name} = ...",
                            description=f"Composant '{comp_name}' jamais importé/utilisé ailleurs",
                            solution=f"Supprimer si inutile ou exporter si réutilisable",
                            auto_fixable=False,
                            confidence=60.0
                        ))

    def categorize_issues(self) -> Dict[str, List[DeadCodeIssue]]:
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

        # Compter par type
        issue_types = defaultdict(int)
        for issue in self.issues:
            issue_types[issue.issue_type] += 1

        report = f"""# Dead Code Cleaner - Rapport d'analyse

**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Projet** : {self.project_path.name}
**Stack** : {self.stack['framework']} ({self.stack['language']})
**Scan** : #{self.project_memory.get('scan_count', 0) + 1}

---

## 📊 Vue d'ensemble

**Fichiers analysés** : {len(self.files_analysis)}
**Issues totales** : {len(self.issues)}

### Par type
"""

        for issue_type, count in sorted(issue_types.items(), key=lambda x: -x[1]):
            report += f"- {issue_type.replace('_', ' ').title()} : {count}\n"

        report += f"""
---

## 🎯 Nettoyage recommandé

### ✅ Suppressions automatiques ({len(categorized['auto_fix'])} issues)
Confiance ≥90% - Peut être supprimé automatiquement

"""

        auto_by_type = defaultdict(list)
        for issue in categorized['auto_fix']:
            auto_by_type[issue.issue_type].append(issue)

        for issue_type, issues in auto_by_type.items():
            report += f"""
#### {issue_type.replace('_', ' ').title()} ({len(issues)})

"""
            for issue in issues[:5]:  # Top 5
                report += f"- {issue.file_path}:{issue.line_number} - {issue.description}\n"

            if len(issues) > 5:
                report += f"  ... et {len(issues) - 5} autres\n"

        report += f"""
---

## 📁 Issues par fichier (Top 10)

"""

        # Top 10 fichiers avec le plus d'issues
        sorted_files = sorted(issues_by_file.items(), key=lambda x: -len(x[1]))

        for file_path, file_issues in sorted_files[:10]:
            report += f"""
### {file_path} ({len(file_issues)} issues)

"""

            for issue in file_issues[:5]:
                report += f"- Ligne {issue.line_number}: {issue.description}\n"

        report += f"""
---

## 📈 Statistiques

- **Imports inutilisés** : {issue_types.get('unused_import', 0)}
- **Console.log** : {issue_types.get('console_log', 0)}
- **Code commenté** : {issue_types.get('commented_code', 0)}
- **Composants inutilisés** : {issue_types.get('unused_component', 0)}

---

## 🔒 Sécurité

**IMPORTANT** : Cet agent ne touche JAMAIS à :
- Exports (fichiers qui exportent des modules)
- Routes (configurations de routing)
- Configs (fichiers de configuration)

**Validation manuelle recommandée** pour :
- Composants marqués comme inutilisés (peuvent être utilisés dynamiquement)
- Code commenté (peut contenir des notes importantes)

---

**Rapport généré par Dead Code Cleaner V2**
"""

        return report

    def run(self):
        """Exécute l'analyse complète"""
        print("\n🔍 Recherche des fichiers source...")
        source_files = self.find_source_files()
        print(f"✅ {len(source_files)} fichiers trouvés\n")

        print("🧹 Analyse en cours...")
        for i, file_path in enumerate(source_files, 1):
            if i % 10 == 0:
                print(f"   Progression : {i}/{len(source_files)}")

            analysis = self.analyze_file(file_path)
            self.files_analysis[str(file_path.relative_to(self.project_path))] = analysis
            self.issues.extend(analysis.issues)

        print(f"✅ Analyse terminée !\n")

        # Analyses avancées
        print("📊 Construction du graphe de dépendances...")
        self.build_import_graph()

        print("🔍 Recherche de composants inutilisés...")
        self.find_unused_components()

        # Générer rapport
        report = self.generate_report()

        # Sauvegarder rapport
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)

        report_filename = f"dead-code-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        report_path = reports_dir / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ Nettoyage terminé !")
        print(f"📄 Rapport : {report_path}")

        # Mettre à jour et sauvegarder la mémoire
        self.project_memory["scan_count"] += 1
        self.project_memory["last_scan"] = datetime.now().isoformat()
        self.save_project_memory()

        print(f"💾 Mémoire sauvegardée")

        # Afficher résumé
        categorized = self.categorize_issues()
        print(f"\n📊 Résumé :")
        print(f"   Issues : {len(self.issues)}")
        print(f"   - Suppressions auto : {len(categorized['auto_fix'])}")
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

    cleaner = DeadCodeCleaner(project_path)
    cleaner.run()

if __name__ == "__main__":
    main()
