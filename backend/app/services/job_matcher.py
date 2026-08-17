from typing import Dict, List

PROFILE_SKILLS = {
    "Azure Databricks",
    "Azure",
    "Python",
    "SQL",
    "RAG",
    "LLM",
    "Azure OpenAI",
    "Agentic AI",
    "MLflow",
    "MLOps",
    "FastAPI",
    "Data Governance",
    "MDM",
    "PIM",
    "Snowflake",
}

TARGET_TITLES = {
    "AI Engineer",
    "GenAI Engineer",
    "AI & Data Engineer",
    "Agentic AI Engineer",
    "Data Engineer",
    "Data & AI Engineer",
    "MLOps Engineer",
    "Machine Learning Engineer",
    "Data Consultant",
    "Data Governance Consultant",
    "Cloud Data Engineer",
}


def score_job(title: str, company: str, skills: List[str], location: str) -> Dict[str, object]:
    title_lower = title.lower()
    skill_set = {skill.lower() for skill in skills}

    score = 0

    if any(keyword.lower() in title_lower for keyword in ["ai engineer", "genai", "agentic ai", "data & ai", "data engineer"]):
        score += 30

    if any(keyword.lower() in title_lower for keyword in ["data engineer", "mlops", "machine learning"]):
        score += 10

    for skill in PROFILE_SKILLS:
        if skill.lower() in {s.lower() for s in skill_set}:
            score += 4

    if "azure databricks" in {s.lower() for s in skill_set}:
        score += 8

    if "azure" in {s.lower() for s in skill_set}:
        score += 6

    if "paris" in location.lower() or "ile-de-france" in location.lower() or "remote" in location.lower():
        score += 8

    if company.lower() in {"microsoft", "databricks", "capgemini", "eviden", "atos", "accenture", "sopra steria", "ippon", "orange", "airbus"}:
        score += 5

    score = max(0, min(score, 100))

    if score >= 90:
        classification = "Très forte adéquation"
    elif score >= 80:
        classification = "Forte adéquation"
    elif score >= 70:
        classification = "Adéquation moyenne"
    else:
        classification = "À revoir"

    return {
        "score": score,
        "classification": classification,
        "matched_skills": sorted(skill_set.intersection({s.lower() for s in PROFILE_SKILLS})),
    }
