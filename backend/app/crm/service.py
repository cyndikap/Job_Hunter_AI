from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.crm.email_classifier import EmailClassifier
from app.crm.models import ApplicationStatus


class CRMService:
    def __init__(self):
        self.email_classifier = EmailClassifier()

    def update_application_status(self, application: dict[str, Any], new_status: str) -> dict[str, Any]:
        previous = application.get("status")
        application["status"] = new_status
        application.setdefault("events", []).append(
            {
                "previous_status": previous,
                "new_status": new_status,
                "event_type": "status_change",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        return application

    def build_timeline(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sorted(events, key=lambda e: e.get("created_at", ""))

    def classify_incoming_email(self, subject: str, content: str) -> dict[str, Any]:
        label, confidence = self.email_classifier.classify(subject, content)
        return {
            "classification": label,
            "confidence_score": confidence,
            "classified_at": datetime.now(timezone.utc).isoformat(),
        }

    def should_send_follow_up(self, status: str, days_since_last_response: int) -> bool:
        return status == ApplicationStatus.APPLIED.value and days_since_last_response >= 7

    def compute_response_metrics(self, applications: list[dict[str, Any]]) -> dict[str, Any]:
        total = len(applications)
        positive = sum(1 for app in applications if app.get("status") in {ApplicationStatus.OFFER_RECEIVED.value, ApplicationStatus.ACCEPTED.value})
        rejected = sum(1 for app in applications if app.get("status") == ApplicationStatus.REJECTED.value)
        return {
            "total_applications": total,
            "positive_responses": positive,
            "negative_responses": rejected,
            "response_rate": round((positive / total) * 100, 2) if total else 0,
        }
