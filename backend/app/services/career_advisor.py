from __future__ import annotations

from collections import Counter
from typing import Any


class CareerAdvisor:
    def analyze_profile(self, profile: dict[str, Any]) -> dict[str, Any]:
        skills = profile.get("skills", [])
        applications = profile.get("applications", [])
        strengths = []
        if "Azure" in skills:
            strengths.append("Fort alignement Azure")
        if "Python" in skills:
            strengths.append("Python bien maîtrisé")
        if "SQL" in skills:
            strengths.append("SQL solide")
        if "Databricks" in skills:
            strengths.append("Expérience Databricks reconnue")

        rejection_count = sum(1 for item in applications if str(item.get("status", "")).upper() == "REJECTED")
        interview_count = sum(1 for item in applications if str(item.get("status", "")).upper() in {"INTERVIEW", "HR_INTERVIEW", "TECHNICAL_INTERVIEW"})

        missing = [
            skill for skill in ["Terraform", "Azure DevOps", "Spark Streaming", "English", "Power BI"]
            if skill not in [s.lower().title() for s in skills]
        ]

        recommendations = [
            "Renforcer Azure DevOps pour les postes senior",
            "Apprendre Terraform pour les architectures cloud",
            "Développer Spark Streaming pour les use cases data real-time",
            "Améliorer l’anglais professionnel pour les échanges internationaux",
        ]

        return {
            "candidate_profile": profile.get("target_role", "Data Engineer"),
            "strengths": strengths or ["Profil technique solide"],
            "weaknesses": ["Expérience limitée sur certains outils cloud critiques"] if rejection_count else ["Aucun signal négatif majeur"],
            "areas_for_improvement": missing or ["Azure DevOps", "Terraform"],
            "missing_technologies": missing,
            "recommendations": recommendations[:3],
            "interview_signal": {
                "rejections": rejection_count,
                "interviews": interview_count,
                "trend": "positive" if interview_count >= 1 else "watchlist",
            },
        }


career_advisor = CareerAdvisor()
