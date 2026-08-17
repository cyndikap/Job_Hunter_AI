from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class NotificationCenter:
    def __init__(self) -> None:
        self.notifications = [
            {
                "id": "n-1",
                "type": "new_offer",
                "title": "Nouvelle offre très pertinente",
                "message": "AI Engineer chez Ippon Technologies correspond à 92% de votre profil.",
                "channel": "email",
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
            {
                "id": "n-2",
                "type": "follow_up",
                "title": "Recruteur à relancer",
                "message": "Relancez Céline Martin de Capgemini dans 48h pour maintenir le contact.",
                "channel": "in_app",
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
            {
                "id": "n-3",
                "type": "no_response",
                "title": "Candidature sans réponse",
                "message": "Une des candidatures a plus de 14 jours sans réponse.",
                "channel": "email",
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
        ]

    def get_notifications(self) -> list[dict[str, Any]]:
        return self.notifications

    def add_notification(self, notification: dict[str, Any]) -> dict[str, Any]:
        self.notifications.insert(0, {**notification, "created_at": datetime.now(timezone.utc).isoformat()})
        return self.notifications[0]


notification_center = NotificationCenter()
