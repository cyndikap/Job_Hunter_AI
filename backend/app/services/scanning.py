from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

from app.services.matching import match_engine
from app.services.sources import APECJobSource, WelcomeToTheJungleSource
from app.supabase_client import supabase_client


class ScanService:
    def __init__(self) -> None:
        self.jobs: list[dict[str, Any]] = []
        self.sources = [
            APECJobSource(),
            WelcomeToTheJungleSource(),
        ]

    def _fingerprint(self, job: dict[str, Any]) -> str:
        raw = f"{job.get('source')}|{job.get('title')}|{job.get('company')}|{job.get('url')}"
        return sha256(raw.encode("utf-8")).hexdigest()

    def scan(self) -> dict[str, Any]:
        found_jobs: list[dict[str, Any]] = []

        for source in self.sources:
            for job in source.fetch_jobs():
                job["fingerprint"] = self._fingerprint(job)
                job["match_score"] = match_engine.calculate(job)["score_overall"]
                job["classification"] = match_engine.calculate(job)["classification"]
                found_jobs.append(job)

        self.jobs = found_jobs

        if supabase_client.is_available():
            supabase_client.upsert_jobs(found_jobs)

        return {
            "status": "ok",
            "jobs_detected": len(found_jobs),
            "sources": [source.name for source in self.sources],
            "scanned_at": datetime.now(timezone.utc).isoformat(),
        }


scan_service = ScanService()
