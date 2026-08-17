from typing import Optional

from pydantic import BaseModel, Field


class JobOffer(BaseModel):
    id: Optional[int] = None
    title: str
    company: str
    location: str
    match_score: int = 0
    classification: str = "À revoir"
    skills: list[str] = Field(default_factory=list)
    url: str


class DashboardSummary(BaseModel):
    candidate: str
    role_target: str
    jobs_monitored: int
    high_match: int
    medium_match: int
    low_match: int
    last_scan: str
