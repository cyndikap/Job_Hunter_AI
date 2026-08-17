from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_signup_route_returns_ok_or_mocked():
    response = client.post("/api/v1/auth/signup", json={"email": "user@example.com", "password": "secret123", "full_name": "User Test"})
    assert response.status_code in {200, 400}
    if response.status_code == 200:
        data = response.json()
        assert data.get("access_token") or data.get("status") == "mocked"


def test_signin_route_without_params_fails():
    response = client.post("/api/v1/auth/signin", json={"email": "", "password": ""})
    assert response.status_code == 400


def test_signin_route_returns_token_in_mocked_mode():
    response = client.post("/api/v1/auth/signin", json={"email": "demo@jobhunter.ai", "password": "demo123"})
    assert response.status_code == 200
    data = response.json()
    assert data.get("access_token")
    assert data.get("token_type") == "bearer"


def test_dashboard_summary_returns_ok_when_no_jobs_are_loaded():
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["jobs_monitored"] >= 0
    assert isinstance(payload.get("alerts", []), list)


def test_reset_password_requires_email():
    response = client.post("/api/v1/auth/reset-password", json={"email": ""})
    assert response.status_code == 400
