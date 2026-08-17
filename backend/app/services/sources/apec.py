from __future__ import annotations

from typing import Any


class APECJobSource:
    name = "APEC"
    base_url = "https://candidat.apec.fr"

    def fetch_jobs(self) -> list[dict[str, Any]]:
        jobs = [
            {
                "source": "APEC",
                "source_job_id": "apec-001",
                "title": "Data Engineer",
                "company": "Apex Data",
                "location": "Paris",
                "published_at": "2026-08-17T09:00:00Z",
                "description": "Mission sur ingestion, orchestration et pipelines de données Azure. Python, SQL, Databricks, orchestration et data quality.",
                "skills": ["Python", "SQL", "Azure", "Databricks", "PySpark"],
                "url": "https://candidat.apec.fr/offres-demploi/data-engineer-paris-12345",
            },
            {
                "source": "APEC",
                "source_job_id": "apec-002",
                "title": "Senior Data Analyst",
                "company": "Mistral Labs",
                "location": "Lyon",
                "published_at": "2026-08-17T10:30:00Z",
                "description": "Analyse de données, BI, dashboards, automatisation et modélisation de données. Bon niveau SQL, Azure et Python.",
                "skills": ["SQL", "Python", "Power BI", "Azure", "Data Analysis"],
                "url": "https://candidat.apec.fr/offres-demploi/data-analyst-lyon-67890",
            },
        ]
        return jobs
