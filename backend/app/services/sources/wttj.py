from __future__ import annotations

from typing import Any


class WelcomeToTheJungleSource:
    name = "Welcome to the Jungle"
    base_url = "https://www.welcometothejungle.com"

    def fetch_jobs(self) -> list[dict[str, Any]]:
        jobs = [
            {
                "source": "Welcome to the Jungle",
                "source_job_id": "wttj-001",
                "title": "AI Engineer",
                "company": "Nova AI",
                "location": "Remote",
                "published_at": "2026-08-17T08:15:00Z",
                "description": "Développer des services d'IA générative, pipelines de données, orchestrations et intégrations sur Azure. Python, LLM, MLOps et RAG.",
                "skills": ["Python", "Machine Learning", "GenAI", "Azure", "LLM", "RAG"],
                "url": "https://www.welcometothejungle.com/fr/jobs/ai-engineer-remote",
            },
            {
                "source": "Welcome to the Jungle",
                "source_job_id": "wttj-002",
                "title": "Data Engineer",
                "company": "Cloudia",
                "location": "Paris",
                "published_at": "2026-08-17T12:00:00Z",
                "description": "Construction de pipelines ETL/ELT, modélisation BI et automatisation. Expérience Databricks, SQL, Spark et cloud.",
                "skills": ["Databricks", "Spark", "SQL", "Azure", "Python"],
                "url": "https://www.welcometothejungle.com/fr/jobs/data-engineer-paris",
            },
        ]
        return jobs
