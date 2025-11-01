#!/usr/bin/env python3
"""
Script de debug pour analyser pourquoi le consensus ne trouve pas de correspondances

Usage:
    python consensus_debug.py /path/to/session/1-ANALYSIS
"""

import sys
import json
from pathlib import Path
from collections import defaultdict

def analyze_session(analysis_dir):
    """Analyse les rapports d'une session pour comprendre le consensus"""

    analysis_path = Path(analysis_dir)

    if not analysis_path.exists():
        print(f"❌ Dossier introuvable : {analysis_path}")
        return

    # Charger tous les rapports JSON (sauf consensus)
    json_files = [f for f in analysis_path.glob("*.json") if f.name != "consensus-issues.json"]

    print(f"📊 ANALYSE DE {len(json_files)} RAPPORTS\n")
    print("=" * 80)

    all_issues = []
    stats_by_agent = defaultdict(lambda: {"total": 0, "auto_fixable": 0, "types": defaultdict(int)})

    # Charger et analyser chaque rapport
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            agent_name = data.get("agent", "unknown")
            issues = data.get("issues", [])

            print(f"\n🤖 {agent_name}")
            print(f"   Total issues : {len(issues)}")

            auto_fixable_count = 0
            type_counts = defaultdict(int)

            for issue in issues:
                issue_type = issue.get("type", "unknown")
                is_auto_fixable = issue.get("auto_fixable", False)

                type_counts[issue_type] += 1

                if is_auto_fixable:
                    auto_fixable_count += 1
                    all_issues.append({
                        "agent": agent_name,
                        "file": issue.get("file", ""),
                        "line": issue.get("line", 0),
                        "type": issue_type,
                        "auto_fixable": True
                    })

            print(f"   Auto-fixable : {auto_fixable_count}")
            print(f"   Types principaux :")
            for issue_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"      • {issue_type}: {count}")

            stats_by_agent[agent_name]["total"] = len(issues)
            stats_by_agent[agent_name]["auto_fixable"] = auto_fixable_count
            stats_by_agent[agent_name]["types"] = dict(type_counts)

        except Exception as e:
            print(f"⚠️  Erreur lecture {json_file.name}: {e}")

    print(f"\n{'=' * 80}")
    print(f"\n📋 RÉSUMÉ GLOBAL")
    print(f"Total issues auto-fixable : {len(all_issues)}")

    # Analyser les correspondances potentielles
    print(f"\n🔍 ANALYSE DES CORRESPONDANCES POTENTIELLES\n")

    # Grouper par fichier
    issues_by_file = defaultdict(list)
    for issue in all_issues:
        issues_by_file[issue["file"]].append(issue)

    print(f"Fichiers avec issues auto-fixable : {len(issues_by_file)}")

    # Chercher les fichiers avec plusieurs agents
    multi_agent_files = {file: issues for file, issues in issues_by_file.items()
                         if len(set(i["agent"] for i in issues)) >= 2}

    print(f"Fichiers analysés par ≥2 agents : {len(multi_agent_files)}")

    if multi_agent_files:
        print(f"\n📁 FICHIERS AVEC POTENTIEL DE CONSENSUS :\n")
        for file, issues in sorted(multi_agent_files.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            agents = set(i["agent"] for i in issues)
            print(f"   {file}")
            print(f"      Agents : {', '.join(agents)}")
            print(f"      Issues : {len(issues)}")

            # Grouper par type
            types = defaultdict(list)
            for issue in issues:
                types[issue["type"]].append(issue)

            # Afficher les types présents
            print(f"      Types :")
            for issue_type, type_issues in types.items():
                type_agents = set(i["agent"] for i in type_issues)
                print(f"         • {issue_type}: {len(type_issues)} ({', '.join(type_agents)})")
            print()
    else:
        print(f"\n⚠️  AUCUN FICHIER ANALYSÉ PAR PLUSIEURS AGENTS")
        print(f"   → Chaque agent analyse des fichiers différents")
        print(f"   → Consensus impossible\n")

        print(f"🔍 RÉPARTITION DES FICHIERS PAR AGENT :\n")
        files_by_agent = defaultdict(set)
        for issue in all_issues:
            files_by_agent[issue["agent"]].add(issue["file"])

        for agent, files in files_by_agent.items():
            print(f"   {agent}: {len(files)} fichiers")
            # Afficher quelques exemples
            for file in sorted(files)[:3]:
                print(f"      • {file}")
            if len(files) > 3:
                print(f"      ... et {len(files) - 3} autres")
            print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python consensus_debug.py /path/to/session/1-ANALYSIS")
        sys.exit(1)

    analyze_session(sys.argv[1])
