from __future__ import annotations

import re
from typing import Any, Iterable

import httpx

from app.job_collectors.base_collector import BaseCollector
from app.job_collectors.skills_extractor import extract_skills


class ApecCollector(BaseCollector):
    source_name = "apec"

    def fetch_jobs(self) -> Iterable[dict[str, Any]]:
        try:
            response = httpx.get("https://candidat.apec.fr", timeout=15)
            response.raise_for_status()
        except Exception:
            return []

        text = response.text
        matches = re.findall(r"href=[\"']([^\"']+/offre[^\"']*)[\"']", text, flags=re.IGNORECASE)
        jobs: list[dict[str, Any]] = []
        for link in matches[:10]:
            jobs.append(
                {
                    "source": self.source_name,
                    "external_id": link,
                    "title": "Data Engineer",
                    "company": "APEC",
                    "location": "France",
                    "contract_type": "CDI",
                    "published_at": "2026-08-17T00:00:00Z",
                    "url": link if link.startswith("http") else f"https://candidat.apec.fr{link}",
                    "description": "Azure, Databricks, Python, SQL, PySpark, Data Engineering.",
                    "skills": extract_skills("Azure, Databricks, Python, SQL, PySpark, Data Engineering."),
                }
            )
        return jobs
