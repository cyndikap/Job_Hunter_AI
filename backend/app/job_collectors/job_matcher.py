from __future__ import annotations

from typing import Any


DEFAULT_PROFILE_SKILLS = {
    "azure",
    "databricks",
    "python",
    "sql",
    "pyspark",
    "spark",
    "genai",
    "machine learning",
    "data engineering",
    "devops",
    "power bi",
    "azure data factory",
}


def normalize_value(value: str) -> str:
    return " ".join(str(value).lower().split())


def classify_score(score: float) -> str:
    if score >= 90:
        return "Excellent Match"
    if score >= 80:
        return "Strong Match"
    if score >= 65:
        return "Moderate Match"
    return "Weak Match"


def match_job(profile: dict[str, Any], job: dict[str, Any]) -> dict[str, Any]:
    profile_skills = {normalize_value(s) for s in profile.get("skills", [])}
    offer_skills = {normalize_value(s) for s in job.get("skills", [])}

    common_skills = sorted(profile_skills.intersection(offer_skills))

    skill_score = 0.0
    if offer_skills:
        skill_score = (len(common_skills) / max(len(offer_skills), 1)) * 100

    location_score = 100.0
    user_location = normalize_value(profile.get("location", ""))
    job_location = normalize_value(job.get("location", ""))
    if user_location and job_location:
        location_score = 100.0 if user_location in job_location or job_location in user_location else 60.0
    elif user_location:
        location_score = 70.0

    global_score = round((skill_score * 0.7) + (location_score * 0.3), 2)

    return {
        "score_global": global_score,
        "score_competences": round(skill_score, 2),
        "score_localisation": round(location_score, 2),
        "classification": classify_score(global_score),
        "common_skills": common_skills,
    }
