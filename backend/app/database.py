from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_tables() -> None:
    from app.models import ApplicationTracking, CandidateProfile, EmailLog, JobMatch, JobOffer, JobSource  # noqa: F401

    Base.metadata.create_all(bind=engine)
