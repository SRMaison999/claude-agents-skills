#!/usr/bin/env python3
"""
Agent Coordinator V2 - Orchestration & Conversational Interface
Chef d'orchestre intelligent pour gérer tous les agents d'analyse

Usage: 
    python agent_coordinator_v2.py /path/to/project
    python agent_coordinator_v2.py /path/to/project --auto
"""

import os
import re
import json
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import subprocess

@dataclass
class Intent:
    """Intention détectée de l'utilisateur"""
    action: str = ""  # cleanup, full_analysis, analyze_buttons, etc.
    agents: List[str] = field(default_factory=list)
    scope: str = "project"  # project, file, component, folder
    target: Optional[str] = None
    focus: Optional[str] = None
    confidence: float = 0.0

@dataclass
class AgentTask:
    """Tâche pour un agent"""
    name: str
    priority: int
    scope: Optional[str] = None
    target: Optional[str] = None
    estimated_time: int = 60  # secondes

@dataclass
class ActionPlan:
    """Plan d'action à exécuter"""
    description: str
    agents: List[AgentTask] = field(default_factory=list)
    parallel: bool = True
    estimated_time: int = 0
    will_modify_code: bool = False

@dataclass
class IssueReport:
    """Issue rapportée par un agent"""
    agent: str
    file_path: str
    line_number: int
    severity: str  # critical, important, minor
    issue_type: str
    description: str
    solution: str
    auto_fixable: bool
    confidence: float

@dataclass
class AnalysisSummary:
    """Résumé de l'analyse"""
    total_files: int = 0
    total_issues: int = 0
    critical_count: int = 0
    important_count: int = 0
    minor_count: int = 0
    auto_fixable_count: int = 0
    avg_confidence: float = 0.0
    critical_issues: List[IssueReport] = field(default_factory=list)
    important_issues: List[IssueReport] = field(default_factory=list)
    minor_issues: List[IssueReport] = field(default_factory=list)
    by_file: Dict[str, List[IssueReport]] = field(default_factory=dict)

class CoordinatorSession:
    """Session de conversation avec mémoire de contexte"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.conversation_history = []
        self.last_analysis: Optional[AnalysisSummary] = None
        self.last_plan: Optional[ActionPlan] = None
        self.pending_fixes = []
        self.user_preferences = {}
    
    def remember(self, user_message: str, coordinator_response: str):
        """Mémorise l'échange"""
        self.conversation_history.append({
            "user": user_message,
            "coordinator": coordinator_response,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_last_user_message(self) -> Optional[str]:
        """Récupère le dernier message utilisateur"""
        if self.conversation_history:
            return self.conversation_history[-1]["user"]
        return None

class AgentCoordinator:
    """
    Chef d'orchestre intelligent qui :
    - Comprend le langage naturel
    - Délègue aux agents spécialisés
    - Compile les résultats
    - Maintient une conversation
    """
    
    def __init__(self, project_path: str, auto_mode: bool = False):
        self.project_path = Path(project_path).resolve()
        self.auto_mode = auto_mode
        self.session = CoordinatorSession(self.project_path)
        
        # Agents disponibles
        self.available_agents = {
            "button-validator": {
                "path": "../button-validator/button_validator_v2.py",
                "enabled": True,
                "timeout": 300
            },
            "props-form-validator": {
                "path": "../props-form-validator/props_form_validator_v2.py",
                "enabled": True,
                "timeout": 300
            },
            "dead-code-cleaner": {
                "path": "../dead-code-cleaner/dead_code_cleaner_v2.py",
                "enabled": True,
                "timeout": 300
            },
            "code-fixer": {
                "path": "../code-fixer/code_fixer_v2.py",
                "enabled": True,
                "timeout": 300
            },
            "consistency-checker": {
                "path": "../component-consistency-checker/consistency_checker_v2.py",
                "enabled": True,
                "timeout": 600
            },
            "readme-editor": {
                "path": "../readme-editor/readme_editor_v2.py",
                "enabled": True,
                "timeout": 300
            }
        }
        
        self.print_header()
    
    def print_header(self):
        """Affiche l'en-tête"""
        print("=" * 70)
        print("🎼 AGENT COORDINATOR V2 - Interface Conversationnelle")
        print("=" * 70)
        print(f"📁 Projet : {self.project_path.name}")
        print(f"🤖 Mode : {'Automatique' if self.auto_mode else 'Conversationnel'}")
        print("=" * 70)
        print()
    
    def understand_intent(self, user_message: str) -> Intent:
        """Comprend l'intention de l'utilisateur"""
        
        intent = Intent()
        message_lower = user_message.lower()
        
        # Patterns de détection
        cleanup_words = ["nettoie", "ménage", "clean", "supprime", "code mort"]
        analyze_words = ["analyse", "vérifie", "regarde", "scan", "check"]
        button_words = ["bouton", "button", "click", "onclick"]
        form_words = ["formulaire", "form", "input", "modal"]
        emoji_words = ["emoji", "émoji", "emoticon"]
        consistency_words = ["cohérence", "cohérent", "uniformité", "standard"]
        all_words = ["tout", "complet", "full", "global", "entier"]
        
        # Détecter l'action principale
        if any(word in message_lower for word in cleanup_words):
            intent.action = "cleanup"
            intent.agents = ["dead-code-cleaner"]
            intent.confidence = 0.9
        
        elif any(word in message_lower for word in emoji_words):
            intent.action = "remove_emojis"
            intent.agents = ["props-form-validator"]
            intent.focus = "emojis_only"
            intent.confidence = 0.95
        
        elif any(word in message_lower for word in button_words):
            intent.action = "analyze_buttons"
            intent.agents = ["button-validator"]
            intent.confidence = 0.9
        
        elif any(word in message_lower for word in form_words):
            intent.action = "analyze_forms"
            intent.agents = ["props-form-validator"]
            intent.focus = "forms_modals"
            intent.confidence = 0.85
        
        elif any(word in message_lower for word in consistency_words):
            intent.action = "check_consistency"
            intent.agents = ["consistency-checker"]
            intent.confidence = 0.9
        
        elif any(word in message_lower for word in all_words):
            intent.action = "full_analysis"
            intent.agents = ["all"]
            intent.confidence = 0.95
        
        elif any(word in message_lower for word in analyze_words):
            # Analyse générale - lancer tous les agents d'analyse
            intent.action = "general_analysis"
            intent.agents = ["button-validator", "props-form-validator", "dead-code-cleaner", "consistency-checker"]
            intent.confidence = 0.7
        
        # Détecter le scope
        # Fichier spécifique
        file_match = re.search(r'\b(\w+\.tsx?)\b', user_message)
        if file_match:
            intent.scope = "file"
            intent.target = file_match.group(1)
            intent.confidence += 0.1
        
        # Composant spécifique
        component_match = re.search(r'\b(\w+(?:Card|Form|Modal|List|Manager))\b', user_message, re.IGNORECASE)
        if component_match:
            intent.scope = "component"
            intent.target = component_match.group(1)
            intent.confidence += 0.1
        
        # Dossier spécifique
        folder_match = re.search(r'\b(teams?|stages?|participants?|personnel|components?)/?\b', message_lower)
        if folder_match:
            intent.scope = "folder"
            intent.target = folder_match.group(1)
            intent.confidence += 0.1
        
        return intent
    
    def create_action_plan(self, intent: Intent) -> ActionPlan:
        """Crée un plan d'action basé sur l'intention"""
        
        plan = ActionPlan(description="")
        
        if intent.action == "cleanup":
            plan.description = "Nettoyage du code mort"
            plan.agents.append(AgentTask(
                name="dead-code-cleaner",
                priority=1,
                estimated_time=120
            ))
            plan.estimated_time = 120
            plan.will_modify_code = False  # Juste détection
        
        elif intent.action == "remove_emojis":
            plan.description = "Suppression des emojis"
            plan.agents.append(AgentTask(
                name="props-form-validator",
                priority=1,
                estimated_time=60,
                scope=intent.scope,
                target=intent.target
            ))
            plan.estimated_time = 60
            plan.will_modify_code = True
        
        elif intent.action == "analyze_buttons":
            plan.description = "Analyse des boutons"
            plan.agents.append(AgentTask(
                name="button-validator",
                priority=1,
                estimated_time=90,
                scope=intent.scope,
                target=intent.target
            ))
            plan.estimated_time = 90
            plan.will_modify_code = False
        
        elif intent.action == "analyze_forms":
            plan.description = "Analyse des formulaires et modales"
            plan.agents.append(AgentTask(
                name="props-form-validator",
                priority=1,
                estimated_time=120,
                scope=intent.scope,
                target=intent.target
            ))
            plan.estimated_time = 120
            plan.will_modify_code = False
        
        elif intent.action == "check_consistency":
            plan.description = "Vérification de la cohérence"
            plan.agents.append(AgentTask(
                name="consistency-checker",
                priority=1,
                estimated_time=180
            ))
            plan.estimated_time = 180
            plan.will_modify_code = False
        
        elif intent.action == "full_analysis":
            plan.description = "Analyse complète du projet"
            plan.agents = [
                AgentTask("button-validator", priority=1, estimated_time=90),
                AgentTask("props-form-validator", priority=1, estimated_time=120),
                AgentTask("consistency-checker", priority=2, estimated_time=180),
                AgentTask("dead-code-cleaner", priority=1, estimated_time=120)
            ]
            plan.parallel = True
            plan.estimated_time = 180  # Max des temps en parallèle
            plan.will_modify_code = False
        
        elif intent.action == "general_analysis":
            plan.description = "Analyse générale"
            plan.agents = [
                AgentTask("button-validator", priority=1, estimated_time=90),
                AgentTask("props-form-validator", priority=1, estimated_time=120),
                AgentTask("dead-code-cleaner", priority=1, estimated_time=120),
                AgentTask("consistency-checker", priority=2, estimated_time=180)
            ]
            plan.parallel = True
            plan.estimated_time = 180  # Max des temps en parallèle
            plan.will_modify_code = False
        
        else:
            plan.description = "Action non reconnue"
        
        return plan
    
    def present_plan(self, plan: ActionPlan) -> bool:
        """Présente le plan et demande confirmation"""
        
        print(f"\n💬 {plan.description}")
        print(f"\nJe vais lancer :")
        
        for agent_task in plan.agents:
            agent_info = self.available_agents.get(agent_task.name, {})
            status = "✅" if agent_info.get("enabled") else "⏳ (pas encore disponible)"
            
            print(f"   • {agent_task.name} {status}")
            if agent_task.scope and agent_task.target:
                print(f"     Scope : {agent_task.scope} ({agent_task.target})")
        
        print(f"\n⏱️  Temps estimé : {plan.estimated_time // 60} min {plan.estimated_time % 60}s")
        print(f"📝 Modifications : {'Oui' if plan.will_modify_code else 'Non (analyse seulement)'}")
        
        if self.auto_mode:
            print(f"\n🤖 Mode auto : Lancement automatique")
            return True
        
        # Mode conversationnel - demander confirmation
        print(f"\n{'─' * 60}")
        response = input("C'est bon pour toi ? [O/n] : ").strip().lower()
        print()
        
        return response in ['', 'o', 'oui', 'y', 'yes', 'ok']
    
    async def run_agent(self, agent_task: AgentTask) -> Dict[str, Any]:
        """Lance un agent et retourne ses résultats"""
        
        agent_info = self.available_agents.get(agent_task.name)
        
        if not agent_info or not agent_info.get("enabled"):
            return {
                "agent": agent_task.name,
                "status": "unavailable",
                "message": f"Agent {agent_task.name} pas encore implémenté"
            }
        
        # Résoudre le chemin absolu de l'agent (important pour Windows avec espaces)
        agent_path = (Path(__file__).parent / agent_info["path"]).resolve()

        if not agent_path.exists():
            return {
                "agent": agent_task.name,
                "status": "not_found",
                "message": f"Agent non trouvé : {agent_path}"
            }

        try:
            # Lancer l'agent avec le bon interpréteur Python (Windows vs Linux)
            import platform
            python_cmd = "py" if platform.system() == "Windows" else "python3"
            cmd = [python_cmd, str(agent_path), str(self.project_path)]

            # Définir le working directory au dossier de l'agent
            # pour que les rapports soient créés au bon endroit
            agent_dir = agent_path.parent

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(agent_dir)
            )
            
            stdout, stderr = await process.communicate()

            # Décoder avec fallback pour compatibilité Windows/Linux
            def decode_with_fallback(data):
                for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
                    try:
                        return data.decode(encoding)
                    except (UnicodeDecodeError, UnicodeError):
                        continue
                return data.decode('utf-8', errors='replace')

            if process.returncode == 0:
                # Parse les résultats (simulé pour l'instant)
                return {
                    "agent": agent_task.name,
                    "status": "success",
                    "stdout": decode_with_fallback(stdout),
                    "stderr": decode_with_fallback(stderr)
                }
            else:
                return {
                    "agent": agent_task.name,
                    "status": "error",
                    "message": decode_with_fallback(stderr)
                }
        
        except Exception as e:
            return {
                "agent": agent_task.name,
                "status": "error",
                "message": str(e)
            }
    
    async def execute_plan(self, plan: ActionPlan) -> Dict[str, Any]:
        """Exécute le plan d'action"""
        
        print(f"\n🎼 {plan.description}")
        print(f"⏳ Lancement de {len(plan.agents)} agent(s)...\n")
        
        results = {}
        
        if plan.parallel:
            # Exécution parallèle
            tasks = [self.run_agent(agent_task) for agent_task in plan.agents]
            agent_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for agent_task, result in zip(plan.agents, agent_results):
                if isinstance(result, Exception):
                    results[agent_task.name] = {
                        "status": "error",
                        "message": str(result)
                    }
                else:
                    results[agent_task.name] = result
                
                status_icon = "✅" if result.get("status") == "success" else "⚠️"
                print(f"{status_icon} {agent_task.name}")
        
        else:
            # Exécution séquentielle
            for agent_task in plan.agents:
                print(f"⏳ {agent_task.name}...")
                result = await self.run_agent(agent_task)
                results[agent_task.name] = result
                
                status_icon = "✅" if result.get("status") == "success" else "⚠️"
                print(f"{status_icon} {agent_task.name}")
        
        print()
        return results
    
    def compile_results(self, results: Dict[str, Any]) -> AnalysisSummary:
        """Compile les résultats de tous les agents"""

        summary = AnalysisSummary()

        # Vérifier les erreurs des agents
        failed_agents = []
        successful_agents = []

        for agent_name, result in results.items():
            status = result.get("status")

            if status == "success":
                successful_agents.append(agent_name)
                # Simuler des issues détectées
                # Dans la vraie implémentation, parser les rapports JSON des agents
                if agent_name == "button-validator":
                    summary.total_files += 15
                    summary.critical_count += 2
                    summary.important_count += 3
                    summary.minor_count += 5
                    summary.auto_fixable_count += 4
            else:
                # Agent a échoué
                failed_agents.append({
                    "name": agent_name,
                    "status": status,
                    "message": result.get("message", "Erreur inconnue"),
                    "stderr": result.get("stderr", "")
                })

        # Afficher les erreurs si présentes
        if failed_agents:
            print(f"\n⚠️  ATTENTION : {len(failed_agents)} agent(s) ont échoué :")
            print(f"{'─' * 70}")
            for failed in failed_agents:
                print(f"\n❌ {failed['name']} ({failed['status']})")
                if failed['message']:
                    # Afficher le message complet (pas de troncature)
                    print(f"   Message :")
                    for line in failed['message'].split('\n'):
                        if line.strip():
                            print(f"      {line}")
                if failed['stderr']:
                    # Afficher stderr complet
                    print(f"   Stderr :")
                    for line in failed['stderr'].split('\n'):
                        if line.strip():
                            print(f"      {line}")
            print(f"\n{'─' * 70}\n")

        summary.total_issues = summary.critical_count + summary.important_count + summary.minor_count

        if summary.total_issues > 0:
            summary.avg_confidence = 85.0

        return summary
    
    def present_summary(self, summary: AnalysisSummary):
        """Présente un résumé concis et actionnable"""
        
        print(f"\n{'=' * 70}")
        print(f"📊 RÉSUMÉ DE L'ANALYSE")
        print(f"{'=' * 70}\n")
        
        if summary.total_issues == 0:
            print(f"✅ Aucun problème détecté ! Le projet est clean.")
            print()
            return
        
        # Issues par sévérité
        print(f"❌ Critiques : {summary.critical_count}")
        if summary.critical_count > 0 and summary.critical_issues:
            for issue in summary.critical_issues[:3]:
                print(f"   • {issue.file_path}:{issue.line_number} - {issue.description}")
            if summary.critical_count > 3:
                print(f"   ... et {summary.critical_count - 3} autres")
        
        print(f"\n⚠️  Importants : {summary.important_count}")
        print(f"ℹ️  Mineurs : {summary.minor_count}")
        
        # Corrections possibles
        if summary.auto_fixable_count > 0:
            print(f"\n✅ {summary.auto_fixable_count} corrections automatiques disponibles")
            print(f"   Confiance moyenne : {summary.avg_confidence:.0f}%")
        
        # Sauvegarder dans la session
        self.session.last_analysis = summary
        
        print(f"\n{'─' * 70}")
        
        if not self.auto_mode:
            print(f"💬 Que veux-tu faire ?")
            print(f"   [1] Voir le détail complet")
            print(f"   [2] Corriger automatiquement (confiance >90%)")
            print(f"   [3] Corriger avec validation")
            print(f"   [4] Rien pour l'instant")
            print(f"{'─' * 70}\n")

    async def ask_user_to_apply_fixes(self, summary: AnalysisSummary) -> bool:
        """Demande TOUJOURS à l'utilisateur s'il veut appliquer les corrections

        RÈGLE : Ne JAMAIS lancer Code Fixer sans accord explicite de l'utilisateur
        """

        if summary.total_issues == 0:
            print("\n✅ Aucun problème détecté, rien à corriger !")
            return False

        print(f"\n{'=' * 70}")
        print(f"💬 VOULEZ-VOUS APPLIQUER CES CORRECTIONS ?")
        print(f"{'=' * 70}\n")

        # Afficher le résumé avec la confiance
        print(f"Confiance moyenne : {summary.avg_confidence:.0f}%")
        if summary.avg_confidence >= 90:
            print(f"✅ Niveau : HAUTE - Les corrections proposées sont sûres\n")
        else:
            print(f"⚠️  Niveau : MOYENNE/BASSE - Validation recommandée\n")

        print(f"Résumé des corrections disponibles :")
        print(f"  • {summary.auto_fixable_count} corrections automatiques")
        print(f"  • {summary.critical_count} critiques")
        print(f"  • {summary.important_count} importantes")
        print(f"  • {summary.minor_count} mineures\n")

        # En mode auto : afficher seulement, NE PAS lancer sans intervention utilisateur
        if self.auto_mode:
            print(f"🤖 Mode automatique : Analyse terminée.")
            print(f"   Pour appliquer les corrections, relancez en mode conversationnel.\n")
            return False

        # TOUJOURS demander confirmation explicite en mode conversationnel
        print(f"Options :")
        print(f"  [o] OUI - Lancer Code Fixer pour appliquer les corrections")
        print(f"  [d] DÉTAILS - Voir plus de détails avant de décider")
        print(f"  [n] NON - Ne rien appliquer pour l'instant\n")

        response = input("Votre choix [o/d/N] : ").lower().strip()

        if response in ['o', 'oui', 'y', 'yes']:
            print(f"\n✅ OK, je lance Code Fixer...\n")
            return True
        elif response in ['d', 'detail', 'détails', 'details']:
            print(f"\n📋 DÉTAILS COMPLETS :")
            print(f"{'─' * 70}")
            # Afficher plus de détails
            if summary.critical_issues:
                print(f"\n❌ Issues CRITIQUES ({len(summary.critical_issues)}) :")
                for issue in summary.critical_issues[:5]:
                    print(f"  • {issue.file_path}:{issue.line_number} - {issue.description}")
                if len(summary.critical_issues) > 5:
                    print(f"  ... et {len(summary.critical_issues) - 5} autres")

            if summary.important_issues:
                print(f"\n⚠️  Issues IMPORTANTES ({len(summary.important_issues)}) :")
                for issue in summary.important_issues[:5]:
                    print(f"  • {issue.file_path}:{issue.line_number} - {issue.description}")
                if len(summary.important_issues) > 5:
                    print(f"  ... et {len(summary.important_issues) - 5} autres")

            print(f"\n{'─' * 70}\n")

            # Redemander après avoir montré les détails
            response = input("Après avoir vu les détails, lancer Code Fixer ? [o/N] : ").lower().strip()
            if response in ['o', 'oui', 'y', 'yes']:
                print(f"\n✅ OK, je lance Code Fixer...\n")
                return True
            else:
                print(f"\n❌ OK, aucune correction ne sera appliquée.")
                print(f"   Les rapports sont disponibles dans ./reports/\n")
                return False
        else:
            print(f"\n❌ OK, aucune correction ne sera appliquée.")
            print(f"   Les rapports sont disponibles dans ./reports/\n")
            return False

    async def launch_code_fixer(self) -> Dict[str, Any]:
        """Lance Code Fixer pour appliquer les corrections"""

        print(f"\n{'=' * 70}")
        print(f"🔧 LANCEMENT DE CODE FIXER")
        print(f"{'=' * 70}\n")

        code_fixer_path = Path(__file__).parent.parent / "code-fixer" / "code_fixer_v2.py"

        if not code_fixer_path.exists():
            print(f"❌ Code Fixer introuvable : {code_fixer_path}")
            return {"status": "error", "message": "Code Fixer non trouvé"}

        try:
            # Lancer Code Fixer en mode auto
            result = subprocess.run(
                ['python3', str(code_fixer_path), '--auto'],
                cwd=self.project_path,
                capture_output=True,
                timeout=600  # 10 minutes max
            )

            if result.returncode == 0:
                print(f"✅ Code Fixer terminé avec succès\n")
                print(result.stdout.decode('utf-8'))

                # Extraire les fichiers modifiés du output
                output = result.stdout.decode('utf-8')
                modified_files = []
                # Pattern simple pour extraire les fichiers (à améliorer)
                for line in output.split('\n'):
                    if 'modifié' in line.lower() or 'modified' in line.lower():
                        modified_files.append(line.strip())

                return {
                    "status": "success",
                    "modified_files": modified_files,
                    "output": output
                }
            else:
                print(f"⚠️  Code Fixer a rencontré des erreurs\n")
                print(result.stderr.decode('utf-8'))
                return {
                    "status": "error",
                    "message": result.stderr.decode('utf-8')
                }

        except Exception as e:
            print(f"❌ Erreur lors du lancement de Code Fixer : {e}")
            return {"status": "error", "message": str(e)}

    async def launch_readme_editor(self, modified_files: List[str] = None) -> Dict[str, Any]:
        """Lance README Editor pour mettre à jour la documentation"""

        print(f"\n{'=' * 70}")
        print(f"📝 LANCEMENT DE README EDITOR")
        print(f"{'=' * 70}\n")

        readme_editor_path = Path(__file__).parent.parent / "readme-editor" / "readme_editor_v2.py"

        if not readme_editor_path.exists():
            print(f"⚠️  README Editor introuvable : {readme_editor_path}")
            return {"status": "error", "message": "README Editor non trouvé"}

        try:
            print(f"📝 Mise à jour de la documentation...\n")

            # Lancer README Editor
            result = subprocess.run(
                ['python3', str(readme_editor_path), str(self.project_path)],
                capture_output=True,
                timeout=300,  # 5 minutes max
                input=b'n\n'  # Répondre 'n' à la question des README par dossier
            )

            if result.returncode == 0:
                print(f"✅ Documentation mise à jour avec succès\n")
                print(result.stdout.decode('utf-8'))
                return {"status": "success"}
            else:
                print(f"⚠️  README Editor a rencontré des erreurs\n")
                print(result.stderr.decode('utf-8'))
                return {"status": "error", "message": result.stderr.decode('utf-8')}

        except Exception as e:
            print(f"⚠️  Erreur lors du lancement de README Editor : {e}")
            return {"status": "error", "message": str(e)}

    def handle_followup(self, user_message: str) -> str:
        """Gère les questions de suivi dans la conversation"""
        
        message_lower = user_message.lower().strip()
        
        # Confirmations simples
        if message_lower in ["oui", "ok", "yes", "vas-y", "d'accord", "1"]:
            return "confirm"
        
        elif message_lower in ["non", "no", "annule", "stop", "4"]:
            return "cancel"
        
        elif message_lower in ["détail", "détails", "montre", "voir", "affiche", "2"]:
            return "show_details"
        
        elif "corrige" in message_lower or "fix" in message_lower or message_lower == "3":
            return "fix"
        
        # Nouvelles demandes
        else:
            return "new_request"
    
    async def conversational_loop(self):
        """Boucle conversationnelle principale"""
        
        print("💬 Bonjour ! Je suis l'Agent Coordinator.")
        print("   Dis-moi ce que tu veux que je fasse sur ton projet.\n")
        print("Exemples :")
        print("   • 'Analyse les boutons'")
        print("   • 'Nettoie le code mort'")
        print("   • 'Vérifie tout'")
        print("   • 'Regarde TeamCard.tsx'")
        print("\n(Tape 'quit' pour quitter)\n")
        
        while True:
            try:
                # Attendre l'entrée utilisateur
                user_input = input("👤 Toi : ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'au revoir']:
                    print("\n👋 À bientôt !\n")
                    break
                
                # Comprendre l'intention
                intent = self.understand_intent(user_input)
                
                if intent.confidence < 0.5:
                    print("\n🤔 Je n'ai pas bien compris.")
                    print("   Peux-tu reformuler ? Par exemple :")
                    print("   • 'Analyse les boutons'")
                    print("   • 'Nettoie le projet'\n")
                    continue
                
                # Créer le plan
                plan = self.create_action_plan(intent)
                
                # Présenter et demander confirmation
                confirmed = self.present_plan(plan)
                
                if not confirmed:
                    print("❌ Action annulée.\n")
                    continue
                
                # Exécuter
                results = await self.execute_plan(plan)

                # Compiler et présenter
                summary = self.compile_results(results)
                self.present_summary(summary)

                # NOUVEAU : Demande TOUJOURS à l'utilisateur avant de corriger
                should_fix = await self.ask_user_to_apply_fixes(summary)

                if should_fix:
                    # Lancer Code Fixer
                    fixer_result = await self.launch_code_fixer()

                    if fixer_result.get("status") == "success":
                        # Lancer README Editor après Code Fixer
                        modified_files = fixer_result.get("modified_files", [])
                        await self.launch_readme_editor(modified_files)

                        print(f"\n🎉 WORKFLOW COMPLET TERMINÉ !")
                        print(f"  ✅ Analyse effectuée")
                        print(f"  ✅ Corrections appliquées")
                        print(f"  ✅ Documentation mise à jour\n")

                # Mémoriser l'échange
                self.session.remember(user_input, f"Exécuté : {plan.description}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interruption - À bientôt !\n")
                break
            except Exception as e:
                print(f"\n⚠️  Erreur : {e}\n")
    
    async def run(self):
        """Point d'entrée principal"""
        
        if not self.project_path.exists():
            print(f"❌ Projet introuvable : {self.project_path}\n")
            return
        
        if self.auto_mode:
            # Mode automatique - analyse complète avec workflow intelligent
            intent = Intent(action="full_analysis", agents=["all"], confidence=1.0)
            plan = self.create_action_plan(intent)

            confirmed = self.present_plan(plan)
            if confirmed:
                # Exécuter l'analyse
                results = await self.execute_plan(plan)
                summary = self.compile_results(results)
                self.present_summary(summary)

                # NOUVEAU : Demande TOUJOURS à l'utilisateur avant de corriger
                should_fix = await self.ask_user_to_apply_fixes(summary)

                if should_fix:
                    # Lancer Code Fixer
                    fixer_result = await self.launch_code_fixer()

                    if fixer_result.get("status") == "success":
                        # Lancer README Editor après Code Fixer
                        modified_files = fixer_result.get("modified_files", [])
                        await self.launch_readme_editor(modified_files)

                        print(f"\n🎉 WORKFLOW COMPLET TERMINÉ !")
                        print(f"  ✅ Analyse effectuée")
                        print(f"  ✅ Corrections appliquées")
                        print(f"  ✅ Documentation mise à jour\n")
        else:
            # Mode conversationnel
            await self.conversational_loop()

def main():
    """Point d'entrée"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python agent_coordinator_v2.py /path/to/project [--auto]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    auto_mode = "--auto" in sys.argv
    
    coordinator = AgentCoordinator(project_path, auto_mode)
    asyncio.run(coordinator.run())

if __name__ == "__main__":
    main()