from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services.smtp_service import SMTPEmailService
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
        self.jobs: list[dict[str, Any]] = []
        self.smtp = SMTPEmailService()
        self.seen_signatures: set[str] = set()

    def _signature(self, job: dict[str, Any]) -> str:
        return f"{job.get('source')}::{job.get('url')}::{job.get('title')}::{job.get('company')}"

    def _store_job(self, job: dict[str, Any]) -> bool:
        signature = self._signature(job)
        if signature in self.seen_signatures:
            return False
        self.seen_signatures.add(signature)
        self.jobs.append({
            **job,
            "detected_at": datetime.now(timezone.utc).isoformat(),
            "match_score": float(job.get("match_score", 0)),
        })
        return True

    def run_all(self) -> dict[str, Any]:
        detected_jobs: list[dict[str, Any]] = []
        profile = {
            "skills": ["Azure", "Databricks", "Python", "SQL", "PySpark", "Spark", "GenAI", "Machine Learning", "Data Engineering"],
            "location": "Paris",
        }

        for collector in self.collectors:
            for raw_job in collector.fetch_jobs():
                normalized = collector.normalize_job(raw_job)
                match_result = match_job(profile, normalized)
                normalized["match_score"] = match_result["score_global"]
                normalized["classification"] = match_result["classification"]
                normalized["common_skills"] = match_result["common_skills"]
                detected_jobs.append(normalized)

                if self._store_job(normalized):
                    if normalized.get("match_score", 0) >= 80:
                        self.smtp.send_email(
                            subject=f"[{normalized.get('classification', 'Match')}] {normalized.get('title', 'Offre')} chez {normalized.get('company', 'Entreprise')}",
                            body=f"Offre compatible détectée\n\nTitre: {normalized.get('title')}\nEntreprise: {normalized.get('company')}\nLieu: {normalized.get('location')}\nScore: {normalized.get('match_score')}\nCompétences: {', '.join(normalized.get('common_skills', []))}\nLien: {normalized.get('url', '')}",
                            to_email="kapnangcynthia@gmail.com",
                        )

        return {
            "status": "ok",
            "jobs_detected": len(detected_jobs),
            "new_jobs": len([job for job in detected_jobs if self._signature(job) in self.seen_signatures]),
            "scanned_at": datetime.now(timezone.utc).isoformat(),
        }


collector_service = CollectorService()
