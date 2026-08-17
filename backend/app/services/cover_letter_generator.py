from __future__ import annotations

from typing import Any


class CoverLetterGenerator:
    def generate(self, company: str, position: str, profile: dict[str, Any]) -> dict[str, Any]:
        return {
            "subject": f"Candidature pour le poste de {position}",
            "body": (
                f"Madame, Monsieur,\n\n"
                f"Je souhaite candidater au poste de {position} au sein de {company}.\n"
                f"Mon profil en {', '.join(profile.get('skills', [])[:5])} et mon intérêt pour les projets data & IA me permettent de contribuer efficacement à vos missions.\n"
                "Je serais ravi d'échanger avec vous sur cette opportunité.\n\n"
                "Cordialement,\n"
                "Cynthia Sileu Kapnang"
            ),
            "email": (
                f"Objet : {position} - {company}\n\n"
                f"Bonjour,\n\n"
                f"Je postule au poste de {position} chez {company}.\n"
                "Je suis particulièrement motivée par les sujets Data, IA et architecture Cloud.\n"
                "Je serais heureux de pouvoir échanger avec vous.\n\n"
                "Cordialement,\nCynthia Sileu Kapnang"
            ),
        }


cover_letter_generator = CoverLetterGenerator()
