from app.services.collector_service import CollectorService


def test_collector_service_detects_and_deduplicates_jobs():
    service = CollectorService()
    job = {
        "source": "apec",
        "title": "Data Engineer",
        "company": "Apex AI",
        "location": "Paris / Remote",
        "url": "https://example.com/jobs/data-engineer",
        "description": "Azure, Databricks, Python, SQL.",
        "skills": ["Azure", "Databricks", "Python", "SQL"],
        "match_score": 91,
        "classification": "Strong Match",
    }

    assert service._store_job(job) is True
    assert service._store_job(job) is False
