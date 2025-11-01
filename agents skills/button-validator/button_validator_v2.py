#!/usr/bin/env python3
"""
Button Validator V2 - Learning Edition
Agent intelligent avec auto-détection et apprentissage continu

Usage: python button_validator_v2.py [project_path]
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
from collections import Counter

@dataclass
class ButtonIssue:
    """Représente un problème détecté sur un bouton"""
    file_path: str
    line_number: int
    severity: str  # "critical", "important", "minor"
    issue_type: str
    code_snippet: str
    description: str
    solution: str
    auto_fixable: bool
    confidence: float = 0.0  # 0-100

@dataclass
class ButtonInfo:
    """Informations sur un bouton détecté"""
    file_path: str
    line_number: int
    button_type: str  # "html_button", "component_button", "icon_button", "clickable_element"
    handler: str
    classes: str
    text_content: str
    is_functional: bool
    issues: List[ButtonIssue] = field(default_factory=list)
    code_snippet: str = ""

class ButtonValidatorLearning:
    """
    Agent intelligent d'analyse de boutons avec apprentissage continu
    """
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.buttons: List[ButtonInfo] = []
        self.issues: List[ButtonIssue] = []
        
        # Auto-détection du stack
        self.stack = self.detect_project_stack()
        self.structure = self.analyze_project_structure()
        
        # Chargement de la mémoire
        project_hash = self.get_project_hash()
        self.project_memory = self.load_project_memory(project_hash)
        self.project_hash = project_hash
        
        # Génération des patterns de détection adaptés
        self.button_patterns = self.generate_button_patterns(self.stack)
        
        # Affichage initial
        self.print_header()
    
    def print_header(self):
        """Affiche l'en-tête de l'analyse"""
        print("="*70)
        print("🧠 Button Validator V2 - Learning Edition")
        print("="*70)
        print(f"📁 Projet : {self.project_path.name}")
        print(f"🔧 Stack : {self.stack['framework']} + {self.stack['css_framework']}")
        print(f"🧠 Analyse #{self.project_memory.get('scan_count', 0) + 1}")
        
        # Afficher l'état d'apprentissage
        scan_count = self.project_memory.get('scan_count', 0)
        if scan_count == 0:
            print(f"🌱 État : DÉCOUVERTE (mode apprentissage)")
        elif scan_count < 5:
            print(f"🌿 État : CROISSANCE (confiance en construction)")
        elif scan_count < 10:
            print(f"🌳 État : MATURITÉ (corrections partiellement autonomes)")
        else:
            print(f"🎓 État : EXPERT (haute autonomie)")
        
        print("="*70)
    
    def get_project_hash(self) -> str:
        """Génère un hash unique pour identifier le projet"""
        project_str = str(self.project_path)
        return hashlib.md5(project_str.encode()).hexdigest()[:12]
    
    def detect_project_stack(self) -> Dict[str, Any]:
        """Détecte automatiquement le stack technologique du projet"""
        
        package_json_path = self.project_path / "package.json"
        
        stack = {
            "framework": "unknown",
            "language": "javascript",
            "ui_libraries": [],
            "icon_libraries": [],
            "css_framework": None,
            "state_management": [],
            "build_tool": None
        }
        
        if not package_json_path.exists():
            print("⚠️  package.json non trouvé - Utilisation des valeurs par défaut")
            return stack
        
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                pkg = json.load(f)
        except Exception as e:
            print(f"⚠️  Erreur lecture package.json : {e}")
            return stack
        
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        
        # Détecter le framework principal
        if "react" in deps:
            stack["framework"] = "react"
            stack["language"] = "typescript" if "typescript" in deps or "@types/react" in deps else "javascript"
        elif "vue" in deps:
            stack["framework"] = "vue"
            stack["language"] = "typescript" if "typescript" in deps else "javascript"
        elif "@angular/core" in deps:
            stack["framework"] = "angular"
            stack["language"] = "typescript"
        elif "svelte" in deps:
            stack["framework"] = "svelte"
        elif "next" in deps:
            stack["framework"] = "nextjs"
            stack["language"] = "typescript"
        
        # Détecter les librairies UI
        ui_libs_map = {
            "@mui/material": "material-ui",
            "antd": "ant-design",
            "@chakra-ui/react": "chakra-ui",
            "@headlessui/react": "headlessui",
            "@radix-ui/react": "radix-ui",
            "react-bootstrap": "bootstrap",
            "@mantine/core": "mantine"
        }
        
        for dep, lib_name in ui_libs_map.items():
            if dep in deps:
                stack["ui_libraries"].append(lib_name)
        
        # Détecter les librairies d'icônes
        icon_libs_map = {
            "lucide-react": "lucide",
            "react-icons": "react-icons",
            "@heroicons/react": "heroicons",
            "@fortawesome/react-fontawesome": "font-awesome"
        }
        
        for dep, lib_name in icon_libs_map.items():
            if dep in deps:
                stack["icon_libraries"].append(lib_name)
        
        # Détecter le framework CSS
        if "tailwindcss" in deps:
            stack["css_framework"] = "tailwind"
        elif "@emotion/react" in deps or "@emotion/styled" in deps:
            stack["css_framework"] = "emotion"
        elif "styled-components" in deps:
            stack["css_framework"] = "styled-components"
        
        # Détecter state management
        state_libs = {
            "zustand": "zustand",
            "redux": "redux",
            "@reduxjs/toolkit": "redux-toolkit",
            "mobx": "mobx",
            "recoil": "recoil",
            "jotai": "jotai"
        }
        
        for dep, lib_name in state_libs.items():
            if dep in deps:
                stack["state_management"].append(lib_name)
        
        # Détecter build tool
        if "vite" in deps:
            stack["build_tool"] = "vite"
        elif "webpack" in deps:
            stack["build_tool"] = "webpack"
        elif "@turbo/gen" in deps:
            stack["build_tool"] = "turbopack"
        
        return stack
    
    def analyze_project_structure(self) -> Dict[str, Any]:
        """Analyse la structure du projet pour trouver les dossiers importants"""
        
        structure = {
            "components_dir": None,
            "src_dir": None,
            "file_extensions": []
        }
        
        # Chercher src/
        if (self.project_path / "src").exists():
            structure["src_dir"] = "src"
            
            # Chercher components/
            if (self.project_path / "src" / "components").exists():
                structure["components_dir"] = "src/components"
            elif (self.project_path / "src" / "app").exists():
                structure["components_dir"] = "src/app"
        elif (self.project_path / "app").exists():
            structure["components_dir"] = "app"
        elif (self.project_path / "components").exists():
            structure["components_dir"] = "components"
        
        return structure
    
    def load_project_memory(self, project_hash: str) -> Dict[str, Any]:
        """Charge ou crée la mémoire spécifique à ce projet"""
        
        memory_dir = Path("brain/projects") / project_hash
        memory_file = memory_dir / "memory.json"
        
        if memory_file.exists():
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    memory = json.load(f)
                return memory
            except Exception as e:
                print(f"⚠️  Erreur chargement mémoire : {e}")
        
        # Créer nouvelle mémoire
        memory_dir.mkdir(parents=True, exist_ok=True)
        memory = {
            "project_path": str(self.project_path),
            "project_hash": project_hash,
            "created_at": datetime.now().isoformat(),
            "scan_count": 0,
            "patterns": {},
            "preferences": {},
            "corrections_history": [],
            "confidence_scores": {},
            "pattern_buffer": []
        }
        
        return memory
    
    def save_project_memory(self):
        """Sauvegarde la mémoire du projet"""
        
        memory_dir = Path("brain/projects") / self.project_hash
        memory_file = memory_dir / "memory.json"
        
        memory_dir.mkdir(parents=True, exist_ok=True)
        
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.project_memory, f, indent=2, ensure_ascii=False)
    
    def generate_button_patterns(self, stack: Dict[str, Any]) -> Dict[str, List[str]]:
        """Génère les patterns de détection selon le stack détecté"""
        
        patterns = {
            "html_buttons": [
                r'<button\s+([^>]*)>',
                r'<input\s+type=["\']button["\']',
                r'<input\s+type=["\']submit["\']'
            ],
            "component_buttons": [],
            "clickable_elements": [
                r'<(\w+)\s+([^>]*onClick[^>]*)>'
            ],
            "icon_buttons": []
        }
        
        # Adapter selon UI libraries
        if "material-ui" in stack["ui_libraries"]:
            patterns["component_buttons"].extend([
                r'<Button\s+', r'<IconButton\s+', r'<Fab\s+'
            ])
        
        if "ant-design" in stack["ui_libraries"]:
            patterns["component_buttons"].append(r'<Button\s+')
        
        if "chakra-ui" in stack["ui_libraries"]:
            patterns["component_buttons"].extend([
                r'<Button\s+', r'<IconButton\s+'
            ])
        
        # Patterns d'icônes
        if "lucide" in stack["icon_libraries"]:
            patterns["icon_buttons"].append(
                r'<(Trash|Plus|Edit|X|Check|Save|Upload|Download|ArrowRight|ArrowLeft|ChevronRight|ChevronLeft|Settings|User|Search)\w*\s+([^>]*onClick)'
            )
        
        if "react-icons" in stack["icon_libraries"]:
            patterns["icon_buttons"].append(
                r'<(Fa|Md|Ai|Bs|Io|Fi|Gi|Hi|Im|Ri|Si|Ti|Vsc|Wi|Cg|Di)\w+\s+([^>]*onClick)'
            )
        
        return patterns
    
    def find_files(self) -> List[Path]:
        """Trouve tous les fichiers à analyser"""
        
        components_dir = self.structure.get("components_dir")
        if not components_dir:
            components_dir = "src"
        
        search_path = self.project_path / components_dir
        
        if not search_path.exists():
            # Fallback : chercher dans tout le projet
            search_path = self.project_path
        
        extensions = [".tsx", ".jsx", ".ts", ".js"]
        files = []
        
        for ext in extensions:
            found = list(search_path.rglob(f"*{ext}"))
            files.extend(found)
        
        # Exclure tests et node_modules
        files = [
            f for f in files 
            if ".test." not in str(f) 
            and ".spec." not in str(f)
            and "node_modules" not in str(f)
            and ".next" not in str(f)
            and "dist" not in str(f)
        ]
        
        return files
    
    def scan_file(self, file_path: Path) -> List[ButtonInfo]:
        """Scanne un fichier pour détecter les boutons"""
        
        buttons = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Scanner avec tous les patterns
            for pattern_type, pattern_list in self.button_patterns.items():
                for pattern in pattern_list:
                    for match in re.finditer(pattern, content, re.MULTILINE):
                        line_num = content[:match.start()].count('\n') + 1
                        line = lines[line_num - 1] if line_num <= len(lines) else ""
                        
                        button = self.extract_button_info(
                            file_path, line_num, line, match, pattern_type
                        )
                        if button:
                            buttons.append(button)
        
        except Exception as e:
            # Silencieux pour les erreurs de lecture (binaires, etc.)
            pass
        
        return buttons
    
    def extract_button_info(self, file_path: Path, line_num: int, 
                           line: str, match, pattern_type: str) -> Optional[ButtonInfo]:
        """Extrait les informations d'un bouton détecté"""
        
        code_snippet = match.group(0)[:100]  # Limiter à 100 chars
        
        # Extraire onClick/onPress
        handler_match = re.search(r'on(Click|Press|Submit)=\{([^}]+)\}', code_snippet)
        handler = handler_match.group(2) if handler_match else None
        
        # Extraire className (Tailwind, CSS Modules, etc.)
        class_match = re.search(r'className=["\']([^"\']*)["\']', code_snippet)
        classes = class_match.group(1) if class_match else ""
        
        # Extraire texte du bouton
        text_match = re.search(r'>([^<]+)</', line)
        text_content = text_match.group(1).strip() if text_match else "NO_TEXT"
        
        return ButtonInfo(
            file_path=str(file_path.relative_to(self.project_path)),
            line_number=line_num,
            button_type=pattern_type,
            handler=handler or "NONE",
            classes=classes,
            text_content=text_content,
            is_functional=bool(handler),
            code_snippet=code_snippet
        )
    
    def analyze_buttons(self):
        """Analyse tous les boutons détectés"""
        
        for button in self.buttons:
            issues = self.analyze_button_with_memory(button)
            button.issues = issues
            self.issues.extend(issues)
        
        # Apprendre de cette analyse
        self.learn_from_analysis()
    
    def analyze_button_with_memory(self, button: ButtonInfo) -> List[ButtonIssue]:
        """Analyse un bouton en utilisant la mémoire du projet"""
        
        issues = []
        
        # === ANALYSE FONCTIONNELLE (universelle) ===
        
        # 1. Handler manquant - TOUJOURS critique
        if not button.handler or button.handler == "NONE":
            issues.append(ButtonIssue(
                file_path=button.file_path,
                line_number=button.line_number,
                severity="critical",
                issue_type="missing_handler",
                code_snippet=button.code_snippet,
                description="Bouton sans handler onClick/onPress",
                solution="Ajouter onClick={handlerFunction}",
                auto_fixable=False,  # Nécessite logique métier
                confidence=100
            ))
        
        # 2. Handler vide - TOUJOURS critique
        elif button.handler in ["() => {}", "() => { }", "undefined"]:
            issues.append(ButtonIssue(
                file_path=button.file_path,
                line_number=button.line_number,
                severity="critical",
                issue_type="empty_handler",
                code_snippet=button.code_snippet,
                description="Handler vide, bouton non fonctionnel",
                solution="Implémenter la logique du handler",
                auto_fixable=False,
                confidence=100
            ))
        
        # === ANALYSE VISUELLE (selon framework CSS) ===
        
        if self.stack["css_framework"] == "tailwind" and button.classes:
            issues.extend(self.analyze_tailwind_classes(button))
        
        return issues
    
    def analyze_tailwind_classes(self, button: ButtonInfo) -> List[ButtonIssue]:
        """Analyse les classes Tailwind avec patterns appris"""
        
        issues = []
        classes = button.classes.split()
        
        # Récupérer le pattern standard appris
        learned = self.project_memory.get("patterns", {}).get("primary_button_standard")
        
        if not learned:
            # Mode apprentissage - stocker pour analyse
            self.store_pattern_observation(button)
            return issues
        
        # Mode validation - comparer avec le pattern appris
        
        # 1. Vérifier couleur de fond
        bg_classes = [c for c in classes if c.startswith("bg-") and not c.startswith("bg-gradient")]
        
        if bg_classes:
            current_bg = bg_classes[0]
            expected_bg = learned.get("background")
            confidence = learned.get("confidence", 0)
            
            # Vérifier si c'est une exception connue
            exceptions = self.project_memory.get("preferences", {}).get("color_exceptions", [])
            
            if current_bg != expected_bg and confidence > 70 and current_bg not in exceptions:
                issues.append(ButtonIssue(
                    file_path=button.file_path,
                    line_number=button.line_number,
                    severity="minor",
                    issue_type="inconsistent_color",
                    code_snippet=button.code_snippet,
                    description=f"Couleur {current_bg} vs standard {expected_bg} ({confidence:.0f}% des cas)",
                    solution=f"Remplacer {current_bg} par {expected_bg}",
                    auto_fixable=confidence >= 90,
                    confidence=confidence
                ))
        
        # 2. Vérifier hover state
        hover_classes = [c for c in classes if c.startswith("hover:")]
        expected_hover = learned.get("hover")
        
        # Vérifier si l'utilisateur a refusé les hovers
        no_hover_pref = self.project_memory.get("preferences", {}).get("no_hover_transitions", False)
        
        if not hover_classes and expected_hover and not no_hover_pref:
            hover_confidence = learned.get("hover_confidence", 0)
            
            if hover_confidence > 50:
                issues.append(ButtonIssue(
                    file_path=button.file_path,
                    line_number=button.line_number,
                    severity="minor",
                    issue_type="missing_hover",
                    code_snippet=button.code_snippet,
                    description=f"Hover state manquant (standard : {expected_hover})",
                    solution=f"Ajouter {expected_hover} aux classes",
                    auto_fixable=hover_confidence >= 90,
                    confidence=hover_confidence
                ))
        
        return issues
    
    def store_pattern_observation(self, button: ButtonInfo):
        """Stocke une observation pour apprentissage ultérieur"""
        
        if "pattern_buffer" not in self.project_memory:
            self.project_memory["pattern_buffer"] = []
        
        classes = button.classes.split()
        bg = next((c for c in classes if c.startswith("bg-") and not c.startswith("bg-gradient")), None)
        hover = next((c for c in classes if c.startswith("hover:bg-")), None)
        
        self.project_memory["pattern_buffer"].append({
            "background": bg,
            "hover": hover,
            "classes": button.classes,
            "file": button.file_path
        })
    
    def learn_from_analysis(self):
        """Apprend des patterns observés dans cette analyse"""
        
        buffer = self.project_memory.get("pattern_buffer", [])
        
        # Si on a 10+ observations et pas encore de pattern standard
        if len(buffer) >= 10 and "primary_button_standard" not in self.project_memory.get("patterns", {}):
            
            # Calculer le pattern majoritaire
            bg_counter = Counter(b["background"] for b in buffer if b["background"])
            hover_counter = Counter(b["hover"] for b in buffer if b["hover"])
            
            if bg_counter:
                most_common_bg, count = bg_counter.most_common(1)[0]
                confidence = (count / len(buffer)) * 100
                
                pattern = {
                    "background": most_common_bg,
                    "confidence": confidence,
                    "occurrences": count,
                    "total_samples": len(buffer),
                    "learned_at": datetime.now().isoformat()
                }
                
                if hover_counter:
                    most_common_hover, hover_count = hover_counter.most_common(1)[0]
                    pattern["hover"] = most_common_hover
                    pattern["hover_confidence"] = (hover_count / len(buffer)) * 100
                
                if "patterns" not in self.project_memory:
                    self.project_memory["patterns"] = {}
                
                self.project_memory["patterns"]["primary_button_standard"] = pattern
                
                print(f"\n🧠 Pattern standard appris : {most_common_bg}")
                print(f"   Confiance : {confidence:.1f}%")
                print(f"   Basé sur {count}/{len(buffer)} observations")
    
    def categorize_issues(self) -> Dict[str, List[ButtonIssue]]:
        """Catégorise les issues par niveau de confiance"""
        
        categorized = {
            "auto_fix": [],      # Confiance ≥90%, correction auto
            "recommend": [],     # Confiance 70-89%, recommandation
            "suggest": [],       # Confiance 50-69%, suggestion
            "ask": []           # Confiance <50% ou critique
        }
        
        for issue in self.issues:
            if issue.severity == "critical":
                # Critiques nécessitent validation humaine
                categorized["ask"].append(issue)
            elif issue.confidence >= 90 and issue.auto_fixable:
                categorized["auto_fix"].append(issue)
            elif issue.confidence >= 70:
                categorized["recommend"].append(issue)
            elif issue.confidence >= 50:
                categorized["suggest"].append(issue)
            else:
                categorized["ask"].append(issue)
        
        return categorized
    
    def generate_report(self) -> str:
        """Génère le rapport d'analyse complet"""
        
        scan_count = self.project_memory["scan_count"] + 1
        
        # Catégoriser les issues
        critical = [i for i in self.issues if i.severity == "critical"]
        important = [i for i in self.issues if i.severity == "important"]
        minor = [i for i in self.issues if i.severity == "minor"]
        
        categorized = self.categorize_issues()
        
        # Calculer confiance moyenne
        confidence_scores = self.project_memory.get("confidence_scores", {})
        avg_confidence = sum(confidence_scores.values()) / len(confidence_scores) if confidence_scores else 0
        
        report = f"""# 🔍 Button Validator V2 - Analyse #{scan_count}

**Date** : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Projet** : {self.project_path.name}
**Chemin** : {self.project_path}

---

## 🧠 État de l'apprentissage

**Stack détecté** :
- Framework : {self.stack["framework"]} ({self.stack["language"]})
- CSS : {self.stack["css_framework"] or "Natif"}
- UI Libraries : {", ".join(self.stack["ui_libraries"]) or "Aucune"}
- Icônes : {", ".join(self.stack["icon_libraries"]) or "Aucune"}
- State : {", ".join(self.stack["state_management"]) or "Sans librairie"}
- Build : {self.stack["build_tool"] or "Standard"}

**Mémoire** :
- Scans effectués : {scan_count}
- Patterns appris : {len(self.project_memory.get("patterns", {}))}
- Préférences confirmées : {len(self.project_memory.get("preferences", {}))}
- Confiance moyenne : {avg_confidence:.1f}%

"""
        
        # Afficher les patterns appris
        patterns = self.project_memory.get("patterns", {})
        if "primary_button_standard" in patterns:
            p = patterns["primary_button_standard"]
            report += f"""
**Pattern bouton primaire appris** :
- Couleur : `{p.get("background", "N/A")}`
- Hover : `{p.get("hover", "N/A")}`
- Confiance : {p.get("confidence", 0):.1f}%
- Observations : {p.get("occurrences", 0)}/{p.get("total_samples", 0)}
"""
        
        report += f"""

---

## 📊 Résumé de l'analyse

- 🔘 **Boutons analysés** : {len(self.buttons)}
- ❌ **Problèmes critiques** : {len(critical)}
- ⚠️  **Problèmes importants** : {len(important)}
- ℹ️  **Améliorations suggérées** : {len(minor)}

**Corrections autonomes** :
- ✅ Auto-correction (confiance ≥90%) : {len(categorized["auto_fix"])}
- ⚠️  Recommandation (70-89%) : {len(categorized["recommend"])}
- 💬 Suggestion (50-69%) : {len(categorized["suggest"])}
- ❓ Validation requise (<50% ou critique) : {len(categorized["ask"])}

---
"""
        
        # Section problèmes critiques
        if critical:
            report += "\n## ❌ PROBLÈMES CRITIQUES\n\n"
            for i, issue in enumerate(critical, 1):
                report += f"""### {i}. {issue.issue_type} - `{issue.file_path}:{issue.line_number}`

**Description** : {issue.description}

**Code** :
```tsx
{issue.code_snippet}
```

**Solution** : {issue.solution}

**Action requise** : Validation humaine nécessaire

---
"""
        
        # Section corrections automatiques
        if categorized["auto_fix"]:
            report += "\n## ✅ CORRECTIONS AUTOMATIQUES (confiance ≥90%)\n\n"
            report += "Ces corrections peuvent être appliquées automatiquement :\n\n"
            for i, issue in enumerate(categorized["auto_fix"], 1):
                report += f"""{i}. **{issue.issue_type}** - `{issue.file_path}:{issue.line_number}`
   - {issue.description}
   - Solution : {issue.solution}
   - Confiance : {issue.confidence:.0f}%

"""
        
        # Section recommandations
        if categorized["recommend"]:
            report += "\n## ⚠️ RECOMMANDATIONS (confiance 70-89%)\n\n"
            report += "Ces corrections sont fortement recommandées :\n\n"
            for i, issue in enumerate(categorized["recommend"], 1):
                report += f"""{i}. **{issue.issue_type}** - `{issue.file_path}:{issue.line_number}`
   - {issue.description}
   - Solution : {issue.solution}
   - Confiance : {issue.confidence:.0f}%

"""
        
        report += "\n---\n"
        report += f"\n**Rapport généré par Button Validator V2 - Learning Edition**\n"
        report += f"**Version** : 2.0.0\n"
        
        return report
    
    def run(self):
        """Lance l'analyse complète"""
        
        print("\n🔍 Démarrage de l'analyse...\n")
        
        # 1. Trouver les fichiers
        files = self.find_files()
        print(f"📄 {len(files)} fichiers à analyser")
        
        if not files:
            print("⚠️  Aucun fichier trouvé à analyser")
            return
        
        # 2. Scanner les boutons
        for i, file_path in enumerate(files, 1):
            if i % 10 == 0:
                print(f"   Progression : {i}/{len(files)}")
            buttons = self.scan_file(file_path)
            self.buttons.extend(buttons)
        
        print(f"🔘 {len(self.buttons)} boutons trouvés\n")
        
        if not self.buttons:
            print("ℹ️  Aucun bouton détecté dans le projet")
            return
        
        # 3. Analyser
        print("🧠 Analyse en cours...")
        self.analyze_buttons()
        
        # 4. Générer rapport
        report = self.generate_report()
        
        # 5. Sauvegarder rapport
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        report_filename = f"button-analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        report_path = reports_dir / report_filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Analyse terminée !")
        print(f"📄 Rapport : {report_path}")
        
        # 6. Mettre à jour et sauvegarder la mémoire
        self.project_memory["scan_count"] += 1
        self.project_memory["last_scan"] = datetime.now().isoformat()
        self.save_project_memory()
        
        print(f"💾 Mémoire sauvegardée")
        
        # 7. Afficher résumé
        categorized = self.categorize_issues()
        print(f"\n📊 Résumé :")
        print(f"   Boutons : {len(self.buttons)}")
        print(f"   Issues : {len(self.issues)}")
        print(f"   - Corrections auto : {len(categorized['auto_fix'])}")
        print(f"   - Recommandations : {len(categorized['recommend'])}")
        print(f"   - Suggestions : {len(categorized['suggest'])}")
        print(f"   - Validation requise : {len(categorized['ask'])}")
        
        return report

def main():
    """Point d'entrée principal"""
    import sys
    
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = "."
    
    validator = ButtonValidatorLearning(project_path)
    validator.run()

if __name__ == "__main__":
    main()
