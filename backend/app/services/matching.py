import re
from typing import Any


class MatchEngine:
    def __init__(self, candidate_profile: dict[str, Any] | None = None) -> None:
        self.candidate_profile = candidate_profile or {
            "full_name": "Cynthia Sileu Kapnang",
            "skills": ["Azure", "Databricks", "PySpark", "Python", "SQL", "Data Engineering", "Machine Learning", "GenAI", "Spark", "DevOps"],
            "experience_years": 5,
            "location": "Paris",
            "remote_preference": True,
        }

    def _normalize(self, value: str | None) -> str:
        if not value:
            return ""
        return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

    def calculate(self, job: dict[str, Any]) -> dict[str, Any]:
        skills = job.get("skills", [])
        text = f"{job.get('title', '')} {job.get('description', '')} {' '.join(skills)}"
        candidate_skills = self.candidate_profile.get("skills", [])
        normalized_text = self._normalize(text)
        overlap = [
            skill for skill in candidate_skills
            if self._normalize(skill) and self._normalize(skill) in normalized_text
        ]

        job_skill_count = max(len(skills), 1)
        skill_score = min(100, round((len(overlap) / job_skill_count) * 100, 2))
        experience_score = 88 if self.candidate_profile.get("experience_years", 0) >= 3 else 60

        location = job.get("location", "")
        normalized_location = self._normalize(location)
        candidate_location = self._normalize(self.candidate_profile.get("location", ""))
        location_score = 100 if "remote" in normalized_location or candidate_location in normalized_location else 80

        overall_score = round((skill_score * 0.5) + (experience_score * 0.3) + (location_score * 0.2), 2)

        if overall_score >= 90:
            classification = "Excellent Match"
        elif overall_score >= 75:
            classification = "Strong Match"
        elif overall_score >= 60:
            classification = "Moderate Match"
        else:
            classification = "Weak Match"

        return {
            "score_overall": overall_score,
            "score_skills": skill_score,
            "score_experience": experience_score,
            "score_location": location_score,
            "classification": classification,
            "common_skills": overlap,
        }


match_engine = MatchEngine()
