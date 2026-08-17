from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.security.jwt_auth import get_current_user
from app.services.chat_service import chat_service

router = APIRouter(tags=["chat"])


@router.post("/chat")
def chat(payload: dict, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("user_id") or payload.get("user_id") or payload.get("userId")
    query = str(payload.get("message") or payload.get("question") or "").strip()
    if not query:
        raise HTTPException(status_code=400, detail="message is required")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    return chat_service.chat(query=query, user_id=str(user_id))


@router.get("/chat/history")
def chat_history(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    return chat_service.conversation_memory.get_recent(str(user_id), limit=20)
