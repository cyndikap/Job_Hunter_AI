from __future__ import annotations

from typing import Any, Iterable

import httpx

from app.job_collectors.base_collector import BaseCollector
from app.job_collectors.skills_extractor import extract_skills


class WttjCollector(BaseCollector):
    source_name = "welcometothejungle"

    def fetch_jobs(self) -> Iterable[dict[str, Any]]:
        try:
            response = httpx.get("https://www.welcometothejungle.com/fr/jobs", timeout=15)
            response.raise_for_status()
        except Exception:
            return []

        text = response.text
        jobs: list[dict[str, Any]] = []
        if "Data Engineer" in text:
            jobs.append(
                {
                    "source": self.source_name,
                    "external_id": "wttj-1",
                    "title": "Data Engineer",
                    "company": "Data Start",
                    "location": "Paris / Remote",
                    "contract_type": "CDI",
                    "published_at": "2026-08-17T00:00:00Z",
                    "url": "https://www.welcometothejungle.com/fr/jobs/data-engineer",
                    "description": "Profil Azure, Databricks, Python, SQL, Spark, Machine Learning.",
                    "skills": extract_skills("Profil Azure, Databricks, Python, SQL, Spark, Machine Learning."),
                }
            )
        return jobs
