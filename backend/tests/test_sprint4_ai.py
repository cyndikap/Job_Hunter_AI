from app.services.career_advisor import CareerAdvisor
from app.services.opportunity_predictor import OpportunityPredictor
from app.services.user_memory import UserMemory


def test_opportunity_prediction_scoring():
    predictor = OpportunityPredictor()
    score = predictor.score_opportunity(
        {
            "match_score": 88,
            "company": "Capgemini",
            "location": "Paris",
            "required_skills": ["Azure", "Python", "SQL"],
            "candidate_skills": ["Azure", "Python", "SQL", "Databricks"],
            "history": {"response_rate": 60, "interview_rate": 25},
        }
    )
    assert 0 <= score["interview_probability"] <= 100
    assert 0 <= score["response_probability"] <= 100
    assert 0 <= score["hire_probability"] <= 100


def test_career_advice_generation():
    advisor = CareerAdvisor()
    advice = advisor.analyze_profile(
        {
            "skills": ["Python", "SQL", "Azure", "Databricks"],
            "experience_years": 5,
            "target_role": "Data Engineer",
            "applications": [{"status": "REJECTED"}, {"status": "INTERVIEW"}],
            "job_history": ["Data Engineer", "AI Engineer"],
        }
    )
    assert advice["strengths"]
    assert advice["areas_for_improvement"]
    assert "recommendations" in advice


def test_user_memory_persists_preferences():
    memory = UserMemory(storage_path="/tmp/jobhunter_ai_memory.json")
    memory.save_preferences({"location": "Paris", "salary_target": 90000})
    memory.record_interaction("prefer Azure Databricks")
    profile = memory.get_profile()
    assert profile["preferences"]["location"] == "Paris"
    assert "Azure Databricks" in profile["interaction_history"][-1]
