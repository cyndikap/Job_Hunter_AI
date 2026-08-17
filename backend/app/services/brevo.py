import os
from typing import Any

import httpx


class BrevoService:
    def __init__(self) -> None:
        self.api_key = os.getenv("BREVO_API_KEY", "")
        self.enabled = bool(self.api_key)

    async def send_alert(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.enabled:
            return {
                "status": "mocked",
                "message": "Brevo is not configured. Email simulated for local development.",
                "payload": payload,
            }

        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        body = {
            "sender": {"name": "Job Hunter AI", "email": "noreply@jobhunterai.local"},
            "to": [{"email": os.getenv("USER_EMAIL", "your@email.com"), "name": "Candidate"}],
            "subject": f"Nouvelle opportunité : {payload.get('title', '')}",
            "htmlContent": f"<h3>{payload.get('title', '')}</h3><p><strong>Entreprise:</strong> {payload.get('company', '')}</p><p><strong>Score:</strong> {payload.get('score', 0)}%</p><p><strong>Compétences:</strong> {', '.join(payload.get('common_skills', []))}</p><p><a href='{payload.get('url', '#')}'>Voir l'offre</a></p>",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=body, timeout=20)
            response.raise_for_status()
            return response.json()


brevo_service = BrevoService()
