from fastapi import APIRouter, Depends, HTTPException

from app.security.jwt_auth import get_current_user
from app.services.career_advisor import career_advisor
from app.services.cover_letter_generator import cover_letter_generator
from app.services.cv_optimizer import cv_optimizer
from app.services.interview_coach import interview_coach
from app.services.llm_provider import llm_provider
from app.services.opportunity_predictor import opportunity_predictor
from app.services.rag_pipeline import RAGPipeline
from app.services.rejection_analyzer import rejection_analyzer
from app.services.user_memory import user_memory
from app.services.weekly_strategy import weekly_strategy

router = APIRouter(prefix="/ai", tags=["ai"])
rag_pipeline = RAGPipeline()


@router.post("/chat")
def chat(payload: dict, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("user_id") or payload.get("user_id") or payload.get("userId")
    query = str(payload.get("message", "") or payload.get("question", "")).strip()
    if not query:
        raise HTTPException(status_code=400, detail="message is required")

    context = rag_pipeline.build_context(query, user_id=user_id, limit=5)
    response = llm_provider.generate(question=query, context=context["context_text"], user_id=user_id)
    return {
        "answer": response["answer"],
        "provider": response["provider"],
        "user_id": user_id,
        "context": {
            "documents": context["documents"],
            "justification": context["justification"],
        },
    }


@router.post("/analyze-cv")
def analyze_cv(payload: dict):
    return cv_optimizer.analyze(payload.get("cv", {}), payload.get("job", {}))


@router.post("/interview-coach")
def interview_coach_route(payload: dict):
    return interview_coach.generate_questions(payload.get("domain", "data engineering"))


@router.post("/opportunity-score")
def opportunity_score(payload: dict):
    return opportunity_predictor.score_opportunity(payload.get("opportunity", {}))


@router.post("/career-advice")
def career_advice(payload: dict):
    return career_advisor.analyze_profile(payload.get("profile", {}))


@router.get("/weekly-plan")
def weekly_plan():
    return weekly_strategy.generate([])


@router.get("/insights")
def insights():
    return {
        "average_match": 82,
        "response_rate": 34,
        "interview_rate": 18,
        "best_opportunities": ["Azure Data Engineer", "Senior Data Engineer", "AI Engineer"],
        "top_skills": ["Azure", "Python", "SQL", "Databricks"],
        "market_gap": "Azure DevOps et Terraform sont sous-représentés par rapport au marché.",
    }


@router.post("/memory")
def save_memory(payload: dict):
    return user_memory.save_preferences(payload)


@router.get("/memory")
def get_memory():
    return user_memory.get_profile()
