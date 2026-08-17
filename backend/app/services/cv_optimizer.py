from __future__ import annotations

from typing import Any


class CVOptimizer:
    def analyze(self, cv: dict[str, Any], job: dict[str, Any]) -> dict[str, Any]:
        cv_skills = set(str(skill).lower() for skill in cv.get("skills", []))
        job_skills = set(str(skill).lower() for skill in job.get("required_skills", []))
        missing = sorted(job_skills - cv_skills)
        return {
            "missing_keywords": missing,
            "recommendations": [
                f"Ajouter la compétence '{keyword}' au CV" for keyword in missing[:3]
            ],
            "optimized_summary": f"Profil orienté {job.get('title', 'Data Engineer')} avec expertise en {', '.join(sorted(cv_skills)[:5])}.",
        }


cv_optimizer = CVOptimizer()
