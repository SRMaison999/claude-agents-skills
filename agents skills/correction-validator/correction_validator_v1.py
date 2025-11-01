#!/usr/bin/env python3
"""
Correction Validator V1 - Agent de Validation des Corrections

RÔLE:
Valider les corrections proposées par les agents d'analyse.
Agit comme un "peer reviewer" indépendant.

WORKFLOW:
1. Lit tous les rapports d'analyse JSON de la session
2. Pour chaque correction proposée, évalue :
   - Est-ce vraiment une erreur ?
   - La solution proposée est-elle appropriée ?
   - Y a-t-il des risques ou effets secondaires ?
   - Peut-on améliorer la solution ?
3. Génère un rapport de validation JSON

USAGE:
    python correction_validator_v1.py /path/to/project --session /path/to/session
    python correction_validator_v1.py /path/to/project --session /path/to/session --validator-id 1
"""

import os
import sys
import io
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Forcer UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

@dataclass
class CorrectionValidation:
    """Validation d'une correction proposée"""
    # Identifiant de la correction
    source_agent: str
    file_path: str
    line_number: int
    issue_type: str
    original_description: str
    proposed_solution: str

    # Évaluation du validateur
    is_real_error: bool              # Est-ce vraiment une erreur ?
    solution_appropriate: bool       # La solution est-elle appropriée ?
    validation_confidence: float     # Confiance 0-100
    risk_level: str                  # "low", "medium", "high"

    # Commentaires du validateur
    validator_comments: str
    suggested_improvement: str = ""

    # Décision finale
    approved: bool = False           # Approuvé par ce validateur

class CorrectionValidatorV1:
    """
    Agent de validation des corrections

    Évalue de manière indépendante si les corrections proposées
    sont pertinentes et appropriées
    """

    def __init__(self, project_path: Path, session_path: Path, validator_id: int = 1):
        self.project_path = project_path
        self.session_path = session_path
        self.validator_id = validator_id
        self.validations: List[CorrectionValidation] = []

        self.analysis_dir = session_path / "1-ANALYSIS"

    def load_analysis_reports(self) -> List[Dict[str, Any]]:
        """Charge tous les rapports d'analyse"""

        if not self.analysis_dir.exists():
            print(f"❌ Dossier d'analyse introuvable : {self.analysis_dir}")
            return []

        # Charger tous les rapports sauf consensus
        json_files = [f for f in self.analysis_dir.glob("*.json")
                     if f.name not in ["consensus-issues.json", "validator-1.json", "validator-2.json"]]

        print(f"📄 Chargement de {len(json_files)} rapports d'analyse...\n")

        all_issues = []
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                agent_name = data.get("agent", "unknown")

                for issue in data.get("issues", []):
                    # Ne valider que les issues avec corrections proposées
                    if issue.get("solution") and issue.get("solution").strip():
                        all_issues.append({
                            "agent": agent_name,
                            "issue": issue
                        })

            except Exception as e:
                print(f"⚠️  Erreur lecture {json_file.name} : {e}")

        print(f"✅ {len(all_issues)} corrections à valider\n")
        return all_issues

    def validate_emoji_removal(self, issue: Dict[str, Any]) -> CorrectionValidation:
        """Valide une correction de suppression d'emoji"""

        file_path = issue.get("file", "")
        description = issue.get("description", "")

        # Déterminer si c'est vraiment une erreur
        is_real_error = True  # Les emojis sont généralement à éviter dans le code

        # Vérifier le contexte du fichier
        is_debug_file = "debug" in file_path.lower()
        is_test_file = "test" in file_path.lower() or "spec" in file_path.lower()

        # Les emojis dans les fichiers de debug sont moins critiques
        if is_debug_file:
            risk_level = "low"
            validation_confidence = 85.0
            solution_appropriate = True
            comments = "Emoji dans fichier de debug. Suppression recommandée mais non critique."
            approved = True
        elif is_test_file:
            risk_level = "low"
            validation_confidence = 70.0
            solution_appropriate = True
            comments = "Emoji dans fichier de test. Impact limité."
            approved = True
        else:
            risk_level = "low"
            validation_confidence = 95.0
            solution_appropriate = True
            comments = "Emoji détecté dans code production. Suppression appropriée."
            approved = True

        return CorrectionValidation(
            source_agent=issue.get("agent", "unknown"),
            file_path=file_path,
            line_number=issue.get("line", 0),
            issue_type=issue.get("type", ""),
            original_description=description,
            proposed_solution=issue.get("solution", ""),
            is_real_error=is_real_error,
            solution_appropriate=solution_appropriate,
            validation_confidence=validation_confidence,
            risk_level=risk_level,
            validator_comments=comments,
            approved=approved
        )

    def validate_console_log_removal(self, issue: Dict[str, Any]) -> CorrectionValidation:
        """Valide une correction de suppression de console.log"""

        file_path = issue.get("file", "")
        description = issue.get("description", "").lower()

        # Vérifier si c'est un vrai console.log de debug
        is_debug_log = "debug" in description or "forgotten" in description

        # Vérifier le contexte
        is_debug_file = "debug" in file_path.lower()

        if is_debug_file:
            # Console.log dans un fichier de debug est normal
            is_real_error = False
            solution_appropriate = False
            validation_confidence = 90.0
            risk_level = "low"
            comments = "Console.log dans fichier de debug. GARDER - c'est intentionnel."
            approved = False
        elif is_debug_log:
            # Console.log oublié dans code production
            is_real_error = True
            solution_appropriate = True
            validation_confidence = 95.0
            risk_level = "low"
            comments = "Console.log de debug oublié. Suppression appropriée."
            approved = True
        else:
            # Incertain
            is_real_error = True
            solution_appropriate = True
            validation_confidence = 70.0
            risk_level = "medium"
            comments = "Console.log détecté. Vérifier s'il est intentionnel."
            approved = False  # Besoin de vérification manuelle

        return CorrectionValidation(
            source_agent=issue.get("agent", "unknown"),
            file_path=file_path,
            line_number=issue.get("line", 0),
            issue_type=issue.get("type", ""),
            original_description=issue.get("description", ""),
            proposed_solution=issue.get("solution", ""),
            is_real_error=is_real_error,
            solution_appropriate=solution_appropriate,
            validation_confidence=validation_confidence,
            risk_level=risk_level,
            validator_comments=comments,
            approved=approved
        )

    def validate_unused_import(self, issue: Dict[str, Any]) -> CorrectionValidation:
        """Valide une correction de suppression d'import inutilisé"""

        # Import inutilisé est généralement safe à supprimer
        is_real_error = True
        solution_appropriate = True
        validation_confidence = 85.0
        risk_level = "low"
        comments = "Import inutilisé. Suppression appropriée pour réduire bundle size."
        approved = True

        return CorrectionValidation(
            source_agent=issue.get("agent", "unknown"),
            file_path=issue.get("file", ""),
            line_number=issue.get("line", 0),
            issue_type=issue.get("type", ""),
            original_description=issue.get("description", ""),
            proposed_solution=issue.get("solution", ""),
            is_real_error=is_real_error,
            solution_appropriate=solution_appropriate,
            validation_confidence=validation_confidence,
            risk_level=risk_level,
            validator_comments=comments,
            approved=approved
        )

    def validate_correction(self, agent: str, issue: Dict[str, Any]) -> CorrectionValidation:
        """Valide une correction proposée selon son type"""

        issue_type = issue.get("type", "").lower()

        # Router vers le validateur approprié selon le type
        if "emoji" in issue_type:
            return self.validate_emoji_removal(issue)
        elif "console" in issue_type:
            return self.validate_console_log_removal(issue)
        elif "import" in issue_type:
            return self.validate_unused_import(issue)
        else:
            # Type non reconnu - validation conservative
            return CorrectionValidation(
                source_agent=agent,
                file_path=issue.get("file", ""),
                line_number=issue.get("line", 0),
                issue_type=issue.get("type", ""),
                original_description=issue.get("description", ""),
                proposed_solution=issue.get("solution", ""),
                is_real_error=False,
                solution_appropriate=False,
                validation_confidence=0.0,
                risk_level="high",
                validator_comments=f"Type '{issue_type}' non reconnu. Validation manuelle requise.",
                approved=False
            )

    def run_validation(self):
        """Exécute la validation de toutes les corrections"""

        print(f"\n{'=' * 80}")
        print(f"🔍 CORRECTION VALIDATOR #{self.validator_id}")
        print(f"{'=' * 80}\n")

        # Charger les rapports d'analyse
        all_issues = self.load_analysis_reports()

        if not all_issues:
            print("⚠️  Aucune correction à valider\n")
            return

        print(f"⏳ Validation de {len(all_issues)} corrections...\n")

        # Valider chaque correction
        for item in all_issues:
            agent = item["agent"]
            issue = item["issue"]

            # Ajouter l'agent dans l'issue pour le validateur
            issue["agent"] = agent

            validation = self.validate_correction(agent, issue)
            self.validations.append(validation)

        # Statistiques
        approved_count = sum(1 for v in self.validations if v.approved)
        rejected_count = len(self.validations) - approved_count

        print(f"\n{'=' * 80}")
        print(f"📊 RÉSULTATS DE LA VALIDATION #{self.validator_id}")
        print(f"{'=' * 80}\n")
        print(f"✅ Corrections approuvées : {approved_count}")
        print(f"❌ Corrections rejetées   : {rejected_count}")
        print(f"📊 Total évalué          : {len(self.validations)}")
        print()

        # Sauvegarder le rapport
        self.save_validation_report()

    def save_validation_report(self):
        """Sauvegarde le rapport de validation en JSON"""

        report_file = self.analysis_dir / f"validator-{self.validator_id}.json"

        report_data = {
            "validator": f"correction-validator-{self.validator_id}",
            "timestamp": datetime.now().isoformat(),
            "project": str(self.project_path),
            "statistics": {
                "total_evaluated": len(self.validations),
                "approved": sum(1 for v in self.validations if v.approved),
                "rejected": sum(1 for v in self.validations if not v.approved),
                "high_confidence": sum(1 for v in self.validations if v.validation_confidence >= 90),
                "medium_confidence": sum(1 for v in self.validations if 70 <= v.validation_confidence < 90),
                "low_confidence": sum(1 for v in self.validations if v.validation_confidence < 70)
            },
            "validations": [asdict(v) for v in self.validations]
        }

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Rapport de validation sauvegardé : validator-{self.validator_id}.json\n")


def main():
    """Point d'entrée"""
    import argparse

    parser = argparse.ArgumentParser(description="Correction Validator V1")
    parser.add_argument("project_path", help="Chemin vers le projet")
    parser.add_argument("--session", required=True, help="Chemin vers la session")
    parser.add_argument("--validator-id", type=int, default=1, help="ID du validateur (1 ou 2)")

    args = parser.parse_args()

    project_path = Path(args.project_path)
    session_path = Path(args.session)

    if not project_path.exists():
        print(f"❌ Projet introuvable : {project_path}")
        sys.exit(1)

    if not session_path.exists():
        print(f"❌ Session introuvable : {session_path}")
        sys.exit(1)

    validator = CorrectionValidatorV1(project_path, session_path, args.validator_id)
    validator.run_validation()


if __name__ == "__main__":
    main()
