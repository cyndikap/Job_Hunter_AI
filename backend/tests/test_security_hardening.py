from datetime import datetime

from app.config import Settings
from app.crm.service import CRMService


def test_settings_uses_pydantic_v2_config():
    assert hasattr(Settings, "model_config")
    assert Settings.model_config.get("extra") == "ignore"


def test_crm_classification_timestamp_is_timezone_aware():
    result = CRMService().classify_incoming_email("Interview request", "I would like to schedule a call")
    timestamp = datetime.fromisoformat(result["classified_at"])
    assert timestamp.tzinfo is not None
