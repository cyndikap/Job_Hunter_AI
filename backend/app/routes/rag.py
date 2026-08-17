from fastapi import APIRouter, HTTPException

from app.services.rag_pipeline import RAGPipeline

router = APIRouter(prefix="/rag", tags=["rag"])
pipeline = RAGPipeline()


@router.post("/index")
def index_documents(payload: dict):
    documents = payload.get("documents") or []
    if not isinstance(documents, list):
        raise HTTPException(status_code=400, detail="documents must be a list")
    return pipeline.index_documents(documents, fallback_user_id=payload.get("user_id"))


@router.post("/search")
def search_documents(payload: dict):
    user_id = payload.get("user_id") or payload.get("userId")
    query = payload.get("query") or payload.get("question") or ""
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    limit = int(payload.get("limit", 5))
    return pipeline.search(query, user_id=user_id, limit=limit)


@router.post("/query")
def query_documents(payload: dict):
    user_id = payload.get("user_id") or payload.get("userId")
    question = payload.get("question") or payload.get("query") or ""
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    if not question:
        raise HTTPException(status_code=400, detail="question is required")
    context = pipeline.build_context(question, user_id=user_id, limit=int(payload.get("limit", 5)))
    return {
        "question": question,
        "user_id": user_id,
        "top_documents": context["documents"],
        "context": context["context_text"],
        "justification": context["justification"],
    }
