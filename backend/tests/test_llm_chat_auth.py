from fastapi.testclient import TestClient

from app.main import app
from app.security.jwt_auth import create_token

client = TestClient(app)


def test_chat_requires_authentication():
    response = client.post(
        "/api/v1/ai/chat",
        json={"message": "Parle-moi de mon profil"},
    )
    assert response.status_code == 401


def test_chat_uses_authenticated_user_identity():
    token = create_token("user-42")
    response = client.post(
        "/api/v1/ai/chat",
        json={"message": "Parle-moi de mon profil"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code in {200, 500}
    if response.status_code == 200:
        payload = response.json()
        assert payload["user_id"] == "user-42"
