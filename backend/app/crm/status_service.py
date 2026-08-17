from __future__ import annotations

from typing import Any

from app.crm.models import ApplicationStatus


class ApplicationStatusService:
    @staticmethod
    def transition(application_status: str, new_status: str) -> str:
        if application_status not in {s.value for s in ApplicationStatus}:
            raise ValueError(f"Unknown status: {application_status}")
        if new_status not in {s.value for s in ApplicationStatus}:
            raise ValueError(f"Unknown target status: {new_status}")
        return new_status

    @staticmethod
    def should_send_follow_up(application_status: str, days_since_last_response: int) -> bool:
        return application_status == ApplicationStatus.APPLIED.value and days_since_last_response >= 7
