from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    DETECTED = "DETECTED"
    TO_REVIEW = "TO_REVIEW"
    TO_APPLY = "TO_APPLY"
    APPLIED = "APPLIED"
    RECRUITER_CONTACTED = "RECRUITER_CONTACTED"
    FOLLOW_UP_SENT = "FOLLOW_UP_SENT"
    HR_INTERVIEW = "HR_INTERVIEW"
    TECHNICAL_INTERVIEW = "TECHNICAL_INTERVIEW"
    OFFER_RECEIVED = "OFFER_RECEIVED"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    WITHDRAWN = "WITHDRAWN"


class EmailDirection(str, Enum):
    INBOUND = "incoming"
    OUTBOUND = "outgoing"


class EmailClassification(str, Enum):
    POSITIVE_RESPONSE = "POSITIVE_RESPONSE"
    INTERVIEW_REQUEST = "INTERVIEW_REQUEST"
    MORE_INFORMATION_REQUIRED = "MORE_INFORMATION_REQUIRED"
    FOLLOW_UP = "FOLLOW_UP"
    REJECTION = "REJECTION"
    AUTOMATIC_RESPONSE = "AUTOMATIC_RESPONSE"
    SPAM = "SPAM"


class ApplicationEventBase(BaseModel):
    application_id: str
    previous_status: Optional[str] = None
    new_status: str
    event_type: str = "status_change"
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RecruiterBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    role: Optional[str] = None


class EmailMessageBase(BaseModel):
    application_id: Optional[str] = None
    recruiter_id: Optional[str] = None
    direction: EmailDirection
    subject: str
    content: str
    received_at: datetime = Field(default_factory=datetime.utcnow)
    classification: Optional[EmailClassification] = None
    confidence_score: Optional[float] = None


class ApplicationBase(BaseModel):
    user_id: str
    job_id: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.DETECTED
    source: Optional[str] = None
    applied_at: Optional[datetime] = None
    notes: Optional[str] = None


class InterviewBase(BaseModel):
    application_id: str
    interview_type: str
    scheduled_at: datetime
    interviewer_name: Optional[str] = None
    notes: Optional[str] = None


class NoteBase(BaseModel):
    application_id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
