from pathlib import Path

from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env", override=False)


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=str(PROJECT_ROOT / ".env"), extra="ignore")

    app_name: str = "Job Hunter AI"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql://postgres:postgres@db:5432/jobhunter"
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = "gpt-4o-mini"
    scheduler_interval_minutes: int = 60
    email_to: str = "kapnangcynthia@gmail.com"
    email_threshold: int = 85
    app_base_url: str = "http://localhost:3000"
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174"
    daily_summary_time: str = "08:00"
    smtp_host: str = "smtp-relay.brevo.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    imap_host: str = "imap.gmail.com"
    imap_port: int = 993
    email: str = ""
    email_password: str = ""
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    jwt_secret: str = "jobhunter-ai-production-secret-1234567890"
    jwt_algorithm: str = "HS256"
    rate_limit_per_minute: int = 120
    admin_user_ids: str = "admin"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    mistral_api_key: str = ""
    mistral_model: str = "mistral-small-latest"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_vector_size: int = 768
    qdrant_collection: str = "jobhunter_vectors"


settings = Settings()
