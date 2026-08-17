from __future__ import annotations

import os
from typing import Any

import httpx

from app.security.jwt_auth import create_token

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")


class SupabaseAuthService:
    def __init__(self) -> None:
        self.base_url = SUPABASE_URL.rstrip("/")
        self.anon_key = SUPABASE_ANON_KEY
        self.service_role_key = SUPABASE_SERVICE_ROLE_KEY

    def is_configured(self) -> bool:
        return bool(self.base_url and self.anon_key)

    def sign_up(self, email: str, password: str, full_name: str | None = None) -> dict[str, Any]:
        if not self.is_configured():
            return {
                "status": "mocked",
                "email": email,
                "message": "Supabase Auth non configuré, mode de dev local.",
                "access_token": create_token(email, {"email": email, "full_name": full_name or ""}),
                "token_type": "bearer",
            }
        payload = {
            "email": email,
            "password": password,
            "data": {"full_name": full_name or ""},
        }
        response = httpx.post(
            f"{self.base_url}/auth/v1/signup",
            json=payload,
            headers={"apikey": self.anon_key, "Content-Type": "application/json"},
            timeout=15.0,
        )
        return {"status": response.status_code, "body": response.json() if response.content else {}}

    def sign_in(self, email: str, password: str) -> dict[str, Any]:
        if not self.is_configured():
            return {
                "status": "mocked",
                "email": email,
                "message": "Supabase Auth non configuré, mode de dev local.",
                "access_token": create_token(email, {"email": email, "role": "user"}),
                "token_type": "bearer",
            }
        payload = {"email": email, "password": password}
        response = httpx.post(
            f"{self.base_url}/auth/v1/token?grant_type=password",
            json=payload,
            headers={"apikey": self.anon_key, "Content-Type": "application/json"},
            timeout=15.0,
        )
        return {"status": response.status_code, "body": response.json() if response.content else {}}

    def reset_password(self, email: str) -> dict[str, Any]:
        if not self.is_configured():
            return {"status": "mocked", "email": email, "message": "Reset password simulé en mode dev."}
        response = httpx.post(
            f"{self.base_url}/auth/v1/recover",
            json={"email": email},
            headers={"apikey": self.anon_key, "Content-Type": "application/json"},
            timeout=15.0,
        )
        return {"status": response.status_code, "body": response.json() if response.content else {}}


supabase_auth_service = SupabaseAuthService()
