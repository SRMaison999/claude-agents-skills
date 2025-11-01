#!/usr/bin/env python3
"""
Consensus Analyzer V2 - Consensus par Fichier

PROBLÈME IDENTIFIÉ:
Les agents sont SPÉCIALISÉS et détectent des types de problèmes DIFFÉRENTS.
→ props-form-validator détecte des emojis
→ dead-code-cleaner détecte des console.log
→ button-validator détecte des missing handlers
→ Ils ne trouvent JAMAIS le MÊME problème au MÊME endroit

NOUVELLE STRATÉGIE:
Au lieu de chercher "2 agents trouvent le même emoji ligne 42",
on cherche "2 agents trouvent des problèmes dans le même fichier".

Si 2+ agents pensent qu'un fichier a des problèmes, alors:
→ TOUTES les corrections auto-fixables de ce fichier sont validées
→ Confiance accrue (plusieurs agents confirment que le fichier nécessite attention)

Règles de consensus V2:
1. Grouper les issues par FICHIER (pas par ligne)
2. Compter combien d'agents différents ont détecté des problèmes dans chaque fichier
3. Si ≥2 agents → fichier validé → appliquer TOUTES corrections auto-fixables du fichier
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple
from pathlib import Path
from collections import defaultdict

@dataclass
class Issue:
    """Issue détectée par un agent"""
    agent: str
    file_path: str
    line_number: int
    severity: str
    issue_type: str
    description: str
    solution: str
    old_code: str = ""
    new_code: str = ""
    confidence: float = 0.0
    auto_fixable: bool = False

@dataclass
class FileConsensus:
    """Consensus pour un fichier"""
    file_path: str
    agents_count: int
    agents: List[str]
    total_issues: int
    auto_fixable_issues: List[Issue]
    all_issues: List[Issue]

@dataclass
class ConsensusResultV2:
    """Résultat du consensus V2"""
    validated_files: List[FileConsensus]
    rejected_files: List[str]
    validated_issues: List[Issue]
    rejected_issues: List[Issue]

    def get_statistics(self) -> Dict[str, int]:
        return {
            "validated_files": len(self.validated_files),
            "rejected_files": len(self.rejected_files),
            "total_validated_issues": len(self.validated_issues),
            "total_rejected_issues": len(self.rejected_issues),
            "auto_fixable_validated": sum(1 for i in self.validated_issues if i.auto_fixable),
            "files_2_agents": sum(1 for f in self.validated_files if f.agents_count == 2),
            "files_3_agents": sum(1 for f in self.validated_files if f.agents_count == 3),
            "files_4_plus": sum(1 for f in self.validated_files if f.agents_count >= 4)
        }

class ConsensusAnalyzerV2:
    """
    Analyseur de consensus V2 - Consensus par fichier

    Stratégie adaptée aux agents spécialisés qui détectent
    des types de problèmes différents
    """

    def __init__(self, min_agents: int = 2):
        """
        Args:
            min_agents: Nombre minimum d'agents requis pour valider un fichier (défaut: 2)
        """
        self.min_agents = min_agents
        self.result: ConsensusResultV2 = None

    def find_consensus(self, all_issues: List[Issue]) -> ConsensusResultV2:
        """
        Trouve les fichiers validés par consensus

        Args:
            all_issues: Toutes les issues de tous les agents

        Returns:
            ConsensusResultV2 avec fichiers validés et issues associées
        """

        # Grouper par fichier
        issues_by_file: Dict[str, Dict[str, List[Issue]]] = defaultdict(lambda: defaultdict(list))

        for issue in all_issues:
            issues_by_file[issue.file_path][issue.agent].append(issue)

        # Analyser chaque fichier
        validated_files = []
        rejected_files = []
        validated_issues = []
        rejected_issues = []

        for file_path, agents_issues in issues_by_file.items():
            agents = list(agents_issues.keys())
            agents_count = len(agents)

            # Collecter toutes les issues du fichier
            all_file_issues = []
            auto_fixable_file_issues = []

            for agent, issues in agents_issues.items():
                for issue in issues:
                    all_file_issues.append(issue)
                    if issue.auto_fixable:
                        auto_fixable_file_issues.append(issue)

            # Décision de consensus
            if agents_count >= self.min_agents:
                # VALIDÉ : 2+ agents ont détecté des problèmes dans ce fichier
                file_consensus = FileConsensus(
                    file_path=file_path,
                    agents_count=agents_count,
                    agents=agents,
                    total_issues=len(all_file_issues),
                    auto_fixable_issues=auto_fixable_file_issues,
                    all_issues=all_file_issues
                )
                validated_files.append(file_consensus)
                validated_issues.extend(auto_fixable_file_issues)
            else:
                # REJETÉ : 1 seul agent a détecté des problèmes
                rejected_files.append(file_path)
                rejected_issues.extend(auto_fixable_file_issues)

        self.result = ConsensusResultV2(
            validated_files=validated_files,
            rejected_files=rejected_files,
            validated_issues=validated_issues,
            rejected_issues=rejected_issues
        )

        return self.result

    def print_consensus_report(self):
        """Affiche un rapport du consensus V2"""
        if not self.result:
            print("⚠️  Aucun résultat de consensus disponible")
            return

        stats = self.result.get_statistics()

        print(f"\n{'=' * 80}")
        print(f"🤝 CONSENSUS V2 - VALIDATION PAR FICHIER")
        print(f"{'=' * 80}\n")

        print(f"📁 Fichiers validés par consensus : {stats['validated_files']}")
        if stats['files_2_agents'] > 0:
            print(f"   • 2 agents d'accord : {stats['files_2_agents']} fichiers")
        if stats['files_3_agents'] > 0:
            print(f"   • 3 agents d'accord : {stats['files_3_agents']} fichiers")
        if stats['files_4_plus'] > 0:
            print(f"   • 4+ agents d'accord : {stats['files_4_plus']} fichiers")
        print()

        print(f"✅ Issues validées : {stats['total_validated_issues']}")
        print(f"   • Auto-fixable : {stats['auto_fixable_validated']}")
        print()

        print(f"❌ Fichiers rejetés (1 seul agent) : {stats['rejected_files']}")
        print(f"   • Issues rejetées : {stats['total_rejected_issues']}")
        print()

        if stats['validated_files'] > 0:
            print(f"💡 Stratégie : Si 2+ agents détectent des problèmes dans un fichier,")
            print(f"   TOUTES les corrections auto-fixables du fichier sont validées")
            print(f"   (même si les agents détectent des types différents)")
        else:
            print(f"⚠️  Aucun fichier validé par consensus")
            print(f"   Chaque fichier n'a été analysé que par 1 seul agent")

        print(f"{'=' * 80}\n")

        # Top fichiers avec le plus d'agents
        if self.result.validated_files:
            print(f"📊 TOP 10 FICHIERS (par nombre d'agents d'accord) :\n")
            sorted_files = sorted(self.result.validated_files,
                                 key=lambda f: (f.agents_count, len(f.auto_fixable_issues)),
                                 reverse=True)[:10]

            for file_consensus in sorted_files:
                print(f"   {file_consensus.file_path}")
                print(f"      • Agents : {', '.join(file_consensus.agents)} ({file_consensus.agents_count})")
                print(f"      • Issues auto-fixable : {len(file_consensus.auto_fixable_issues)}")
                print()


if __name__ == "__main__":
    # Test du consensus analyzer V2

    test_issues = [
        # Fichier 1 : Détecté par 3 agents (emoji + console + consistency)
        Issue(agent="props-form-validator", file_path="src/App.tsx", line_number=42,
              severity="critical", issue_type="emoji_detected",
              description="Emoji in code", solution="Remove emoji",
              confidence=100.0, auto_fixable=True),

        Issue(agent="dead-code-cleaner", file_path="src/App.tsx", line_number=10,
              severity="minor", issue_type="console_log",
              description="Console.log forgotten", solution="Remove console.log",
              confidence=100.0, auto_fixable=True),

        Issue(agent="consistency-checker", file_path="src/App.tsx", line_number=20,
              severity="important", issue_type="consistency_issue",
              description="Inconsistent styling", solution="Standardize",
              confidence=70.0, auto_fixable=False),

        # Fichier 2 : Détecté par 1 seul agent (sera rejeté)
        Issue(agent="props-form-validator", file_path="src/utils/helper.ts", line_number=5,
              severity="critical", issue_type="emoji_detected",
              description="Emoji found", solution="Remove",
              confidence=100.0, auto_fixable=True),

        # Fichier 3 : Détecté par 2 agents (validé)
        Issue(agent="dead-code-cleaner", file_path="src/components/Button.tsx", line_number=15,
              severity="minor", issue_type="unused_import",
              description="Unused import", solution="Remove import",
              confidence=95.0, auto_fixable=True),

        Issue(agent="button-validator", file_path="src/components/Button.tsx", line_number=20,
              severity="critical", issue_type="missing_handler",
              description="Missing onClick", solution="Add handler",
              confidence=50.0, auto_fixable=False),
    ]

    analyzer = ConsensusAnalyzerV2(min_agents=2)
    result = analyzer.find_consensus(test_issues)

    print(f"Test Results:")
    print(f"  Validated files: {len(result.validated_files)}")
    print(f"  Rejected files: {len(result.rejected_files)}")
    print(f"  Validated issues: {len(result.validated_issues)}")
    print()

    analyzer.print_consensus_report()

    print(f"📋 DÉTAILS DES FICHIERS VALIDÉS :\n")
    for fc in result.validated_files:
        print(f"✅ {fc.file_path}")
        print(f"   Agents : {', '.join(fc.agents)} ({fc.agents_count} agents)")
        print(f"   Issues auto-fixable validées : {len(fc.auto_fixable_issues)}")
        for issue in fc.auto_fixable_issues:
            print(f"      • [{issue.agent}] {issue.issue_type} (ligne {issue.line_number})")
        print()
