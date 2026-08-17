from app.services.vector_store import QdrantVectorStore


def test_vector_store_insertion_search_and_delete():
    store = QdrantVectorStore(collection_name="test_vectors", use_memory_fallback=True)
    store.delete_collection()

    doc = {
        "id": "doc-1",
        "user_id": "user-1",
        "document_type": "cv",
        "source_id": "cv-1",
        "content": "Azure Data Engineer with Databricks and Python expertise.",
        "metadata": {"title": "CV"},
    }

    insert_result = store.upsert_document(doc, vector=[0.1, 0.2, 0.3])
    assert insert_result["status"] == "ok"

    results = store.search(
        vector=[0.1, 0.2, 0.3],
        user_id="user-1",
        limit=5,
    )
    assert len(results["results"]) >= 1

    delete_result = store.delete_document("doc-1", user_id="user-1")
    assert delete_result["deleted"] in {True, 1}
