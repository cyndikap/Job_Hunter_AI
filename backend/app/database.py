from urllib.parse import urlparse

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


def _resolve_database_url() -> str:
    database_url = settings.database_url
    if database_url.startswith("sqlite://"):
        return database_url

    parsed = urlparse(database_url)
    if parsed.hostname in {"db", "localhost", "127.0.0.1"}:
        try:
            engine_test = create_engine(database_url, pool_pre_ping=True)
            with engine_test.connect() as _:
                return database_url
        except Exception:
            return "sqlite:///./jobhunter.db"

    return database_url


engine = create_engine(_resolve_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_tables() -> None:
    from app.models_sqlalchemy import (  # noqa: F401
        ApplicationTracking,
        CandidateProfile,
        ConversationTurn,
        EmailLog,
        JobMatch,
        JobOffer,
        JobSkill,
        JobSource,
    )

    Base.metadata.create_all(bind=engine)
