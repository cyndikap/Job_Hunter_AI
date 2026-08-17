from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.job_collectors.collectors.apec_collector import ApecCollector
from app.job_collectors.collectors.hellowork_collector import HelloworkCollector
from app.job_collectors.collectors.wttj_collector import WttjCollector
from app.job_collectors.job_matcher import match_job


class CollectorService:
    def __init__(self):
        self.collectors = [
            ApecCollector(),
            WttjCollector(),
            HelloworkCollector(),
        ]

    def run(self, profile: dict[str, Any]) -> dict[str, Any]:
        all_jobs: list[dict[str, Any]] = []
        for collector in self.collectors:
            for raw in collector.fetch_jobs():
                normalized = collector.normalize_job(raw)
                all_jobs.append(normalized)

        matches = []
        for job in all_jobs:
            result = match_job(profile, job)
            job["match_result"] = result
            matches.append(job)

        return {
            "jobs_seen": len(all_jobs),
            "matches": matches,
            "collected_at": datetime.now(timezone.utc).isoformat(),
        }
