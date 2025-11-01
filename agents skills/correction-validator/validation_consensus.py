#!/usr/bin/env python3
"""
Validation Consensus - Comparaison des 2 validateurs

Compare les validations de 2 validateurs indépendants
et ne garde que les corrections approuvées par LES DEUX
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ConsensusValidation:
    """Correction validée par consensus (2 validateurs d'accord)"""
    file_path: str
    line_number: int
    issue_type: str
    description: str
    solution: str

    # Consensus des 2 validateurs
    validator1_approved: bool
    validator2_approved: bool
    validator1_confidence: float
    validator2_confidence: float
    average_confidence: float

    # Source
    source_agent: str

    # Décision finale
    consensus_approved: bool

class ValidationConsensus:
    """
    Compare les validations de 2 validateurs indépendants
    """

    def __init__(self, session_path: Path):
        self.session_path = session_path
        self.analysis_dir = session_path / "1-ANALYSIS"

        self.validator1_data: Dict[str, Any] = {}
        self.validator2_data: Dict[str, Any] = {}

        self.consensus_validations: List[ConsensusValidation] = []
        self.approved_corrections: List[Dict[str, Any]] = []
        self.rejected_corrections: List[Dict[str, Any]] = []

    def load_validator_reports(self) -> bool:
        """Charge les rapports des 2 validateurs"""

        validator1_file = self.analysis_dir / "validator-1.json"
        validator2_file = self.analysis_dir / "validator-2.json"

        if not validator1_file.exists():
            print(f"❌ Rapport validateur 1 introuvable : {validator1_file}")
            return False

        if not validator2_file.exists():
            print(f"❌ Rapport validateur 2 introuvable : {validator2_file}")
            return False

        # Charger validateur 1
        with open(validator1_file, 'r', encoding='utf-8') as f:
            self.validator1_data = json.load(f)

        # Charger validateur 2
        with open(validator2_file, 'r', encoding='utf-8') as f:
            self.validator2_data = json.load(f)

        print(f"✅ Rapports des 2 validateurs chargés\n")
        return True

    def find_matching_validation(self, val1: Dict[str, Any], validations2: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Trouve la validation correspondante dans le validateur 2"""

        for val2 in validations2:
            # Match sur fichier + ligne + type
            if (val1["file_path"] == val2["file_path"] and
                val1["line_number"] == val2["line_number"] and
                val1["issue_type"] == val2["issue_type"]):
                return val2

        return None

    def compare_validations(self):
        """Compare les validations des 2 validateurs"""

        print(f"\n{'=' * 80}")
        print(f"🤝 CONSENSUS ENTRE LES 2 VALIDATEURS")
        print(f"{'=' * 80}\n")

        validations1 = self.validator1_data.get("validations", [])
        validations2 = self.validator2_data.get("validations", [])

        print(f"📊 Validateur 1 : {len(validations1)} évaluations")
        print(f"📊 Validateur 2 : {len(validations2)} évaluations\n")

        # Comparer chaque validation du validateur 1 avec le validateur 2
        both_approved = 0
        both_rejected = 0
        disagreement = 0

        for val1 in validations1:
            val2 = self.find_matching_validation(val1, validations2)

            if not val2:
                # Correction évaluée par validateur 1 mais pas validateur 2 (bizarre)
                continue

            # Calculer la confiance moyenne
            avg_confidence = (val1["validation_confidence"] + val2["validation_confidence"]) / 2

            # Décision de consensus
            both_approve = val1["approved"] and val2["approved"]

            consensus = ConsensusValidation(
                file_path=val1["file_path"],
                line_number=val1["line_number"],
                issue_type=val1["issue_type"],
                description=val1["original_description"],
                solution=val1["proposed_solution"],
                validator1_approved=val1["approved"],
                validator2_approved=val2["approved"],
                validator1_confidence=val1["validation_confidence"],
                validator2_confidence=val2["validation_confidence"],
                average_confidence=avg_confidence,
                source_agent=val1["source_agent"],
                consensus_approved=both_approve
            )

            self.consensus_validations.append(consensus)

            # Statistiques
            if val1["approved"] and val2["approved"]:
                both_approved += 1
                self.approved_corrections.append({
                    "file": val1["file_path"],
                    "line": val1["line_number"],
                    "type": val1["issue_type"],
                    "description": val1["original_description"],
                    "solution": val1["proposed_solution"],
                    "confidence": avg_confidence,
                    "auto_fixable": True,
                    "agent": val1["source_agent"]
                })
            elif not val1["approved"] and not val2["approved"]:
                both_rejected += 1
            else:
                disagreement += 1
                self.rejected_corrections.append({
                    "file": val1["file_path"],
                    "line": val1["line_number"],
                    "type": val1["issue_type"],
                    "reason": f"Désaccord (V1: {val1['approved']}, V2: {val2['approved']})"
                })

        print(f"✅ Les 2 approuvent   : {both_approved}")
        print(f"❌ Les 2 rejettent   : {both_rejected}")
        print(f"⚠️  Désaccord         : {disagreement}")
        print()

        if disagreement > 0:
            print(f"💡 En cas de désaccord → REJET (sécurité)")
            print()

        return both_approved

    def save_consensus_report(self):
        """Sauvegarde le rapport de consensus"""

        consensus_file = self.analysis_dir / "consensus-validated-corrections.json"

        report_data = {
            "consensus_type": "dual_validation",
            "description": "Corrections validées par les 2 validateurs indépendants",
            "timestamp": datetime.now().isoformat(),
            "consensus_enabled": True,
            "min_validators_required": 2,
            "statistics": {
                "total_evaluated": len(self.consensus_validations),
                "both_approved": len(self.approved_corrections),
                "both_rejected": sum(1 for c in self.consensus_validations
                                    if not c.validator1_approved and not c.validator2_approved),
                "disagreement": sum(1 for c in self.consensus_validations
                                   if c.validator1_approved != c.validator2_approved),
                "auto_fixable": len(self.approved_corrections)
            },
            "issues": self.approved_corrections
        }

        with open(consensus_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Consensus sauvegardé : consensus-validated-corrections.json")
        print(f"   → {len(self.approved_corrections)} corrections approuvées par les 2 validateurs\n")

    def print_summary(self):
        """Affiche un résumé détaillé"""

        print(f"{'=' * 80}")
        print(f"📋 RÉSUMÉ DU CONSENSUS DE VALIDATION")
        print(f"{'=' * 80}\n")

        approved = len(self.approved_corrections)
        rejected = len(self.rejected_corrections)

        print(f"✅ Corrections approuvées (consensus) : {approved}")
        print(f"❌ Corrections rejetées (désaccord)   : {rejected}")
        print()

        if approved > 0:
            print(f"💡 Seules les {approved} corrections validées par LES DEUX validateurs")
            print(f"   seront appliquées par Code Fixer")
            print()

            # Grouper par type
            by_type = {}
            for corr in self.approved_corrections:
                issue_type = corr["type"]
                by_type[issue_type] = by_type.get(issue_type, 0) + 1

            print(f"📊 Par type :")
            for issue_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
                print(f"   • {issue_type}: {count}")
            print()

        print(f"{'=' * 80}\n")

    def run(self):
        """Exécute l'analyse de consensus"""

        if not self.load_validator_reports():
            return False

        approved_count = self.compare_validations()

        if approved_count > 0:
            self.save_consensus_report()

        self.print_summary()

        return True


def main():
    """Point d'entrée"""
    import sys
    from pathlib import Path

    if len(sys.argv) < 2:
        print("Usage: python validation_consensus.py /path/to/session")
        sys.exit(1)

    session_path = Path(sys.argv[1])

    if not session_path.exists():
        print(f"❌ Session introuvable : {session_path}")
        sys.exit(1)

    consensus = ValidationConsensus(session_path)
    success = consensus.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
