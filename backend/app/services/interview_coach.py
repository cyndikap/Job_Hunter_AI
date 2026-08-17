from __future__ import annotations

from typing import Any


class InterviewCoach:
    def generate_questions(self, domain: str) -> dict[str, Any]:
        questions = {
            "data engineering": [
                "Comment concevez-vous un pipeline de données scalable ?",
                "Quels défis de qualité de données avez-vous rencontrés ?",
            ],
            "azure": [
                "Comment gérez-vous la sécurité et la gouvernance Azure ?",
                "Quels services Azure avez-vous utilisés en production ?",
            ],
            "databricks": [
                "Comment optimisez-vous les jobs Databricks ?",
                "Quelle stratégie utilisez-vous pour la gestion des clusters ?",
            ],
            "python": [
                "Comment structurez-vous un code Python robuste en production ?",
                "Quels design patterns utilisez-vous pour des services API ?",
            ],
            "generative ai": [
                "Comment évaluez-vous la qualité d’un système RAG ?",
                "Quelles sont les limites des LLMs en production ?",
            ],
        }
        return {"domain": domain, "questions": questions.get(domain.lower(), ["Expliquez votre expérience sur ce sujet."])}

    def simulate(self, domain: str) -> dict[str, Any]:
        questions = self.generate_questions(domain)["questions"]
        return {
            "domain": domain,
            "mock_interview": questions,
            "advice": "Restez concret, utilisez des exemples métiers, et expliquez vos décisions d’architecture.",
        }


interview_coach = InterviewCoach()
