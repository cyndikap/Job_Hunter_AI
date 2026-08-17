from __future__ import annotations

from datetime import datetime, timezone
from statistics import mean
from typing import Any


class AnalyticsService:
    def __init__(self) -> None:
        self.default_data = {
            "jobs": [
                {"title": "AI Engineer", "company": "Ippon Technologies", "source": "APEC", "match_score": 92, "published_at": "2026-08-15T10:00:00+00:00", "status": "applied", "response_time_days": 3},
                {"title": "Data Engineer", "company": "Capgemini", "source": "Welcome to the Jungle", "match_score": 88, "published_at": "2026-08-14T10:00:00+00:00", "status": "interview", "response_time_days": 2},
                {"title": "Senior Data Scientist", "company": "Mistral", "source": "APEC", "match_score": 94, "published_at": "2026-08-12T10:00:00+00:00", "status": "hired", "response_time_days": 5},
            ],
            "applications": [
                {"status": "replied", "response_time_days": 3},
                {"status": "interview", "response_time_days": 2},
                {"status": "hired", "response_time_days": 5},
                {"status": "pending", "response_time_days": 14},
            ],
            "skills": [
                {"name": "Azure DevOps", "demand": 87},
                {"name": "Terraform", "demand": 82},
                {"name": "Spark Streaming", "demand": 75},
                {"name": "Data Governance", "demand": 72},
                {"name": "Python", "demand": 95},
            ],
            "profile_skills": ["Python", "SQL", "Azure", "AI", "FastAPI"],
        }

    def calculate_dashboard_metrics(self) -> dict[str, Any]:
        jobs = self.default_data["jobs"]
        applications = self.default_data["applications"]
        skills = self.default_data["skills"]

        response_rate = round((sum(1 for item in applications if item["status"] in {"replied", "interview", "hired"}) / len(applications)) * 100, 2)
        interview_rate = round((sum(1 for item in applications if item["status"] == "interview") / len(applications)) * 100, 2)
        hire_rate = round((sum(1 for item in applications if item["status"] == "hired") / len(applications)) * 100, 2)
        average_response_time = round(mean(item["response_time_days"] for item in applications), 2)

        top_opportunities = [
            {
                "title": job["title"],
                "company": job["company"],
                "score": job["match_score"],
                "interview_probability": min(98, job["match_score"] - 4),
                "hire_probability": min(90, max(30, job["match_score"] - 10)),
                "published_at": job["published_at"],
            }
            for job in sorted(jobs, key=lambda x: x["match_score"], reverse=True)[:10]
        ]

        missing_skills = [
            skill["name"] for skill in skills if skill["name"] not in self.default_data["profile_skills"]
        ]
        career_score = min(100, max(0, round((sum(job["match_score"] for job in jobs) / len(jobs)) * 0.7 + response_rate * 0.3, 2)))

        return {
            "response_rate": response_rate,
            "interview_rate": interview_rate,
            "hire_rate": hire_rate,
            "average_response_time_days": average_response_time,
            "top_opportunities": top_opportunities,
            "missing_skills": missing_skills,
            "career_score": career_score,
            "most_reactive_company": "Ippon Technologies",
            "most_efficient_source": "APEC",
            "most_demanded_technology": "Python",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }


analytics_service = AnalyticsService()
