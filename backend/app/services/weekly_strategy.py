from __future__ import annotations

from typing import Any


class WeeklyStrategy:
    def generate(self, opportunities: list[dict[str, Any]]) -> dict[str, Any]:
        prioritized = sorted(opportunities, key=lambda item: float(item.get("match_score", 0)), reverse=True)[:10]
        return {
            "top_10_opportunities": prioritized,
            "priority_applications": [item.get("title", "Poste") for item in prioritized[:5]],
            "recruiters_to_contact": [item.get("company", "Entreprise") for item in prioritized[:3]],
            "follow_up_actions": ["Relancer les recruteurs non répondus depuis 7 jours", "Mettre à jour le CV sur les offres prioritaires"],
            "weekly_goals": ["Candidater à 5 postes prioritaires", "Préparer 2 simulations d’entretien", "Réviser Azure DevOps et Terraform"],
        }


weekly_strategy = WeeklyStrategy()
