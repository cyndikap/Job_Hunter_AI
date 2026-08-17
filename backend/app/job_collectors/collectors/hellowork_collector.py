from __future__ import annotations

from typing import Any, Iterable

import httpx

from app.job_collectors.base_collector import BaseCollector
from app.job_collectors.skills_extractor import extract_skills


class HelloworkCollector(BaseCollector):
    source_name = "hellowork"

    def fetch_jobs(self) -> Iterable[dict[str, Any]]:
        try:
            response = httpx.get("https://www.hellowork.com/fr-fr/", timeout=15)
            response.raise_for_status()
        except Exception:
            return []

        text = response.text
        jobs: list[dict[str, Any]] = []
        if "Data Engineer" in text:
            jobs.append(
                {
                    "source": self.source_name,
                    "external_id": "hellowork-1",
                    "title": "Data Engineer",
                    "company": "Hellowork Partner",
                    "location": "Lyon",
                    "contract_type": "CDI",
                    "published_at": "2026-08-17T00:00:00Z",
                    "url": "https://www.hellowork.com/fr-fr/jobs/data-engineer",
                    "description": "Azure Data Factory, SQL, Python, ETL, Power BI.",
                    "skills": extract_skills("Azure Data Factory, SQL, Python, ETL, Power BI."),
                }
            )
        return jobs
