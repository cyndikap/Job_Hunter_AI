from fastapi import APIRouter, HTTPException

from app.services.supabase_auth import supabase_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(payload: dict):
    email = str(payload.get("email", ""))
    password = str(payload.get("password", ""))
    if not email or not password:
        raise HTTPException(status_code=400, detail="email and password are required")
    return supabase_auth_service.sign_up(email, password, payload.get("full_name"))


@router.post("/signin")
def signin(payload: dict):
    email = str(payload.get("email", ""))
    password = str(payload.get("password", ""))
    if not email or not password:
        raise HTTPException(status_code=400, detail="email and password are required")
    return supabase_auth_service.sign_in(email, password)


@router.post("/reset-password")
def reset_password(payload: dict):
    email = str(payload.get("email", ""))
    if not email:
        raise HTTPException(status_code=400, detail="email is required")
    return supabase_auth_service.reset_password(email)
