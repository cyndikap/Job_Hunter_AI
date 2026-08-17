from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Iterable


class BaseCollector(ABC):
    source_name: str = "base"

    @abstractmethod
    def fetch_jobs(self) -> Iterable[dict[str, Any]]:
        """Return a list of raw job dictionaries."""

    def normalize_job(self, raw: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        return {
            "source": raw.get("source") or self.source_name,
            "external_id": str(raw.get("external_id") or raw.get("id") or ""),
            "title": str(raw.get("title") or "").strip(),
            "company": str(raw.get("company") or "").strip(),
            "location": str(raw.get("location") or "").strip(),
            "contract_type": str(raw.get("contract_type") or raw.get("employment_type") or "").strip(),
            "published_at": raw.get("published_at") or now.isoformat(),
            "url": str(raw.get("url") or "").strip(),
            "description": str(raw.get("description") or "").strip(),
            "skills": raw.get("skills") or [],
            "first_seen_at": raw.get("first_seen_at") or now.isoformat(),
            "is_active": True,
        }
