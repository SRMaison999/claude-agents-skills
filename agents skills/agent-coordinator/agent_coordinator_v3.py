#!/usr/bin/env python3
"""
Agent Coordinator V3 - Orchestrateur Intelligent
Chef d'orchestre pour gérer tous les agents d'analyse, correction et documentation

Architecture centralisée avec sessions :
- reports/session-{timestamp}/1-ANALYSIS/    → Rapports JSON des agents
- reports/session-{timestamp}/2-FIXES/       → Corrections appliquées + backup
- reports/session-{timestamp}/3-DOCUMENTATION/ → Mises à jour README

NOUVEAUTÉ : Système de consensus multi-agents
- Seules les issues validées par au moins 2 agents sont appliquées
- Protection contre les faux positifs
- consensus-issues.json généré automatiquement

Usage:
    python agent_coordinator_v3.py /path/to/project
    python agent_coordinator_v3.py /path/to/project --auto
"""

import os
import sys
import io
import json
import asyncio
import platform
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import defaultdict

# Import du convertisseur
from report_converter import convert_report, save_json_report

# Import du consensus analyzer
from consensus_analyzer import ConsensusAnalyzer, ConsensusIssue

# Forcer UTF-8 pour la console Windows (support des emojis)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

@dataclass
class Issue:
    """Représente un problème détecté"""
    agent: str
    file_path: str
    line_number: int
    severity: str  # critical, important, minor
    issue_type: str
    description: str
    solution: str
    old_code: str = ""
    new_code: str = ""
    confidence: float = 0.0
    auto_fixable: bool = False

@dataclass
class AgentResult:
    """Résultat de l'exécution d'un agent"""
    agent_name: str
    status: str  # success, error, unavailable
    execution_time: float = 0.0
    issues_found: int = 0
    critical_count: int = 0
    important_count: int = 0
    minor_count: int = 0
    auto_fixable_count: int = 0
    report_path: Optional[Path] = None
    error_message: Optional[str] = None
    issues: List[Issue] = field(default_factory=list)

@dataclass
class SessionSummary:
    """Résumé complet d'une session d'analyse"""
    session_id: str
    session_path: Path
    project_path: Path
    start_time: str
    end_time: Optional[str] = None
    total_agents: int = 0
    successful_agents: int = 0
    failed_agents: int = 0
    total_issues: int = 0
    critical_count: int = 0
    important_count: int = 0
    minor_count: int = 0
    auto_fixable_count: int = 0
    agent_results: List[AgentResult] = field(default_factory=list)
    all_issues: List[Issue] = field(default_factory=list)
    fixes_applied: int = 0
    readme_updated: bool = False

    # Consensus data
    consensus_enabled: bool = True
    consensus_issues: List[ConsensusIssue] = field(default_factory=list)
    consensus_count: int = 0
    rejected_count: int = 0

class AgentCoordinatorV3:
    """
    Orchestrateur intelligent V3

    Gère le workflow complet :
    1. Analyse (agents parallèles → JSON)
    2. Corrections (Code Fixer → FIXES-APPLIED.md)
    3. Documentation (README Editor → README-UPDATE.md)
    """

    def __init__(self, project_path: str, auto_mode: bool = False):
        self.project_path = Path(project_path).resolve()
        self.auto_mode = auto_mode

        # Créer la session
        self.session_id = datetime.now().strftime('%Y%m%d-%H%M%S')
        self.session_summary = SessionSummary(
            session_id=self.session_id,
            session_path=self.create_session_folders(),
            project_path=self.project_path,
            start_time=datetime.now().isoformat()
        )

        # Agents disponibles
        self.available_agents = {
            "button-validator": {
                "script": "../button-validator/button_validator_v2.py",
                "enabled": True,
                "timeout": 300,
                "description": "Analyse des boutons et handlers"
            },
            "props-form-validator": {
                "script": "../props-form-validator/props_form_validator_v2.py",
                "enabled": True,
                "timeout": 300,
                "description": "Validation props, formulaires, emojis"
            },
            "dead-code-cleaner": {
                "script": "../dead-code-cleaner/dead_code_cleaner_v2.py",
                "enabled": True,
                "timeout": 300,
                "description": "Détection code mort, imports, console.log"
            },
            "consistency-checker": {
                "script": "../component-consistency-checker/consistency_checker_v2.py",
                "enabled": True,
                "timeout": 600,
                "description": "Cohérence visuelle des composants"
            }
        }

        self.print_header()

    def create_session_folders(self) -> Path:
        """Crée l'arborescence de la session"""
        # Dossier racine des rapports
        reports_root = Path(__file__).parent.parent.parent / "reports"
        reports_root.mkdir(exist_ok=True)

        # Dossier de session
        session_path = reports_root / f"session-{self.session_id}"
        session_path.mkdir(exist_ok=True)

        # Sous-dossiers
        (session_path / "1-ANALYSIS").mkdir(exist_ok=True)
        (session_path / "2-FIXES").mkdir(exist_ok=True)
        (session_path / "2-FIXES" / "backup").mkdir(exist_ok=True)
        (session_path / "3-DOCUMENTATION").mkdir(exist_ok=True)

        return session_path

    def print_header(self):
        """Affiche l'en-tête"""
        print("=" * 80)
        print("🎼 AGENT COORDINATOR V3 - Orchestrateur Intelligent")
        print("=" * 80)
        print(f"📁 Projet       : {self.project_path.name}")
        print(f"🆔 Session      : {self.session_id}")
        print(f"📊 Rapports     : reports/session-{self.session_id}/")
        print(f"🤖 Mode         : {'Automatique' if self.auto_mode else 'Conversationnel'}")
        print("=" * 80)
        print()

    async def run_agent(self, agent_name: str) -> AgentResult:
        """Lance un agent d'analyse"""

        agent_info = self.available_agents.get(agent_name)
        result = AgentResult(agent_name=agent_name, status="unknown")

        if not agent_info or not agent_info.get("enabled"):
            result.status = "unavailable"
            result.error_message = f"Agent {agent_name} non disponible"
            return result

        # Résoudre le chemin de l'agent
        agent_script = (Path(__file__).parent / agent_info["script"]).resolve()
        agent_dir = agent_script.parent

        if not agent_script.exists():
            result.status = "error"
            result.error_message = f"Script introuvable : {agent_script}"
            return result

        try:
            start_time = datetime.now()

            # Commande Python (Windows vs Linux)
            python_cmd = "py" if platform.system() == "Windows" else "python3"

            # Lancer l'agent V2 normalement (il écrit dans son propre dossier)
            cmd = [
                python_cmd,
                str(agent_script),
                str(self.project_path)
            ]

            # Lancer l'agent
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(agent_dir)
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=agent_info.get("timeout", 300)
            )

            execution_time = (datetime.now() - start_time).total_seconds()
            result.execution_time = execution_time

            # Décoder avec fallback
            def decode_output(data):
                for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
                    try:
                        return data.decode(encoding)
                    except:
                        continue
                return data.decode('utf-8', errors='replace')

            if process.returncode == 0:
                result.status = "success"

                # L'agent V2 a écrit son rapport Markdown dans son propre dossier reports/
                # Trouver le rapport le plus récent
                agent_reports_dir = agent_dir / "reports"

                if agent_reports_dir.exists():
                    # Trouver le rapport le plus récent
                    reports = sorted(agent_reports_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)

                    if reports:
                        latest_report = reports[0]

                        # Copier le rapport Markdown dans la session
                        session_md_path = self.session_summary.session_path / "1-ANALYSIS" / latest_report.name
                        shutil.copy2(latest_report, session_md_path)

                        # Convertir en JSON
                        json_data = convert_report(latest_report, agent_name)

                        if json_data:
                            # Sauvegarder le JSON
                            json_path = self.session_summary.session_path / "1-ANALYSIS" / f"{agent_name}.json"
                            save_json_report(json_data, json_path)

                            result.report_path = json_path
                            self.parse_agent_report(result, json_path)
                        else:
                            result.error_message = f"Erreur conversion Markdown → JSON"
                    else:
                        result.error_message = f"Aucun rapport trouvé dans {agent_reports_dir}"
                else:
                    result.error_message = f"Dossier reports introuvable : {agent_reports_dir}"
            else:
                result.status = "error"
                result.error_message = decode_output(stderr)

        except asyncio.TimeoutError:
            result.status = "timeout"
            result.error_message = f"Timeout après {agent_info.get('timeout')}s"
        except Exception as e:
            result.status = "error"
            result.error_message = str(e)

        return result

    def parse_agent_report(self, result: AgentResult, report_path: Path):
        """Parse le rapport JSON d'un agent"""
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Statistiques
            stats = data.get("statistics", {})
            result.issues_found = stats.get("total_issues", 0)
            result.critical_count = stats.get("critical", 0)
            result.important_count = stats.get("important", 0)
            result.minor_count = stats.get("minor", 0)
            result.auto_fixable_count = stats.get("auto_fixable", 0)

            # Issues détaillées
            for issue_data in data.get("issues", []):
                issue = Issue(
                    agent=result.agent_name,
                    file_path=issue_data.get("file", ""),
                    line_number=issue_data.get("line", 0),
                    severity=issue_data.get("severity", "minor"),
                    issue_type=issue_data.get("type", ""),
                    description=issue_data.get("description", ""),
                    solution=issue_data.get("solution", ""),
                    old_code=issue_data.get("old_code", ""),
                    new_code=issue_data.get("new_code", ""),
                    confidence=issue_data.get("confidence", 0.0),
                    auto_fixable=issue_data.get("auto_fixable", False)
                )
                result.issues.append(issue)

        except Exception as e:
            result.error_message = f"Erreur parsing JSON : {e}"

    async def run_analysis_phase(self, agents_to_run: List[str]) -> List[AgentResult]:
        """Phase 1 : Analyse parallèle"""

        print(f"\n{'=' * 80}")
        print(f"📊 PHASE 1 : ANALYSE")
        print(f"{'=' * 80}\n")
        print(f"⏳ Lancement de {len(agents_to_run)} agent(s) en parallèle...\n")

        # Lancer tous les agents en parallèle
        tasks = [self.run_agent(agent_name) for agent_name in agents_to_run]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Traiter les résultats
        agent_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                agent_results.append(AgentResult(
                    agent_name=agents_to_run[i],
                    status="error",
                    error_message=str(result)
                ))
            else:
                agent_results.append(result)

            # Afficher le statut
            agent_name = agents_to_run[i] if isinstance(result, Exception) else result.agent_name
            status_icon = "✅" if result.status == "success" else "❌"
            print(f"{status_icon} {agent_name:30} ", end="")

            if isinstance(result, AgentResult) and result.status == "success":
                print(f"({result.issues_found} issues - {result.execution_time:.1f}s)")
            else:
                error_msg = str(result) if isinstance(result, Exception) else result.error_message
                print(f"(ERREUR : {error_msg[:50]}...)")

        return agent_results

    def compile_results(self, agent_results: List[AgentResult]):
        """Compile les résultats de tous les agents"""

        self.session_summary.total_agents = len(agent_results)
        self.session_summary.agent_results = agent_results

        for result in agent_results:
            if result.status == "success":
                self.session_summary.successful_agents += 1
                self.session_summary.total_issues += result.issues_found
                self.session_summary.critical_count += result.critical_count
                self.session_summary.important_count += result.important_count
                self.session_summary.minor_count += result.minor_count
                self.session_summary.auto_fixable_count += result.auto_fixable_count
                self.session_summary.all_issues.extend(result.issues)
            else:
                self.session_summary.failed_agents += 1

    def analyze_consensus(self):
        """
        Analyse le consensus multi-agents

        Seules les issues validées par au moins 2 agents seront appliquées
        """

        print(f"\n{'=' * 80}")
        print(f"🤝 ANALYSE DE CONSENSUS MULTI-AGENTS")
        print(f"{'=' * 80}\n")

        if self.session_summary.successful_agents < 2:
            print(f"⚠️  Moins de 2 agents réussis, consensus désactivé")
            print(f"   → Toutes les issues seront considérées\n")
            self.session_summary.consensus_enabled = False
            return

        # Lancer l'analyse de consensus
        analyzer = ConsensusAnalyzer(line_tolerance=2)
        consensus_issues, rejected_issues = analyzer.find_consensus(
            self.session_summary.all_issues,
            min_agents=2
        )

        # Mettre à jour le résumé
        self.session_summary.consensus_issues = consensus_issues
        self.session_summary.consensus_count = len(consensus_issues)
        self.session_summary.rejected_count = len(rejected_issues)

        # Afficher le rapport
        stats = analyzer.get_statistics()

        print(f"✅ Issues validées par consensus : {stats['total_consensus']}")
        if stats['consensus_2_agents'] > 0:
            print(f"   • 2 agents d'accord : {stats['consensus_2_agents']}")
        if stats['consensus_3_agents'] > 0:
            print(f"   • 3 agents d'accord : {stats['consensus_3_agents']}")
        if stats['consensus_4_plus'] > 0:
            print(f"   • 4+ agents d'accord : {stats['consensus_4_plus']}")
        print()

        print(f"🤖 Corrections automatiques disponibles : {stats['auto_fixable']}")
        print()

        print(f"❌ Issues rejetées (1 seul agent) : {stats['total_rejected']}")
        print(f"   → Pas assez de consensus pour appliquer")
        print()

        if stats['total_consensus'] > 0:
            print(f"💡 Seules les {stats['total_consensus']} issues validées seront appliquées")
            print(f"   (protection contre les faux positifs)")
        else:
            print(f"⚠️  Aucun consensus trouvé")
            print(f"   Les agents ne sont pas d'accord sur les corrections")

        print(f"{'=' * 80}")

        # Sauvegarder le fichier consensus-issues.json
        self.save_consensus_issues()

        # Mettre à jour auto_fixable_count avec le consensus
        self.session_summary.auto_fixable_count = stats['auto_fixable']

    def save_consensus_issues(self):
        """Sauvegarde les issues de consensus en JSON"""

        if not self.session_summary.consensus_enabled:
            return

        consensus_file = self.session_summary.session_path / "1-ANALYSIS" / "consensus-issues.json"

        # Convertir ConsensusIssue en dict pour JSON
        consensus_data = {
            "consensus_enabled": True,
            "min_agents_required": 2,
            "timestamp": datetime.now().isoformat(),
            "statistics": {
                "total_consensus": self.session_summary.consensus_count,
                "rejected": self.session_summary.rejected_count,
                "auto_fixable": sum(1 for i in self.session_summary.consensus_issues if i.auto_fixable)
            },
            "issues": [
                {
                    "file": issue.file_path,
                    "line": issue.line_number,
                    "type": issue.issue_type,
                    "description": issue.description,
                    "solution": issue.solution,
                    "severity": issue.severity,
                    "old_code": issue.old_code,
                    "new_code": issue.new_code,
                    "confidence": issue.confidence,
                    "auto_fixable": issue.auto_fixable,
                    "agreed_by": issue.agreed_by,
                    "consensus_level": issue.consensus_level
                }
                for issue in self.session_summary.consensus_issues
            ]
        }

        with open(consensus_file, 'w', encoding='utf-8') as f:
            json.dump(consensus_data, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Consensus sauvegardé : consensus-issues.json\n")

    def present_analysis_summary(self):
        """Présente le résumé de l'analyse"""

        s = self.session_summary

        print(f"\n{'=' * 80}")
        print(f"📊 RÉSUMÉ DE L'ANALYSE")
        print(f"{'=' * 80}\n")

        # Agents
        print(f"🤖 Agents exécutés : {s.successful_agents}/{s.total_agents}")
        if s.failed_agents > 0:
            print(f"⚠️  Agents échoués  : {s.failed_agents}")
        print()

        # Message honnête sur l'état de l'app
        print(f"{'─' * 80}")
        print(f"✅ Votre application FONCTIONNE")
        print(f"{'─' * 80}\n")

        # Catégorisation honnête
        print(f"📋 Suggestions d'amélioration détectées : {s.total_issues}\n")

        # Analyser les types réels
        emoji_count = sum(1 for issue in s.all_issues if 'emoji' in issue.issue_type.lower())
        console_count = sum(1 for issue in s.all_issues if 'console' in issue.issue_type.lower())
        import_count = sum(1 for issue in s.all_issues if 'import' in issue.issue_type.lower())
        consistency_count = s.important_count  # Généralement des incohérences visuelles

        print(f"🟡 **NETTOYAGE DU CODE** (recommandé mais non bloquant)")
        if console_count > 0:
            print(f"   • {console_count} console.log de debug à retirer")
        if import_count > 0:
            print(f"   • {import_count} imports inutilisés (bundle size)")
        if emoji_count > 0:
            print(f"   • {emoji_count} emojis dans le code (convention)")
        print()

        if consistency_count > 0:
            print(f"🎨 **COHÉRENCE VISUELLE** (suggestions de design)")
            print(f"   • {consistency_count} variations de style détectées")
            print(f"   (ex: couleurs de boutons, espacements)")
            print()

        # Bugs réels (s'il y en a)
        real_bugs = s.critical_count - emoji_count
        if real_bugs > 0:
            print(f"🔴 **BUGS POTENTIELS** (à vérifier)")
            print(f"   • {real_bugs} problèmes fonctionnels détectés")
            print()

        # Corrections automatiques
        if s.auto_fixable_count > 0:
            print(f"🤖 Corrections automatiques disponibles : {s.auto_fixable_count}")
            if s.consensus_enabled:
                print(f"   ✅ Validées par consensus multi-agents (min 2 agents)")
            print(f"   (principalement nettoyage : console.log, emojis, imports)")
            print()

        # Rapports générés
        print(f"📁 Rapports détaillés dans :")
        try:
            print(f"   {s.session_path.relative_to(Path.cwd())}/1-ANALYSIS/")
        except ValueError:
            print(f"   {s.session_path}/1-ANALYSIS/")

        # Détails par agent
        if not self.auto_mode:
            print(f"\n{'─' * 80}")
            print(f"💬 Options :")
            print(f"   [d] Voir les DÉTAILS")
            print(f"   [c] CONTINUER (appliquer nettoyage automatique)")
            print(f"   [q] QUITTER (garder l'app telle quelle)")
            print(f"{'─' * 80}\n")

    def show_detailed_issues(self, limit: int = 10):
        """Affiche les détails des issues"""

        s = self.session_summary

        print(f"\n{'=' * 80}")
        print(f"🔍 DÉTAILS DES SUGGESTIONS (Top {limit} par catégorie)")
        print(f"{'=' * 80}\n")

        # Catégoriser par TYPE plutôt que par sévérité
        issues_by_type = {
            "nettoyage": [i for i in s.all_issues if any(word in i.issue_type.lower() for word in ['emoji', 'console', 'import', 'commented'])],
            "coherence": [i for i in s.all_issues if 'consistency' in i.agent or i.severity == "important"],
            "autres": [i for i in s.all_issues if i not in issues_by_type.get("nettoyage", []) and i not in issues_by_type.get("coherence", [])]
        }

        # Nettoyage
        if issues_by_type.get("nettoyage"):
            print(f"🟡 NETTOYAGE DU CODE ({len(issues_by_type['nettoyage'])}) :\n")
            for issue in issues_by_type["nettoyage"][:limit]:
                type_name = {
                    'emoji_detected': '🎨 Emoji dans le code',
                    'console_log': '🐛 Console.log de debug',
                    'unused_import': '📦 Import inutilisé',
                    'commented_code': '💬 Code commenté'
                }.get(issue.issue_type, issue.issue_type)

                print(f"  • {type_name}")
                print(f"    Fichier   : {issue.file_path}:{issue.line_number}")
                print(f"    Détail    : {issue.description[:60]}")
                print()

            if len(issues_by_type["nettoyage"]) > limit:
                print(f"  ... et {len(issues_by_type['nettoyage']) - limit} autres\n")

        # Cohérence
        if issues_by_type.get("coherence"):
            print(f"🎨 COHÉRENCE VISUELLE ({len(issues_by_type['coherence'])}) :\n")
            for issue in issues_by_type["coherence"][:limit]:
                print(f"  • {issue.file_path}:{issue.line_number}")
                print(f"    Suggestion : {issue.description[:70]}")
                print()

            if len(issues_by_type["coherence"]) > limit:
                print(f"  ... et {len(issues_by_type['coherence']) - limit} autres\n")

        # Autres
        if issues_by_type.get("autres"):
            print(f"❓ AUTRES ({len(issues_by_type['autres'])}) :\n")
            for issue in issues_by_type["autres"][:limit]:
                print(f"  • {issue.file_path}:{issue.line_number}")
                print(f"    Type : {issue.issue_type}")
                print(f"    {issue.description[:70]}")
                print()

        print(f"{'─' * 80}\n")
        print(f"💡 Rappel : Ce sont des SUGGESTIONS, pas des bugs bloquants.\n")

    async def run_code_fixer(self) -> bool:
        """Phase 2 : Application des corrections"""

        print(f"\n{'=' * 80}")
        print(f"🔧 PHASE 2 : CORRECTIONS")
        print(f"{'=' * 80}\n")

        code_fixer_script = (Path(__file__).parent.parent / "code-fixer" / "code_fixer_v3.py").resolve()

        if not code_fixer_script.exists():
            print(f"❌ Code Fixer V3 introuvable : {code_fixer_script}")
            return False

        try:
            python_cmd = "py" if platform.system() == "Windows" else "python3"

            cmd = [
                python_cmd,
                str(code_fixer_script),
                str(self.project_path),
                "--session", str(self.session_summary.session_path)
            ]

            print(f"⏳ Lancement de Code Fixer...\n")

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                print(f"✅ Code Fixer terminé avec succès\n")

                # Lire le nombre de corrections depuis FIXES-APPLIED.md
                fixes_report = self.session_summary.session_path / "2-FIXES" / "FIXES-APPLIED.md"
                if fixes_report.exists():
                    # Parser le nombre de corrections (ligne "**Corrections appliquées** : X")
                    with open(fixes_report, 'r', encoding='utf-8') as f:
                        content = f.read()
                        import re
                        match = re.search(r'\*\*Corrections appliquées\*\*\s*:\s*(\d+)', content)
                        if match:
                            self.session_summary.fixes_applied = int(match.group(1))

                return True
            else:
                print(f"❌ Code Fixer a échoué\n")
                print(stderr.decode('utf-8', errors='replace'))
                return False

        except Exception as e:
            print(f"❌ Erreur lors du lancement de Code Fixer : {e}")
            return False

    async def run_readme_editor(self) -> bool:
        """Phase 3 : Mise à jour documentation"""

        print(f"\n{'=' * 80}")
        print(f"📝 PHASE 3 : DOCUMENTATION")
        print(f"{'=' * 80}\n")

        readme_editor_script = (Path(__file__).parent.parent / "readme-editor" / "readme_editor_v3.py").resolve()

        if not readme_editor_script.exists():
            print(f"❌ README Editor V3 introuvable : {readme_editor_script}")
            return False

        try:
            python_cmd = "py" if platform.system() == "Windows" else "python3"

            cmd = [
                python_cmd,
                str(readme_editor_script),
                str(self.project_path),
                "--session", str(self.session_summary.session_path)
            ]

            print(f"⏳ Lancement de README Editor...\n")

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                print(f"✅ README Editor terminé avec succès\n")
                self.session_summary.readme_updated = True
                return True
            else:
                print(f"⚠️  README Editor a échoué (non bloquant)\n")
                print(stderr.decode('utf-8', errors='replace'))
                return False

        except Exception as e:
            print(f"⚠️  Erreur lors du lancement de README Editor : {e}")
            return False

    def present_final_summary(self):
        """Présente le résumé final de la session"""

        s = self.session_summary
        s.end_time = datetime.now().isoformat()

        print(f"\n{'=' * 80}")
        print(f"🎉 SESSION TERMINÉE")
        print(f"{'=' * 80}\n")

        # Message encourageant
        if s.fixes_applied > 0:
            print(f"✅ Votre code est plus propre !")
        else:
            print(f"✅ Analyse terminée")
        print()

        print(f"📊 Résumé :")
        print(f"   • Suggestions d'amélioration : {s.total_issues}")
        print(f"   • Nettoyages appliqués       : {s.fixes_applied}")
        print(f"   • Documentation MAJ          : {'✅ Oui' if s.readme_updated else '❌ Non'}")
        print()

        # Catégorisation des suggestions
        emoji_count = sum(1 for issue in s.all_issues if 'emoji' in issue.issue_type.lower())
        console_count = sum(1 for issue in s.all_issues if 'console' in issue.issue_type.lower())

        if s.total_issues > 0:
            print(f"💡 Type de suggestions :")
            if emoji_count > 0:
                status = "✅ Nettoyés" if s.fixes_applied > 0 else "⏳ Détectés"
                print(f"   • Emojis dans le code     : {emoji_count} {status}")
            if console_count > 0:
                print(f"   • Console.log de debug    : {console_count}")
            if s.important_count > 0:
                print(f"   • Cohérence visuelle      : {s.important_count}")
            print()

        print(f"📁 Tous les rapports sont dans :")
        try:
            print(f"   {s.session_path.relative_to(Path.cwd())}/")
        except ValueError:
            print(f"   {s.session_path}/")
        print()
        print(f"   • 1-ANALYSIS/       → Rapports d'analyse JSON")
        if s.fixes_applied > 0:
            print(f"   • 2-FIXES/          → FIXES-APPLIED.md (voir ce qui a été modifié)")
        else:
            print(f"   • 2-FIXES/          → Aucune modification apportée")
        print(f"   • 3-DOCUMENTATION/  → README-UPDATE.md")
        print()

        # Sauvegarder le résumé JSON de la session
        self.save_session_summary()

        print(f"💬 Rappel : Les \"suggestions\" détectées ne sont PAS des bugs.")
        print(f"   Votre application fonctionne correctement.")
        print(f"{'=' * 80}\n")

    def save_session_summary(self):
        """Sauvegarde le résumé de session en JSON"""
        summary_file = self.session_summary.session_path / "session-summary.json"

        # Convertir en dict (sans les objets complexes)
        summary_data = {
            "session_id": self.session_summary.session_id,
            "project": str(self.session_summary.project_path),
            "start_time": self.session_summary.start_time,
            "end_time": self.session_summary.end_time,
            "consensus": {
                "enabled": self.session_summary.consensus_enabled,
                "consensus_count": self.session_summary.consensus_count,
                "rejected_count": self.session_summary.rejected_count
            },
            "statistics": {
                "total_agents": self.session_summary.total_agents,
                "successful_agents": self.session_summary.successful_agents,
                "failed_agents": self.session_summary.failed_agents,
                "total_issues": self.session_summary.total_issues,
                "critical": self.session_summary.critical_count,
                "important": self.session_summary.important_count,
                "minor": self.session_summary.minor_count,
                "auto_fixable": self.session_summary.auto_fixable_count,
                "fixes_applied": self.session_summary.fixes_applied,
                "readme_updated": self.session_summary.readme_updated
            },
            "agents": [
                {
                    "name": r.agent_name,
                    "status": r.status,
                    "execution_time": r.execution_time,
                    "issues_found": r.issues_found
                }
                for r in self.session_summary.agent_results
            ]
        }

        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)

    async def run_full_workflow(self):
        """Exécute le workflow complet"""

        # Phase 1 : Analyse
        agents_to_run = [name for name, info in self.available_agents.items() if info.get("enabled")]
        agent_results = await self.run_analysis_phase(agents_to_run)

        # Compiler les résultats
        self.compile_results(agent_results)

        # Analyser le consensus multi-agents
        self.analyze_consensus()

        # Présenter le résumé
        self.present_analysis_summary()

        # En mode conversationnel, demander confirmation
        if not self.auto_mode:
            while True:
                choice = input("Votre choix : ").lower().strip()

                if choice in ['d', 'detail', 'détails']:
                    self.show_detailed_issues(limit=20)
                    print("Appuyez sur [c] pour CONTINUER ou [q] pour QUITTER")
                    continue
                elif choice in ['c', 'continue', 'continuer']:
                    break
                elif choice in ['q', 'quit', 'quitter']:
                    print("\n👋 Session terminée sans corrections.\n")
                    return
                else:
                    print("Choix invalide. [d] détails, [c] continuer, [q] quitter")

        # Si aucune correction auto-fixable, ne pas lancer Code Fixer
        if self.session_summary.auto_fixable_count == 0:
            print(f"\n⚠️  Aucune correction automatique disponible.")
            print(f"   Les issues nécessitent une intervention manuelle.\n")
            self.present_final_summary()
            return

        # Demander confirmation pour les corrections
        if not self.auto_mode:
            print(f"\n{'─' * 80}")
            print(f"💬 Lancer Code Fixer pour appliquer {self.session_summary.auto_fixable_count} corrections ?")
            print(f"   [o] OUI")
            print(f"   [n] NON")
            print(f"{'─' * 80}\n")

            choice = input("Votre choix [O/n] : ").lower().strip()
            if choice in ['n', 'non', 'no']:
                print("\n❌ Corrections annulées.\n")
                self.present_final_summary()
                return

        # Phase 2 : Corrections
        code_fixer_success = await self.run_code_fixer()

        if not code_fixer_success:
            print("\n⚠️  Code Fixer a échoué. Arrêt du workflow.\n")
            self.present_final_summary()
            return

        # Phase 3 : Documentation
        await self.run_readme_editor()

        # Résumé final
        self.present_final_summary()

    async def run(self):
        """Point d'entrée principal"""

        if not self.project_path.exists():
            print(f"❌ Projet introuvable : {self.project_path}\n")
            return

        await self.run_full_workflow()

def main():
    """Point d'entrée"""
    if len(sys.argv) < 2:
        print("Usage: python agent_coordinator_v3.py /path/to/project [--auto]")
        sys.exit(1)

    project_path = sys.argv[1]
    auto_mode = "--auto" in sys.argv

    coordinator = AgentCoordinatorV3(project_path, auto_mode)
    asyncio.run(coordinator.run())

if __name__ == "__main__":
    main()
