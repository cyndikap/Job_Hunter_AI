from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class CandidateProfile(Base):
    __tablename__ = "candidate_profile"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    target_title = Column(String(255), nullable=False)
    location_preference = Column(String(255), default="Île-de-France")
    remote_preference = Column(String(50), default="partial_or_full_remote")
    contract_type = Column(String(50), default="CDI")
    country = Column(String(100), default="France")
    cv_summary = Column(Text)


class JobSource(Base):
    __tablename__ = "job_source"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    base_url = Column(Text)
    active = Column(Boolean, default=True)
    priority_level = Column(Integer, default=1)


class JobOffer(Base):
    __tablename__ = "job_offer"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("job_source.id"))
    external_id = Column(String(255))
    title = Column(String(255), nullable=False)
    company = Column(String(255))
    location = Column(String(255))
    contract_type = Column(String(50))
    remote_mode = Column(String(50))
    url = Column(Text)
    description = Column(Text)
    published_at = Column(DateTime)
    scraped_at = Column(DateTime)
    fingerprint = Column(String(255))


class JobSkill(Base):
    __tablename__ = "job_skill"

    id = Column(Integer, primary_key=True, index=True)
    job_offer_id = Column(Integer, ForeignKey("job_offer.id", ondelete="CASCADE"))
    skill_name = Column(String(255), nullable=False)
    confidence = Column(Numeric(5, 2), default=0.0)


class JobMatch(Base):
    __tablename__ = "job_match"

    id = Column(Integer, primary_key=True, index=True)
    job_offer_id = Column(Integer, ForeignKey("job_offer.id", ondelete="CASCADE"))
    candidate_id = Column(Integer, ForeignKey("candidate_profile.id"))
    match_score = Column(Integer, nullable=False)
    classification = Column(String(50))
    summary = Column(Text)
    strengths = Column(Text)
    missing_skills = Column(Text)
    email_sent = Column(Boolean, default=False)
    linkedin_sent = Column(Boolean, default=False)
    url = Column(Text)


class EmailLog(Base):
    __tablename__ = "email_log"

    id = Column(Integer, primary_key=True, index=True)
    job_offer_id = Column(Integer, ForeignKey("job_offer.id"))
    to_email = Column(String(255), nullable=False)
    subject = Column(String(255))
    payload = Column(Text)
    status = Column(String(50), default="sent")


class ApplicationTracking(Base):
    __tablename__ = "application_tracking"

    id = Column(Integer, primary_key=True, index=True)
    job_offer_id = Column(Integer, ForeignKey("job_offer.id"))
    company = Column(String(255))
    status = Column(String(50), default="new")
    match_score = Column(Integer)
    date_applied = Column(DateTime)
    contact_email = Column(String(255))
    email_body = Column(Text)
    linkedin_message = Column(Text)
    cover_letter = Column(Text)
    notes = Column(Text)
