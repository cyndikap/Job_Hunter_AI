from __future__ import annotations

from typing import Any


class OpportunityPredictor:
    def score_opportunity(self, opportunity: dict[str, Any]) -> dict[str, Any]:
        match_score = float(opportunity.get("match_score", 0))
        response_rate = float(opportunity.get("history", {}).get("response_rate", 50))
        interview_rate = float(opportunity.get("history", {}).get("interview_rate", 20))
        company_factor = 1.0 if opportunity.get("company", "").lower() in {"capgemini", "google", "microsoft", "aws"} else 0.85
        location_factor = 1.0 if str(opportunity.get("location", "")).lower() in {"paris", "france", "remote"} else 0.8
        skill_overlap = 0.0
        required_skills = opportunity.get("required_skills", [])
        candidate_skills = opportunity.get("candidate_skills", [])
        if required_skills:
            skill_overlap = (len(set(required_skills).intersection(candidate_skills)) / len(required_skills)) * 100

        interview_probability = min(100.0, max(0.0, (match_score * 0.55) + (skill_overlap * 0.25) + (interview_rate * 0.2) * company_factor))
        response_probability = min(100.0, max(0.0, (match_score * 0.45) + (response_rate * 0.35) + (skill_overlap * 0.2) * location_factor))
        hire_probability = min(100.0, max(0.0, (match_score * 0.40) + (skill_overlap * 0.30) + (response_probability * 0.3) * 0.5))

        return {
            "interview_probability": round(interview_probability, 2),
            "response_probability": round(response_probability, 2),
            "hire_probability": round(hire_probability, 2),
            "explanation": {
                "match_score": match_score,
                "skill_overlap": round(skill_overlap, 2),
                "company_factor": company_factor,
                "location_factor": location_factor,
            },
        }


opportunity_predictor = OpportunityPredictor()
