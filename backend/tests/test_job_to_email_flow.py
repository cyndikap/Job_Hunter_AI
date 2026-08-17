from app.services.alerting import AlertService
from app.services.matching import MatchEngine


def test_job_to_matching_then_alert_email_flow():
    job = {
        "title": "Senior Data Engineer",
        "company": "Apex AI",
        "location": "Paris / Remote",
        "url": "https://example.com/jobs/apex-ai-data-engineer",
        "description": "We are looking for a data engineer with Azure Databricks, PySpark, SQL, Python and GenAI experience.",
        "skills": ["Azure", "Databricks", "PySpark", "Python", "SQL", "GenAI", "Spark"],
    }

    match = MatchEngine().calculate(job)
    assert match["score_overall"] >= 85
    assert match["classification"] in {"Excellent Match", "Strong Match"}

    alert = AlertService()
    result = alert.send_email({
        **job,
        "match_score": int(match["score_overall"]),
        "skills": job["skills"],
    })

    assert result["status"] in {"sent", "error", "mocked"}
    assert result["channel"] == "email"
    assert "Job Hunter AI" in result["subject"]
