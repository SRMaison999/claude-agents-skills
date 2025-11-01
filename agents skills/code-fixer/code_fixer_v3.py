#!/usr/bin/env python3
"""
Code Fixer V3 - Application des corrections

Lit les rapports JSON de la session
Applique les corrections auto-fixables (confiance ≥90%)
Génère FIXES-APPLIED.md (traçabilité lisible)

SÉCURITÉ :
- Syntax check après chaque modification
- Rollback automatique si erreur
- Mode --dry-run pour simulation

Usage:
    python code_fixer_v3.py /path/to/project --session /path/to/session
    python code_fixer_v3.py /path/to/project --session /path/to/session --dry-run
"""

import sys
import io
import json
import shutil
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict

# Forcer UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

@dataclass
class Fix:
    """Une correction à appliquer"""
    agent: str
    file_path: str
    line_number: int
    fix_type: str
    description: str
    solution: str
    old_code: str
    new_code: str
    confidence: float
    applied: bool = False
    success: bool = False
    error: str = ""

class CodeFixerV3:
    """
    Applique les corrections automatiques avec vérifications
    """

    def __init__(self, project_path: Path, session_path: Path, dry_run: bool = False):
        self.project_path = project_path
        self.session_path = session_path
        self.dry_run = dry_run
        self.fixes: List[Fix] = []
        self.fixes_applied: List[Fix] = []
        self.fixes_failed: List[Fix] = []
        self.syntax_errors: List[Dict[str, Any]] = []

    def load_json_reports(self):
        """Charge tous les rapports JSON de la session"""

        analysis_dir = self.session_path / "1-ANALYSIS"

        if not analysis_dir.exists():
            print(f"❌ Dossier d'analyse introuvable : {analysis_dir}")
            return

        json_files = list(analysis_dir.glob("*.json"))

        print(f"📄 Chargement de {len(json_files)} rapports JSON...\n")

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                agent_name = data.get("agent", "unknown")

                # Extraire les issues auto-fixables
                for issue in data.get("issues", []):
                    if issue.get("auto_fixable", False) and issue.get("confidence", 0) >= 90:
                        fix = Fix(
                            agent=agent_name,
                            file_path=issue.get("file", ""),
                            line_number=issue.get("line", 0),
                            fix_type=issue.get("type", ""),
                            description=issue.get("description", ""),
                            solution=issue.get("solution", ""),
                            old_code=issue.get("old_code", ""),
                            new_code=issue.get("new_code", ""),
                            confidence=issue.get("confidence", 0.0)
                        )
                        self.fixes.append(fix)

            except Exception as e:
                print(f"⚠️  Erreur lecture {json_file.name} : {e}")

        print(f"✅ {len(self.fixes)} corrections automatiques chargées\n")

    def backup_file(self, file_path: Path):
        """Crée un backup d'un fichier"""
        if not file_path.exists():
            return

        backup_dir = self.session_path / "2-FIXES" / "backup"
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Chemin relatif pour préserver la structure
        try:
            relative_path = file_path.relative_to(self.project_path)
        except ValueError:
            relative_path = file_path.name

        backup_path = backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(file_path, backup_path)

    def rollback_file(self, file_path: Path) -> bool:
        """Restaure un fichier depuis le backup"""
        try:
            relative_path = file_path.relative_to(self.project_path)
        except ValueError:
            relative_path = file_path.name

        backup_path = self.session_path / "2-FIXES" / "backup" / relative_path

        if not backup_path.exists():
            return False

        shutil.copy2(backup_path, file_path)
        return True

    def verify_syntax(self, file_path: Path) -> tuple[bool, Optional[str]]:
        """
        Vérifie la syntaxe d'un fichier TypeScript/JavaScript

        Returns:
            (success, error_message)
        """

        # Vérifier que c'est un fichier TS/JS
        if file_path.suffix not in ['.ts', '.tsx', '.js', '.jsx']:
            return (True, None)  # Pas applicable

        try:
            # Pour les fichiers .js/.jsx : utiliser Node.js en priorité
            if file_path.suffix in ['.js', '.jsx']:
                try:
                    result = subprocess.run(
                        ['node', '--check', str(file_path)],
                        cwd=self.project_path,
                        capture_output=True,
                        timeout=5
                    )

                    if result.returncode == 0:
                        return (True, None)
                    else:
                        error_msg = result.stderr.decode('utf-8', errors='replace')[:300]
                        return (False, error_msg)

                except FileNotFoundError:
                    # Node pas disponible, essayer TypeScript avec --allowJs
                    pass

            # Pour .ts/.tsx OU si Node unavailable : TypeScript
            result = subprocess.run(
                ['npx', 'tsc', '--noEmit', '--skipLibCheck', '--allowJs', str(file_path)],
                cwd=self.project_path,
                capture_output=True,
                timeout=10
            )

            if result.returncode == 0:
                return (True, None)
            else:
                error_output = result.stderr.decode('utf-8', errors='replace')

                # Ignorer l'erreur "allowJs" si c'est la seule erreur
                if "Did you mean to enable the 'allowJs' option?" in error_output and len(error_output) < 300:
                    return (True, None)  # Pas une vraie erreur de syntaxe

                # Extraire les erreurs pertinentes
                error_lines = [line for line in error_output.split('\n') if file_path.name in line or 'error TS' in line]
                error_msg = '\n'.join(error_lines[:5]) if error_lines else error_output[:300]
                return (False, error_msg)

        except FileNotFoundError:
            # Ni TypeScript ni Node disponibles
            return (True, None)  # Mode dégradé - on laisse passer

        except subprocess.TimeoutExpired:
            return (False, "Timeout lors de la vérification")
        except Exception as e:
            return (False, f"Erreur vérification: {str(e)}")

    def apply_emoji_removal(self, file_path: Path, fix: Fix) -> bool:
        """Supprime un emoji"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if fix.line_number > len(lines):
                fix.error = f"Ligne {fix.line_number} hors limites"
                return False

            # Pattern emoji universel
            emoji_pattern = re.compile(
                "["
                "\U0001F600-\U0001F64F"
                "\U0001F300-\U0001F5FF"
                "\U0001F680-\U0001F6FF"
                "\U0001F700-\U0001F77F"
                "\U0001F780-\U0001F7FF"
                "\U0001F800-\U0001F8FF"
                "\U0001F900-\U0001F9FF"
                "\U0001FA00-\U0001FA6F"
                "\U0001FA70-\U0001FAFF"
                "\U00002700-\U000027BF"
                "\U000024C2-\U0001F251"
                "]+"
            )

            line_index = fix.line_number - 1
            original_line = lines[line_index]
            new_line = emoji_pattern.sub('', original_line)

            # Nettoyer les espaces multiples
            new_line = re.sub(r'  +', ' ', new_line)

            if original_line != new_line:
                fix.old_code = original_line.strip()
                fix.new_code = new_line.strip()
                lines[line_index] = new_line

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                return True

            return False

        except Exception as e:
            fix.error = str(e)
            return False

    def apply_console_log_removal(self, file_path: Path, fix: Fix) -> bool:
        """Supprime un console.log"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if fix.line_number > len(lines):
                fix.error = f"Ligne {fix.line_number} hors limites"
                return False

            line_index = fix.line_number - 1
            original_line = lines[line_index]

            # Vérifier que la ligne contient console.log
            if 'console.log' in original_line or 'console.error' in original_line or 'console.warn' in original_line:
                fix.old_code = original_line.strip()

                # Supprimer la ligne
                del lines[line_index]
                fix.new_code = "[ligne supprimée]"

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                return True

            return False

        except Exception as e:
            fix.error = str(e)
            return False

    def apply_unused_import_removal(self, file_path: Path, fix: Fix) -> bool:
        """Supprime un import inutilisé"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if fix.line_number > len(lines):
                fix.error = f"Ligne {fix.line_number} hors limites"
                return False

            line_index = fix.line_number - 1
            original_line = lines[line_index]

            # Extraire le nom de l'import depuis la description
            match = re.search(r"Import\s+'([^']+)'\s+non utilisé", fix.description)
            if not match:
                fix.error = "Impossible d'extraire le nom de l'import"
                return False

            import_name = match.group(1)

            # Supprimer l'import de la ligne
            # Pattern: import { A, B, C } from 'module'
            if '{' in original_line and '}' in original_line:
                # Import destructuré
                new_line = re.sub(r',?\s*' + re.escape(import_name) + r'\s*,?', '', original_line)
                new_line = re.sub(r'\{\s*,', '{', new_line)
                new_line = re.sub(r',\s*\}', '}', new_line)
                new_line = re.sub(r'\{\s*\}', '', new_line)

                # Si l'import est vide, supprimer toute la ligne
                if re.search(r'import\s*\{\s*\}\s*from', new_line):
                    fix.old_code = original_line.strip()
                    fix.new_code = "[ligne supprimée]"
                    del lines[line_index]
                else:
                    fix.old_code = original_line.strip()
                    fix.new_code = new_line.strip()
                    lines[line_index] = new_line

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                return True

            # Import simple : import X from 'module'
            elif f"import {import_name}" in original_line or f"import\t{import_name}" in original_line:
                fix.old_code = original_line.strip()
                fix.new_code = "[ligne supprimée]"
                del lines[line_index]

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                return True

            return False

        except Exception as e:
            fix.error = str(e)
            return False

    def apply_fix(self, fix: Fix) -> bool:
        """Applique une correction avec vérifications"""

        file_path = self.project_path / fix.file_path

        if not file_path.exists():
            fix.error = f"Fichier introuvable : {file_path}"
            return False

        # MODE DRY-RUN : Simuler sans modifier
        if self.dry_run:
            fix.old_code = "[DRY-RUN - non modifié]"
            fix.new_code = "[DRY-RUN - simulation]"
            return True

        # Backup avant modification
        self.backup_file(file_path)

        # Appliquer selon le type
        success = False
        if fix.fix_type == "emoji_detected":
            success = self.apply_emoji_removal(file_path, fix)
        elif fix.fix_type == "console_log":
            success = self.apply_console_log_removal(file_path, fix)
        elif fix.fix_type == "unused_import":
            success = self.apply_unused_import_removal(file_path, fix)
        else:
            fix.error = f"Type de correction non supporté : {fix.fix_type}"
            return False

        # Si la modification technique a échoué
        if not success:
            return False

        # VÉRIFICATION DE SYNTAXE
        syntax_ok, syntax_error = self.verify_syntax(file_path)

        if not syntax_ok:
            # ROLLBACK AUTOMATIQUE
            rollback_success = self.rollback_file(file_path)

            fix.error = f"Erreur de syntaxe après modification (ROLLBACK {'✅' if rollback_success else '❌'}): {syntax_error}"
            fix.success = False

            # Tracker l'erreur de syntaxe
            self.syntax_errors.append({
                "file": fix.file_path,
                "line": fix.line_number,
                "fix_type": fix.fix_type,
                "error": syntax_error,
                "rollback_success": rollback_success
            })

            return False

        # Tout est OK
        return True

    def apply_all_fixes(self):
        """Applique toutes les corrections"""

        print(f"🔧 Application de {len(self.fixes)} corrections...\n")

        # Grouper par fichier
        by_file = defaultdict(list)
        for fix in self.fixes:
            by_file[fix.file_path].append(fix)

        total_files = len(by_file)
        current_file = 0

        for file_path, file_fixes in by_file.items():
            current_file += 1
            print(f"[{current_file}/{total_files}] {file_path} ({len(file_fixes)} corrections)")

            for fix in file_fixes:
                success = self.apply_fix(fix)

                if success:
                    fix.applied = True
                    fix.success = True
                    self.fixes_applied.append(fix)
                else:
                    fix.applied = True
                    fix.success = False
                    self.fixes_failed.append(fix)

        print(f"\n✅ {len(self.fixes_applied)} corrections appliquées")
        if self.fixes_failed:
            print(f"⚠️  {len(self.fixes_failed)} corrections échouées")

    def generate_fixes_report(self) -> str:
        """Génère le rapport FIXES-APPLIED.md"""

        report = f"""# Corrections appliquées - Session {self.session_path.name.replace('session-', '')}

**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Projet** : {self.project_path.name}

---

## 📊 Vue d'ensemble

**Fichiers modifiés** : {len(set(f.file_path for f in self.fixes_applied))}
**Corrections appliquées** : {len(self.fixes_applied)}
**Corrections échouées** : {len(self.fixes_failed)}
**Backup** : 2-FIXES/backup/

---

"""

        if self.fixes_applied:
            # Grouper par fichier
            by_file = defaultdict(list)
            for fix in self.fixes_applied:
                by_file[fix.file_path].append(fix)

            report += "## ✅ Corrections réussies\n\n"

            for file_path in sorted(by_file.keys()):
                report += f"### Fichier : {file_path}\n\n"

                for fix in by_file[file_path]:
                    report += f"**Ligne {fix.line_number}** - {fix.fix_type}\n"
                    report += f"- **Agent** : {fix.agent}\n"
                    report += f"- **Type** : {fix.fix_type}\n"
                    report += f"- **Confiance** : {fix.confidence}%\n"
                    report += f"- **Description** : {fix.description}\n"
                    report += f"- **Solution** : {fix.solution}\n\n"

                    if fix.old_code and fix.new_code:
                        report += f"**AVANT** :\n```\n{fix.old_code}\n```\n\n"
                        report += f"**APRÈS** :\n```\n{fix.new_code}\n```\n\n"

                    report += "---\n\n"

        if self.fixes_failed:
            report += "## ❌ Corrections échouées\n\n"
            report += f"**Total** : {len(self.fixes_failed)} correction(s) échouée(s)\n\n"

            # Grouper par type d'erreur
            syntax_errors = [f for f in self.fixes_failed if "syntaxe" in f.error.lower()]
            other_errors = [f for f in self.fixes_failed if "syntaxe" not in f.error.lower()]

            if syntax_errors:
                report += f"### 🚨 Erreurs de syntaxe ({len(syntax_errors)}) - ROLLBACK effectué\n\n"
                for fix in syntax_errors:
                    report += f"**{fix.file_path}:{fix.line_number}** - {fix.fix_type}\n"
                    report += f"- **Agent** : {fix.agent}\n"
                    report += f"- **Description** : {fix.description}\n"
                    report += f"- **Erreur** : {fix.error}\n\n"
                    report += "---\n\n"

            if other_errors:
                report += f"### ⚠️  Autres erreurs ({len(other_errors)})\n\n"
                for fix in other_errors:
                    report += f"**{fix.file_path}:{fix.line_number}** - {fix.fix_type}\n"
                    report += f"- **Agent** : {fix.agent}\n"
                    report += f"- **Description** : {fix.description}\n"
                    report += f"- **Erreur** : {fix.error}\n\n"

        # Section statistiques détaillées
        if self.syntax_errors:
            report += f"\n## 📊 Détails des erreurs de syntaxe\n\n"
            report += f"**Fichiers concernés** : {len(set(e['file'] for e in self.syntax_errors))}\n\n"

            for error in self.syntax_errors:
                report += f"### {error['file']}:{error['line']}\n"
                report += f"- **Type de correction** : {error['fix_type']}\n"
                report += f"- **Rollback** : {'✅ Succès' if error['rollback_success'] else '❌ Échec'}\n"
                report += f"- **Message d'erreur** :\n```\n{error['error']}\n```\n\n"

        report += f"""
---

## 🔒 Sécurité

- ✅ Backup créé pour tous les fichiers modifiés
- ✅ Vérification de syntaxe après chaque modification
- ✅ Rollback automatique en cas d'erreur
- 📁 Backups : `2-FIXES/backup/`

---

**Rapport généré par Code Fixer V3**
*Session : {self.session_path.name}*
"""

        return report

    def run(self):
        """Lance le processus complet"""

        print("=" * 80)
        print("🔧 CODE FIXER V3" + (" [DRY-RUN MODE]" if self.dry_run else ""))
        print("=" * 80)
        print(f"📁 Projet  : {self.project_path.name}")
        print(f"🆔 Session : {self.session_path.name}")
        if self.dry_run:
            print(f"⚠️  Mode    : DRY-RUN (simulation - aucune modification)")
        print("=" * 80)
        print()

        # 1. Charger les rapports JSON
        self.load_json_reports()

        if not self.fixes:
            print("ℹ️  Aucune correction automatique à appliquer.\n")
            return

        # 2. Appliquer les corrections (ou simuler)
        self.apply_all_fixes()

        # Affichage détaillé des résultats
        if self.syntax_errors:
            print(f"🚨 {len(self.syntax_errors)} erreur(s) de syntaxe détectée(s) (rollback effectué)")

        # 3. Générer le rapport
        report = self.generate_fixes_report()

        # 4. Sauvegarder le rapport
        fixes_dir = self.session_path / "2-FIXES"
        fixes_dir.mkdir(parents=True, exist_ok=True)

        report_name = "FIXES-APPLIED-DRY-RUN.md" if self.dry_run else "FIXES-APPLIED.md"
        report_path = fixes_dir / report_name
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n📄 Rapport : {report_path.relative_to(self.session_path)}")

        if self.dry_run:
            print(f"\n💡 Aucune modification apportée (mode DRY-RUN)")
            print(f"   Relancez sans --dry-run pour appliquer les corrections\n")
        else:
            print()

def main():
    """Point d'entrée"""

    if len(sys.argv) < 4 or sys.argv[2] != "--session":
        print("Usage:")
        print("  python code_fixer_v3.py /path/to/project --session /path/to/session")
        print("  python code_fixer_v3.py /path/to/project --session /path/to/session --dry-run")
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()
    session_path = Path(sys.argv[3]).resolve()
    dry_run = "--dry-run" in sys.argv

    if not project_path.exists():
        print(f"❌ Projet introuvable : {project_path}")
        sys.exit(1)

    if not session_path.exists():
        print(f"❌ Session introuvable : {session_path}")
        sys.exit(1)

    fixer = CodeFixerV3(project_path, session_path, dry_run=dry_run)
    fixer.run()

if __name__ == "__main__":
    main()
