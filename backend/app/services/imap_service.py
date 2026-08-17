import os
import re
from typing import Any


class IMAPEmailService:
    def __init__(self) -> None:
        self.host = os.getenv("IMAP_HOST", "imap.gmail.com")
        self.port = int(os.getenv("IMAP_PORT", "993"))
        self.email = os.getenv("EMAIL", "")
        self.password = os.getenv("EMAIL_PASSWORD", "")

    def classify_message(self, message: dict[str, Any]) -> dict[str, Any]:
        subject = str(message.get("subject", "")).lower()
        body = str(message.get("body", "")).lower()
        combined = f"{subject} {body}"

        if any(keyword in combined for keyword in ["interview", "entretien", "rdv", "call"]):
            return {
                "status": "interview",
                "provider": "recruiter",
                "keywords": ["interview", "entretien"],
                "summary": "Réponse recruteur : entretien proposé.",
            }

        if any(keyword in combined for keyword in ["refus", "rejected", "not proceed", "non retenu"]):
            return {
                "status": "rejected",
                "provider": "recruiter",
                "keywords": ["refus", "rejected"],
                "summary": "Réponse recruteur : candidature refusée.",
            }

        if any(keyword in combined for keyword in ["merci", "candidature", "interested", "cv"]):
            return {
                "status": "received",
                "provider": "recruiter",
                "keywords": ["candidature", "received"],
                "summary": "Réponse recruteur reçue.",
            }

        return {
            "status": "unknown",
            "provider": "recruiter",
            "keywords": [],
            "summary": "Réponse non identifiée.",
        }

    def fetch_incoming_messages(self) -> list[dict[str, Any]]:
        return []
