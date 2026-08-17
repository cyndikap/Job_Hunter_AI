from __future__ import annotations

from collections import Counter
from typing import Any


class RejectionAnalyzer:
    def analyze(self, history: list[dict[str, Any]]) -> dict[str, Any]:
        rejections = [entry for entry in history if str(entry.get("status", "")).upper() == "REJECTED"]
        by_company = Counter(item.get("company", "Inconnu") for item in rejections)
        by_skill = Counter(skill for item in rejections for skill in item.get("required_skills", []))
        return {
            "total_rejections": len(rejections),
            "top_companies": by_company.most_common(3),
            "common_requirements": by_skill.most_common(5),
            "recommandations": [
                "Renforcer Azure DevOps",
                "Mieux valoriser les projets IA et Data Engineering",
                "Cibler plus précisément les postes alignés avec votre profil",
            ],
        }


rejection_analyzer = RejectionAnalyzer()
