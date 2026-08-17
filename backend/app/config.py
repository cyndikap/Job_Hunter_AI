from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Job Hunter AI"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql://postgres:postgres@db:5432/jobhunter"
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = "gpt-4o-mini"
    scheduler_interval_minutes: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
