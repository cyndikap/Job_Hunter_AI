from app.job_collectors.job_matcher import match_job
from app.job_collectors.skills_extractor import extract_skills


def test_extract_skills_basic():
    text = "We are looking for Azure Databricks, Python, SQL, PySpark and GenAI engineer."
    skills = extract_skills(text)
    assert "Azure" in skills
    assert "Databricks" in skills
    assert "Python" in skills
    assert "SQL" in skills
    assert "PySpark" in skills


def test_match_job_score_and_classification():
    profile = {
        "skills": ["Azure", "Databricks", "Python", "SQL"],
        "location": "Paris",
    }
    job = {
        "skills": ["Azure", "Databricks", "Python", "SQL", "PySpark"],
        "location": "Paris / Remote",
    }

    result = match_job(profile, job)
    assert result["score_global"] >= 80
    assert result["classification"] in {"Strong Match", "Excellent Match"}
    assert result["score_competences"] > 0
