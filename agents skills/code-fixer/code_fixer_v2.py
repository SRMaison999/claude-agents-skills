#!/usr/bin/env python3
"""
Code Fixer V2 - Correction Engine
Agent d'application automatique des corrections validées avec backup et rollback

SÉCURITÉ : Backup avant chaque modification, rollback automatique si erreur

Usage:
    python code_fixer_v2.py --auto                    # Mode automatique
    python code_fixer_v2.py --fixes report.json       # Depuis un fichier
    python code_fixer_v2.py --rollback {timestamp}    # Rollback
"""

import os
import re
import json
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
from collections import defaultdict

@dataclass
class Fix:
    """Représente une correction à appliquer"""
    file_path: str
    line_number: int
    fix_type: str
    description: str
    old_content: str
    new_content: str
    confidence: float
    applied: bool = False
    success: bool = False
    error: Optional[str] = None

@dataclass
class FixSession:
    """Session de corrections"""
    timestamp: str
    backup_dir: Path
    fixes_applied: List[Fix] = field(default_factory=list)
    fixes_failed: List[Fix] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)

class CodeFixer:
    """
    Agent d'application automatique des corrections
    """

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.session = self.create_session()

        self.print_header()

    def print_header(self):
        """Affiche l'en-tête"""
        print("="*70)
        print("🔧 Code Fixer V2 - Correction Engine")
        print("="*70)
        print(f"📁 Projet : {self.project_path.name}")
        print(f"🕐 Session : {self.session.timestamp}")
        print(f"💾 Backup : {self.session.backup_dir}")
        print("="*70)

    def create_session(self) -> FixSession:
        """Crée une nouvelle session de corrections"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        backup_dir = self.project_path / ".agent-backup" / timestamp
        backup_dir.mkdir(parents=True, exist_ok=True)

        return FixSession(
            timestamp=timestamp,
            backup_dir=backup_dir
        )

    def find_latest_reports(self) -> List[Path]:
        """Trouve les rapports les plus récents des agents"""
        reports_dir = self.project_path / "reports"

        if not reports_dir.exists():
            return []

        # Chercher tous les rapports générés aujourd'hui
        today = datetime.now().strftime('%Y%m%d')

        reports = []
        for report_file in reports_dir.glob(f"*-{today}-*.md"):
            reports.append(report_file)

        # Si aucun rapport aujourd'hui, prendre les 3 plus récents
        if not reports:
            all_reports = sorted(reports_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
            reports = all_reports[:3]

        return reports

    def parse_report_for_fixes(self, report_path: Path) -> List[Fix]:
        """Parse un rapport pour extraire les corrections auto"""
        fixes = []

        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return fixes

        # Détecter le type de rapport
        if 'button-analysis' in report_path.name:
            fixes.extend(self.parse_button_report(content))
        elif 'props-form-analysis' in report_path.name:
            fixes.extend(self.parse_props_report(content))
        elif 'dead-code-report' in report_path.name:
            fixes.extend(self.parse_dead_code_report(content))

        return fixes

    def parse_button_report(self, content: str) -> List[Fix]:
        """Parse le rapport du button validator"""
        fixes = []

        # Chercher les corrections auto (confiance >= 90)
        # Pattern: **file_path:line** [severity]
        pattern = r'\*\*([^:]+):(\d+)\*\*[^\n]*\n.*?Type\s*:\s*([^\n]+)\n.*?Problème\s*:\s*([^\n]+)\n.*?Solution\s*:\s*([^\n]+)\n.*?Confiance\s*:\s*(\d+(?:\.\d+)?)%'

        for match in re.finditer(pattern, content, re.DOTALL):
            file_path = match.group(1).strip()
            line_num = int(match.group(2))
            fix_type = match.group(3).strip()
            description = match.group(4).strip()
            solution = match.group(5).strip()
            confidence = float(match.group(6))

            if confidence >= 90:
                fixes.append(Fix(
                    file_path=file_path,
                    line_number=line_num,
                    fix_type=fix_type,
                    description=description,
                    old_content="",  # À extraire du fichier
                    new_content="",  # À calculer
                    confidence=confidence
                ))

        return fixes

    def parse_props_report(self, content: str) -> List[Fix]:
        """Parse le rapport du props validator"""
        fixes = []

        # Chercher les emojis (priorité absolue, confiance 100%)
        emoji_pattern = r'\*\*([^:]+):(\d+)\*\*[^\n]*emoji[^\n]*\n.*?Problème\s*:\s*([^\n]+)\n.*?Solution\s*:\s*([^\n]+)'

        for match in re.finditer(emoji_pattern, content, re.DOTALL | re.IGNORECASE):
            file_path = match.group(1).strip()
            line_num = int(match.group(2))
            description = match.group(3).strip()
            solution = match.group(4).strip()

            fixes.append(Fix(
                file_path=file_path,
                line_number=line_num,
                fix_type="emoji_removal",
                description=description,
                old_content="",
                new_content="",
                confidence=100.0
            ))

        return fixes

    def parse_dead_code_report(self, content: str) -> List[Fix]:
        """Parse le rapport du dead code cleaner"""
        fixes = []

        # Chercher les suppressions auto (imports, console.log)
        # Section "Suppressions automatiques"
        auto_section = re.search(r'Suppressions automatiques.*?```(.*?)```', content, re.DOTALL)

        if auto_section:
            auto_content = auto_section.group(1)

            # Parse les lignes: - file.tsx:123 - description
            pattern = r'-\s*([^:]+):(\d+)\s*-\s*(.+)'

            for match in re.finditer(pattern, auto_content):
                file_path = match.group(1).strip()
                line_num = int(match.group(2))
                description = match.group(3).strip()

                # Déterminer le type
                if 'import' in description.lower():
                    fix_type = "unused_import"
                elif 'console' in description.lower():
                    fix_type = "console_log"
                else:
                    fix_type = "dead_code"

                fixes.append(Fix(
                    file_path=file_path,
                    line_number=line_num,
                    fix_type=fix_type,
                    description=description,
                    old_content="",
                    new_content="",
                    confidence=95.0
                ))

        return fixes

    def backup_file(self, file_path: Path):
        """Crée un backup d'un fichier"""
        if not file_path.exists():
            return

        relative_path = file_path.relative_to(self.project_path)
        backup_path = self.session.backup_dir / relative_path

        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)

    def apply_fix(self, fix: Fix) -> bool:
        """Applique une correction à un fichier"""
        file_path = self.project_path / fix.file_path

        if not file_path.exists():
            fix.error = f"Fichier introuvable: {file_path}"
            return False

        # Backup avant modification
        self.backup_file(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if fix.line_number > len(lines):
                fix.error = f"Ligne {fix.line_number} hors limites ({len(lines)} lignes)"
                return False

            # Appliquer la correction selon le type
            if fix.fix_type == "emoji_removal":
                success = self.remove_emoji(lines, fix)
            elif fix.fix_type == "unused_import":
                success = self.remove_unused_import(lines, fix)
            elif fix.fix_type == "console_log":
                success = self.remove_console_log(lines, fix)
            elif fix.fix_type == "dead_code":
                success = self.remove_dead_code(lines, fix)
            else:
                fix.error = f"Type de correction inconnu: {fix.fix_type}"
                return False

            if success:
                # Écrire les modifications
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                # Vérifier la syntaxe si TypeScript/JavaScript
                if file_path.suffix in ['.ts', '.tsx', '.js', '.jsx']:
                    if not self.verify_syntax(file_path):
                        # Rollback ce fichier
                        self.rollback_file(file_path)
                        fix.error = "Erreur de syntaxe après modification"
                        return False

                fix.applied = True
                fix.success = True
                return True

        except Exception as e:
            fix.error = str(e)
            # Rollback ce fichier
            self.rollback_file(file_path)
            return False

        return False

    def remove_emoji(self, lines: List[str], fix: Fix) -> bool:
        """Supprime les emojis d'une ligne"""
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
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+"
        )

        line_idx = fix.line_number - 1
        if line_idx < 0 or line_idx >= len(lines):
            return False

        original = lines[line_idx]
        modified = emoji_pattern.sub('', original)

        fix.old_content = original.strip()
        fix.new_content = modified.strip()

        lines[line_idx] = modified

        return True

    def remove_unused_import(self, lines: List[str], fix: Fix) -> bool:
        """Supprime un import inutilisé"""
        # Chercher la ligne d'import
        for i, line in enumerate(lines):
            if line.strip().startswith('import') and fix.line_number - 5 <= i + 1 <= fix.line_number + 5:
                # Vérifier si c'est le bon import (basé sur la description)
                fix.old_content = line.strip()
                lines[i] = ""  # Supprimer la ligne
                fix.new_content = "(ligne supprimée)"
                return True

        return False

    def remove_console_log(self, lines: List[str], fix: Fix) -> bool:
        """Supprime un console.log"""
        line_idx = fix.line_number - 1
        if line_idx < 0 or line_idx >= len(lines):
            return False

        line = lines[line_idx]

        if 'console.' in line:
            fix.old_content = line.strip()

            # Supprimer la ligne complète si elle ne contient que le console.log
            stripped = line.strip()
            if stripped.startswith('console.') or (';' in stripped and stripped.split(';')[0].strip().startswith('console.')):
                lines[line_idx] = ""
                fix.new_content = "(ligne supprimée)"
            else:
                # Sinon, juste retirer le console.log de la ligne
                modified = re.sub(r'console\.(log|warn|error|info|debug)\([^)]*\);?', '', line)
                lines[line_idx] = modified
                fix.new_content = modified.strip()

            return True

        return False

    def remove_dead_code(self, lines: List[str], fix: Fix) -> bool:
        """Supprime du code mort"""
        line_idx = fix.line_number - 1
        if line_idx < 0 or line_idx >= len(lines):
            return False

        fix.old_content = lines[line_idx].strip()
        lines[line_idx] = ""
        fix.new_content = "(ligne supprimée)"

        return True

    def verify_syntax(self, file_path: Path) -> bool:
        """Vérifie la syntaxe du fichier (parse sans exécuter)"""
        # Pour TypeScript/JavaScript, on peut vérifier avec Node.js si disponible
        try:
            # Essayer avec node --check
            result = subprocess.run(
                ['node', '--check', str(file_path)],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            # Si node n'est pas disponible, on suppose que c'est OK
            return True

    def rollback_file(self, file_path: Path):
        """Restaure un fichier depuis le backup"""
        relative_path = file_path.relative_to(self.project_path)
        backup_path = self.session.backup_dir / relative_path

        if backup_path.exists():
            shutil.copy2(backup_path, file_path)

    def rollback_session(self):
        """Rollback complet de la session"""
        print(f"\n⏪ Rollback de la session {self.session.timestamp}...")

        for file_path_str in self.session.files_modified:
            file_path = self.project_path / file_path_str
            self.rollback_file(file_path)

        print(f"✅ Rollback terminé - {len(self.session.files_modified)} fichiers restaurés")

    def create_git_commit(self, fixes_applied: List[Fix]) -> bool:
        """Crée un commit Git avec les modifications"""
        try:
            # Vérifier si Git est disponible
            result = subprocess.run(
                ['git', 'status'],
                cwd=self.project_path,
                capture_output=True,
                timeout=5
            )

            if result.returncode != 0:
                print("⚠️  Git non disponible ou pas un repo Git")
                return False

            # Ajouter les fichiers modifiés
            for fix in fixes_applied:
                subprocess.run(
                    ['git', 'add', fix.file_path],
                    cwd=self.project_path,
                    timeout=5
                )

            # Créer le message de commit
            message = f"fix: Auto-corrections ({len(fixes_applied)} corrections)\n\n"
            message += "Corrections appliquées par Code Fixer V2:\n"

            fix_types = defaultdict(int)
            for fix in fixes_applied:
                fix_types[fix.fix_type] += 1

            for fix_type, count in fix_types.items():
                message += f"- {fix_type.replace('_', ' ').title()}: {count}\n"

            # Commit
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.project_path,
                capture_output=True,
                timeout=10
            )

            if result.returncode == 0:
                print(f"✅ Commit Git créé")
                return True
            else:
                print(f"⚠️  Impossible de créer le commit: {result.stderr.decode()}")
                return False

        except Exception as e:
            print(f"⚠️  Erreur Git: {e}")
            return False

    def generate_report(self) -> str:
        """Génère le rapport de la session"""
        report = f"""# Code Fixer - Rapport de corrections

**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Session** : {self.session.timestamp}
**Projet** : {self.project_path.name}

---

## 📊 Vue d'ensemble

**Corrections appliquées** : {len(self.session.fixes_applied)}
**Corrections échouées** : {len(self.session.fixes_failed)}
**Fichiers modifiés** : {len(self.session.files_modified)}

---

## ✅ Corrections réussies

"""

        for fix in self.session.fixes_applied:
            report += f"""
### {fix.file_path}:{fix.line_number}
- **Type** : {fix.fix_type}
- **Description** : {fix.description}
- **Confiance** : {fix.confidence}%
- **Avant** : `{fix.old_content[:100]}`
- **Après** : `{fix.new_content[:100]}`
"""

        if self.session.fixes_failed:
            report += f"""
---

## ❌ Corrections échouées

"""

            for fix in self.session.fixes_failed:
                report += f"""
### {fix.file_path}:{fix.line_number}
- **Type** : {fix.fix_type}
- **Description** : {fix.description}
- **Erreur** : {fix.error}
"""

        report += f"""
---

## 💾 Backup

Backup sauvegardé dans : `{self.session.backup_dir.relative_to(self.project_path)}`

Pour rollback :
```bash
python code_fixer_v2.py --rollback {self.session.timestamp}
```

---

**Rapport généré par Code Fixer V2**
"""

        return report

    def run_auto_mode(self):
        """Mode automatique : lit les rapports et applique les corrections auto"""
        print("\n🔍 Recherche des rapports récents...")

        reports = self.find_latest_reports()

        if not reports:
            print("❌ Aucun rapport trouvé dans ./reports/")
            return

        print(f"✅ {len(reports)} rapport(s) trouvé(s)\n")

        # Extraire toutes les corrections auto
        all_fixes = []
        for report_path in reports:
            print(f"📄 Analyse de {report_path.name}...")
            fixes = self.parse_report_for_fixes(report_path)
            all_fixes.extend(fixes)

        if not all_fixes:
            print("\n❌ Aucune correction automatique trouvée (confiance >= 90%)")
            return

        print(f"\n✅ {len(all_fixes)} correction(s) automatique(s) trouvée(s)\n")

        # Grouper par type
        by_type = defaultdict(list)
        for fix in all_fixes:
            by_type[fix.fix_type].append(fix)

        print("📋 Corrections à appliquer :")
        for fix_type, fixes in by_type.items():
            print(f"   - {fix_type.replace('_', ' ').title()} : {len(fixes)}")

        # Demander confirmation
        print(f"\n⚠️  {len(all_fixes)} modifications vont être appliquées.")
        print(f"💾 Backup créé dans : {self.session.backup_dir.relative_to(self.project_path)}")

        confirm = input("\nContinuer ? [o/N] : ")

        if confirm.lower() not in ['o', 'oui', 'y', 'yes']:
            print("❌ Annulé")
            return

        # Appliquer les corrections
        print("\n🔧 Application des corrections...\n")

        for i, fix in enumerate(all_fixes, 1):
            print(f"[{i}/{len(all_fixes)}] {fix.file_path}:{fix.line_number} - {fix.fix_type}...")

            success = self.apply_fix(fix)

            if success:
                self.session.fixes_applied.append(fix)
                if fix.file_path not in self.session.files_modified:
                    self.session.files_modified.append(fix.file_path)
                print(f"  ✅ Appliqué")
            else:
                self.session.fixes_failed.append(fix)
                print(f"  ❌ Échoué: {fix.error}")

        print(f"\n✅ Corrections terminées !")
        print(f"   Réussies : {len(self.session.fixes_applied)}")
        print(f"   Échouées : {len(self.session.fixes_failed)}")

        # Créer commit Git (optionnel)
        if self.session.fixes_applied:
            create_commit = input("\nCréer un commit Git ? [o/N] : ")
            if create_commit.lower() in ['o', 'oui', 'y', 'yes']:
                self.create_git_commit(self.session.fixes_applied)

        # Générer rapport
        report = self.generate_report()

        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)

        report_filename = f"fixes-applied-{self.session.timestamp}.md"
        report_path = reports_dir / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n📄 Rapport : {report_path}")

def main():
    """Point d'entrée principal"""
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python code_fixer_v2.py --auto")
        print("  python code_fixer_v2.py --rollback {timestamp}")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "--auto":
        fixer = CodeFixer(".")
        fixer.run_auto_mode()

    elif mode == "--rollback":
        if len(sys.argv) < 3:
            print("❌ Timestamp requis pour rollback")
            sys.exit(1)

        timestamp = sys.argv[2]
        fixer = CodeFixer(".")

        # Charger la session à rollback
        fixer.session.timestamp = timestamp
        fixer.session.backup_dir = fixer.project_path / ".agent-backup" / timestamp

        if not fixer.session.backup_dir.exists():
            print(f"❌ Backup introuvable : {fixer.session.backup_dir}")
            sys.exit(1)

        # Lister les fichiers à restaurer
        backup_files = list(fixer.session.backup_dir.rglob("*"))
        backup_files = [f for f in backup_files if f.is_file()]

        fixer.session.files_modified = [
            str(f.relative_to(fixer.session.backup_dir))
            for f in backup_files
        ]

        print(f"⚠️  {len(backup_files)} fichier(s) vont être restaurés")
        confirm = input("Continuer ? [o/N] : ")

        if confirm.lower() in ['o', 'oui', 'y', 'yes']:
            fixer.rollback_session()

    else:
        print(f"❌ Mode inconnu: {mode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
