#!/usr/bin/env python3
"""
Consensus Analyzer - Système de consensus multi-agents

Analyse les corrections proposées par plusieurs agents et ne retient
que celles sur lesquelles AU MOINS 2 agents sont d'accord.

Règles de consensus :
1. Même fichier
2. Même ligne (± 2 lignes de tolérance)
3. Même type de problème (emoji, console.log, unused_import, etc.)

Objectif : Éviter les faux positifs et s'assurer de la pertinence des corrections
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
class ConsensusIssue:
    """Issue validée par consensus multi-agents"""
    file_path: str
    line_number: int
    issue_type: str
    description: str
    solution: str
    severity: str
    old_code: str = ""
    new_code: str = ""
    confidence: float = 0.0
    auto_fixable: bool = False

    # Consensus
    agreed_by: List[str] = field(default_factory=list)
    consensus_level: int = 0  # Nombre d'agents d'accord

    # Source issues
    source_issues: List[Issue] = field(default_factory=list)

class ConsensusAnalyzer:
    """
    Analyseur de consensus multi-agents

    Compare les issues détectées par différents agents et identifie
    celles qui ont un consensus (au moins 2 agents d'accord).
    """

    def __init__(self, line_tolerance: int = 2):
        """
        Args:
            line_tolerance: Tolérance en nombre de lignes pour matcher (défaut: 2)
        """
        self.line_tolerance = line_tolerance
        self.consensus_issues: List[ConsensusIssue] = []
        self.rejected_issues: List[Issue] = []

    def normalize_issue_type(self, issue_type: str) -> str:
        """Normalise le type d'issue pour faciliter la comparaison"""
        issue_type_lower = issue_type.lower()

        # Emojis
        if 'emoji' in issue_type_lower:
            return 'emoji'

        # Console.log
        if 'console' in issue_type_lower:
            return 'console_log'

        # Imports
        if 'import' in issue_type_lower:
            return 'unused_import'

        # Commented code
        if 'comment' in issue_type_lower:
            return 'commented_code'

        # Button issues
        if 'button' in issue_type_lower:
            return 'button_issue'

        # Props issues
        if 'prop' in issue_type_lower:
            return 'props_issue'

        # Consistency
        if 'consistency' in issue_type_lower or 'cohérence' in issue_type_lower:
            return 'consistency'

        return issue_type_lower

    def issues_match(self, issue1: Issue, issue2: Issue) -> bool:
        """
        Détermine si deux issues correspondent au même problème

        Critères :
        1. Même fichier
        2. Ligne proche (± tolerance)
        3. Même type normalisé
        """
        # Même fichier
        if issue1.file_path != issue2.file_path:
            return False

        # Ligne proche
        line_diff = abs(issue1.line_number - issue2.line_number)
        if line_diff > self.line_tolerance:
            return False

        # Même type
        type1 = self.normalize_issue_type(issue1.issue_type)
        type2 = self.normalize_issue_type(issue2.issue_type)

        return type1 == type2

    def find_consensus(self, all_issues: List[Issue], min_agents: int = 2) -> Tuple[List[ConsensusIssue], List[Issue]]:
        """
        Trouve les issues qui ont un consensus

        Args:
            all_issues: Toutes les issues de tous les agents
            min_agents: Nombre minimum d'agents requis pour consensus (défaut: 2)

        Returns:
            (consensus_issues, rejected_issues)
        """

        # Grouper par fichier pour optimiser
        issues_by_file: Dict[str, List[Issue]] = defaultdict(list)
        for issue in all_issues:
            issues_by_file[issue.file_path].append(issue)

        # Issues déjà traitées (garder les objets eux-mêmes)
        processed: Set[id] = set()
        consensus_list: List[ConsensusIssue] = []

        # Parcourir chaque fichier
        for file_path, file_issues in issues_by_file.items():
            # Parcourir chaque issue
            for i, issue1 in enumerate(file_issues):
                if id(issue1) in processed:
                    continue

                # Trouver toutes les issues qui matchent
                matching_issues = [issue1]
                matching_agents = {issue1.agent}

                for j, issue2 in enumerate(file_issues):
                    if i == j or id(issue2) in processed:
                        continue

                    # Vérifier si elles correspondent
                    if self.issues_match(issue1, issue2):
                        # Éviter les doublons du même agent
                        if issue2.agent not in matching_agents:
                            matching_issues.append(issue2)
                            matching_agents.add(issue2.agent)

                # Si consensus atteint
                if len(matching_agents) >= min_agents:
                    # Créer une issue de consensus
                    consensus = self.create_consensus_issue(matching_issues)
                    consensus_list.append(consensus)

                    # Marquer comme traitées (utiliser id() pour identifier l'objet)
                    for match in matching_issues:
                        processed.add(id(match))

        # Identifier les issues rejetées (sans consensus)
        rejected = [issue for issue in all_issues
                   if id(issue) not in processed]

        self.consensus_issues = consensus_list
        self.rejected_issues = rejected

        return consensus_list, rejected

    def create_consensus_issue(self, matching_issues: List[Issue]) -> ConsensusIssue:
        """
        Crée une issue de consensus à partir des issues matchantes

        Stratégie de fusion :
        - file_path, line_number, issue_type : issue principale (première)
        - description : la plus détaillée
        - solution : la plus détaillée
        - confidence : moyenne
        - auto_fixable : True si au moins une issue est auto-fixable
        - severity : la plus élevée
        """

        # Issue principale (première)
        primary = matching_issues[0]

        # Description la plus détaillée
        descriptions = [i.description for i in matching_issues]
        best_description = max(descriptions, key=len)

        # Solution la plus détaillée
        solutions = [i.solution for i in matching_issues]
        best_solution = max(solutions, key=len)

        # Confidence moyenne
        avg_confidence = sum(i.confidence for i in matching_issues) / len(matching_issues)

        # Auto-fixable si au moins une issue l'est
        is_auto_fixable = any(i.auto_fixable for i in matching_issues)

        # Severity la plus élevée
        severity_order = {'critical': 3, 'important': 2, 'minor': 1}
        severities = [i.severity for i in matching_issues]
        best_severity = max(severities, key=lambda s: severity_order.get(s, 0))

        # Old/New code (priorité à celui qui en a)
        old_code = next((i.old_code for i in matching_issues if i.old_code), "")
        new_code = next((i.new_code for i in matching_issues if i.new_code), "")

        return ConsensusIssue(
            file_path=primary.file_path,
            line_number=primary.line_number,
            issue_type=self.normalize_issue_type(primary.issue_type),
            description=best_description,
            solution=best_solution,
            severity=best_severity,
            old_code=old_code,
            new_code=new_code,
            confidence=avg_confidence,
            auto_fixable=is_auto_fixable,
            agreed_by=[i.agent for i in matching_issues],
            consensus_level=len(matching_issues),
            source_issues=matching_issues
        )

    def get_statistics(self) -> Dict[str, int]:
        """Retourne les statistiques du consensus"""
        return {
            "total_consensus": len(self.consensus_issues),
            "total_rejected": len(self.rejected_issues),
            "consensus_2_agents": sum(1 for i in self.consensus_issues if i.consensus_level == 2),
            "consensus_3_agents": sum(1 for i in self.consensus_issues if i.consensus_level == 3),
            "consensus_4_plus": sum(1 for i in self.consensus_issues if i.consensus_level >= 4),
            "auto_fixable": sum(1 for i in self.consensus_issues if i.auto_fixable)
        }

    def print_consensus_report(self):
        """Affiche un rapport du consensus"""
        stats = self.get_statistics()

        print(f"\n{'=' * 80}")
        print(f"🤝 ANALYSE DE CONSENSUS MULTI-AGENTS")
        print(f"{'=' * 80}\n")

        print(f"✅ Issues validées par consensus : {stats['total_consensus']}")
        print(f"   • 2 agents d'accord : {stats['consensus_2_agents']}")
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
            print(f"   (minimum 2 agents d'accord)")
        else:
            print(f"⚠️  Aucun consensus trouvé")
            print(f"   Les agents ne sont pas d'accord sur les corrections")

        print(f"{'=' * 80}\n")


if __name__ == "__main__":
    # Test du consensus analyzer

    # Simuler des issues de différents agents
    test_issues = [
        # Emoji détecté par 3 agents
        Issue(agent="button-validator", file_path="src/App.tsx", line_number=42,
              severity="critical", issue_type="emoji_detected",
              description="Emoji in button text", solution="Remove emoji",
              confidence=95.0, auto_fixable=True),

        Issue(agent="props-form-validator", file_path="src/App.tsx", line_number=42,
              severity="critical", issue_type="emoji_in_code",
              description="Emoji found", solution="Remove emoji",
              confidence=98.0, auto_fixable=True),

        Issue(agent="dead-code-cleaner", file_path="src/App.tsx", line_number=43,  # ligne proche
              severity="minor", issue_type="emoji_detected",
              description="Emoji in code", solution="Remove",
              confidence=90.0, auto_fixable=True),

        # Console.log détecté par 2 agents
        Issue(agent="dead-code-cleaner", file_path="src/utils/debug.js", line_number=10,
              severity="minor", issue_type="console_log",
              description="Console.log forgotten", solution="Remove console.log",
              confidence=100.0, auto_fixable=True),

        Issue(agent="props-form-validator", file_path="src/utils/debug.js", line_number=10,
              severity="minor", issue_type="debug_console",
              description="Debug console left", solution="Remove",
              confidence=95.0, auto_fixable=True),

        # Issue unique (sera rejetée)
        Issue(agent="consistency-checker", file_path="src/components/Header.tsx", line_number=20,
              severity="important", issue_type="consistency_issue",
              description="Inconsistent styling", solution="Standardize",
              confidence=70.0, auto_fixable=False),
    ]

    analyzer = ConsensusAnalyzer(line_tolerance=2)
    consensus, rejected = analyzer.find_consensus(test_issues, min_agents=2)

    print(f"Test Results:")
    print(f"  Consensus issues: {len(consensus)}")
    print(f"  Rejected issues: {len(rejected)}")
    print()

    for issue in consensus:
        print(f"✅ {issue.file_path}:{issue.line_number}")
        print(f"   Type: {issue.issue_type}")
        print(f"   Agreed by: {', '.join(issue.agreed_by)} ({issue.consensus_level} agents)")
        print(f"   Auto-fixable: {issue.auto_fixable}")
        print()

    analyzer.print_consensus_report()
