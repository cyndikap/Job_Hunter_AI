import os
from typing import Any

from supabase import Client, create_client


class SupabaseClient:
    def __init__(self) -> None:
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY")
        self.client: Client | None = None

        if self.url and self.key:
            self.client = create_client(self.url, self.key)

    def is_available(self) -> bool:
        return self.client is not None

    def upsert_jobs(self, jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not self.client:
            return jobs

        payload = [
            {
                "source": job.get("source"),
                "source_job_id": job.get("source_job_id"),
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "url": job.get("url"),
                "description": job.get("description"),
                "published_at": job.get("published_at"),
                "skills": job.get("skills", []),
                "match_score": job.get("match_score", 0),
                "classification": job.get("classification", "Weak Match"),
            }
            for job in jobs
        ]

        try:
            response = self.client.table("jobs").upsert(payload, on_conflict="url").execute()
            return response.data or jobs
        except Exception:
            return jobs


supabase_client = SupabaseClient()
