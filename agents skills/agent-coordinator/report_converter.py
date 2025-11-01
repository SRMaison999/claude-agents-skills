#!/usr/bin/env python3
"""
Report Converter - Convertit les rapports Markdown en JSON structuré

Lit les rapports Markdown générés par les agents V2
et les convertit en JSON pour Code Fixer et Agent Coordinator V3
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

def read_file_with_fallback(file_path: Path) -> str:
    """Lit un fichier avec gestion multi-encodage"""
    for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    return ""

def convert_button_validator_report(markdown_path: Path) -> Dict[str, Any]:
    """Convertit le rapport du button-validator"""

    content = read_file_with_fallback(markdown_path)
    if not content:
        return {}

    # Extraire les statistiques
    stats = {
        "total_issues": 0,
        "critical": 0,
        "important": 0,
        "minor": 0,
        "auto_fixable": 0
    }

    # Boutons analysés
    match = re.search(r'🔘 \*\*Boutons analysés\*\*\s*:\s*(\d+)', content)
    if match:
        stats["buttons_analyzed"] = int(match.group(1))

    # Problèmes critiques
    match = re.search(r'\*\*Problèmes critiques\*\*\s*:\s*(\d+)', content)
    if match:
        stats["critical"] = int(match.group(1))

    # Problèmes importants
    match = re.search(r'\*\*Problèmes importants\*\*\s*:\s*(\d+)', content)
    if match:
        stats["important"] = int(match.group(1))

    # Améliorations suggérées
    match = re.search(r'\*\*Améliorations suggérées\*\*\s*:\s*(\d+)', content)
    if match:
        stats["minor"] = int(match.group(1))

    # Auto-correction
    match = re.search(r'Auto-correction[^:]*:\s*(\d+)', content)
    if match:
        stats["auto_fixable"] = int(match.group(1))

    stats["total_issues"] = stats["critical"] + stats["important"] + stats["minor"]

    # Extraire les issues (section PROBLÈMES CRITIQUES)
    issues = []

    # Pattern pour les issues critiques
    issue_pattern = r'###\s*\d+\.\s*([^-]+)\s*-\s*`([^:]+):(\d+)`\s*\n\*\*Description\*\*\s*:\s*([^\n]+)\n.*?\*\*Solution\*\*\s*:\s*([^\n]+)'

    for match in re.finditer(issue_pattern, content, re.DOTALL):
        issue_type = match.group(1).strip()
        file_path = match.group(2).strip()
        line_number = int(match.group(3))
        description = match.group(4).strip()
        solution = match.group(5).strip()

        issues.append({
            "file": file_path,
            "line": line_number,
            "severity": "critical",
            "type": issue_type,
            "description": description,
            "solution": solution,
            "old_code": "",
            "new_code": "",
            "confidence": 50.0,  # Par défaut, validation requise
            "auto_fixable": False
        })

    return {
        "agent": "button-validator",
        "timestamp": markdown_path.stem.split('-')[-1] if '-' in markdown_path.stem else "",
        "statistics": stats,
        "issues": issues
    }

def convert_props_form_validator_report(markdown_path: Path) -> Dict[str, Any]:
    """Convertit le rapport du props-form-validator"""

    content = read_file_with_fallback(markdown_path)
    if not content:
        return {}

    # Extraire les statistiques
    stats = {
        "total_issues": 0,
        "critical": 0,
        "important": 0,
        "minor": 0,
        "auto_fixable": 0
    }

    # Issues totales
    match = re.search(r'\*\*Issues totales\*\*\s*:\s*(\d+)', content)
    if match:
        stats["total_issues"] = int(match.group(1))

    # CRITIQUES
    match = re.search(r'\*\*CRITIQUES\*\*\s*:\s*(\d+)', content)
    if match:
        stats["critical"] = int(match.group(1))

    # IMPORTANTES
    match = re.search(r'\*\*IMPORTANTES\*\*\s*:\s*(\d+)', content)
    if match:
        stats["important"] = int(match.group(1))

    # MINEURES
    match = re.search(r'\*\*MINEURES\*\*\s*:\s*(\d+)', content)
    if match:
        stats["minor"] = int(match.group(1))

    # Corrections automatiques
    match = re.search(r'Corrections automatiques\s*\((\d+)\s+issues?\)', content)
    if match:
        stats["auto_fixable"] = int(match.group(1))

    # Extraire les issues auto-fixables (emojis principalement)
    issues = []

    # Pattern pour les corrections auto
    issue_pattern = r'\*\*([^:]+):(\d+)\*\*\s*\[(\w+)\]\s*\n-\s*Type\s*:\s*([^\n]+)\n-\s*Problème\s*:\s*([^\n]+)\n-\s*Solution\s*:\s*([^\n]+)\n-\s*Confiance\s*:\s*(\d+(?:\.\d+)?)%'

    for match in re.finditer(issue_pattern, content):
        file_path = match.group(1).strip()
        line_number = int(match.group(2))
        severity_tag = match.group(3).strip().lower()
        issue_type = match.group(4).strip()
        description = match.group(5).strip()
        solution = match.group(6).strip()
        confidence = float(match.group(7))

        severity_map = {"critical": "critical", "important": "important", "info": "minor"}
        severity = severity_map.get(severity_tag, "minor")

        issues.append({
            "file": file_path,
            "line": line_number,
            "severity": severity,
            "type": issue_type,
            "description": description,
            "solution": solution,
            "old_code": "",
            "new_code": "",
            "confidence": confidence,
            "auto_fixable": confidence >= 90.0
        })

    return {
        "agent": "props-form-validator",
        "timestamp": markdown_path.stem.split('-')[-1] if '-' in markdown_path.stem else "",
        "statistics": stats,
        "issues": issues
    }

def convert_dead_code_cleaner_report(markdown_path: Path) -> Dict[str, Any]:
    """Convertit le rapport du dead-code-cleaner"""

    content = read_file_with_fallback(markdown_path)
    if not content:
        return {}

    # Extraire les statistiques
    stats = {
        "total_issues": 0,
        "critical": 0,
        "important": 0,
        "minor": 0,
        "auto_fixable": 0
    }

    # Issues totales
    match = re.search(r'\*\*Issues totales\*\*\s*:\s*(\d+)', content)
    if match:
        stats["total_issues"] = int(match.group(1))
        stats["minor"] = int(match.group(1))  # Tout est "minor"

    # Suppressions automatiques
    match = re.search(r'Suppressions automatiques\s*\((\d+)\s+issues?\)', content)
    if match:
        stats["auto_fixable"] = int(match.group(1))

    # Extraire les issues par type
    issues = []

    # Console Log
    console_pattern = r'-\s+([^:]+):(\d+)\s+-\s+Console\.log oublié'
    for match in re.finditer(console_pattern, content):
        file_path = match.group(1).strip()
        line_number = int(match.group(2))

        issues.append({
            "file": file_path,
            "line": line_number,
            "severity": "minor",
            "type": "console_log",
            "description": "Console.log oublié",
            "solution": "Supprimer console.log()",
            "old_code": "",
            "new_code": "",
            "confidence": 100.0,
            "auto_fixable": True
        })

    # Unused Import
    import_pattern = r'-\s+([^:]+):(\d+)\s+-\s+Import\s+\'([^\']+)\'\s+non utilisé'
    for match in re.finditer(import_pattern, content):
        file_path = match.group(1).strip()
        line_number = int(match.group(2))
        import_name = match.group(3).strip()

        issues.append({
            "file": file_path,
            "line": line_number,
            "severity": "minor",
            "type": "unused_import",
            "description": f"Import '{import_name}' non utilisé",
            "solution": f"Supprimer '{import_name}' de l'import",
            "old_code": "",
            "new_code": "",
            "confidence": 95.0,
            "auto_fixable": True
        })

    return {
        "agent": "dead-code-cleaner",
        "timestamp": markdown_path.stem.split('-')[-1] if '-' in markdown_path.stem else "",
        "statistics": stats,
        "issues": issues[:stats["auto_fixable"]]  # Limiter aux auto-fixables
    }

def convert_consistency_checker_report(markdown_path: Path) -> Dict[str, Any]:
    """Convertit le rapport du consistency-checker"""

    content = read_file_with_fallback(markdown_path)
    if not content:
        return {}

    # Extraire les statistiques
    stats = {
        "total_issues": 0,
        "critical": 0,
        "important": 0,
        "minor": 0,
        "auto_fixable": 0
    }

    # Incohérences détectées
    match = re.search(r'\*\*Incohérences détectées\*\*\s*:\s*(\d+)', content)
    if match:
        stats["total_issues"] = int(match.group(1))
        stats["important"] = int(match.group(1))  # Tout est "important"

    # Pas de corrections auto pour le consistency checker (trop complexe)
    stats["auto_fixable"] = 0

    issues = []

    # Les issues de cohérence nécessitent une intervention humaine
    # On pourrait extraire plus de détails si nécessaire

    return {
        "agent": "consistency-checker",
        "timestamp": markdown_path.stem.split('-')[-1] if '-' in markdown_path.stem else "",
        "statistics": stats,
        "issues": issues
    }

def convert_report(markdown_path: Path, agent_name: str) -> Optional[Dict[str, Any]]:
    """Convertit un rapport Markdown en JSON selon l'agent"""

    converters = {
        "button-validator": convert_button_validator_report,
        "props-form-validator": convert_props_form_validator_report,
        "dead-code-cleaner": convert_dead_code_cleaner_report,
        "consistency-checker": convert_consistency_checker_report
    }

    converter = converters.get(agent_name)
    if not converter:
        return None

    return converter(markdown_path)

def save_json_report(data: Dict[str, Any], output_path: Path):
    """Sauvegarde le rapport JSON"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Test
    import sys

    if len(sys.argv) < 3:
        print("Usage: python report_converter.py <markdown_file> <agent_name>")
        sys.exit(1)

    markdown_file = Path(sys.argv[1])
    agent_name = sys.argv[2]

    data = convert_report(markdown_file, agent_name)

    if data:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"Erreur: impossible de convertir le rapport pour {agent_name}")
        sys.exit(1)
