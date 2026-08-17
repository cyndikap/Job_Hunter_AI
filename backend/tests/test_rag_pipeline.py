from app.services.rag_pipeline import RAGPipeline


def test_rag_pipeline_builds_context_from_documents():
    pipeline = RAGPipeline(use_memory_fallback=True)

    docs = [
        {
            "id": "cv-1",
            "user_id": "user-1",
            "document_type": "cv",
            "source_id": "profile-1",
            "content": "Senior Data Engineer with Azure Databricks and Python skills.",
            "created_at": "2026-08-17T00:00:00Z",
        },
        {
            "id": "job-1",
            "user_id": "user-1",
            "document_type": "job",
            "source_id": "job-42",
            "content": "Azure Databricks Data Engineer role in Paris with PySpark and SQL.",
            "created_at": "2026-08-17T00:00:00Z",
        },
    ]

    indexed = pipeline.index_documents(docs)
    assert indexed["indexed_count"] == 2

    context = pipeline.build_context(query="Azure Databricks engineer role", user_id="user-1", limit=3)
    assert len(context["documents"]) >= 1
    assert context["context_text"]
