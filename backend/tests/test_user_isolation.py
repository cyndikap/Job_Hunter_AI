from app.services.vector_store import QdrantVectorStore


def test_user_vectors_are_isolated():
    store = QdrantVectorStore(collection_name="user_isolation_test", use_memory_fallback=True)
    store.delete_collection()

    user_a_doc = {
        "id": "a-doc-1",
        "user_id": "user-A",
        "document_type": "cv",
        "source_id": "a-cv",
        "content": "User A: Python and Azure Data Factory experience.",
        "metadata": {"title": "CV A"},
    }
    user_b_doc = {
        "id": "b-doc-1",
        "user_id": "user-B",
        "document_type": "cv",
        "source_id": "b-cv",
        "content": "User B: Java and Kubernetes experience.",
        "metadata": {"title": "CV B"},
    }

    store.upsert_document(user_a_doc, vector=[0.9, 0.1, 0.2])
    store.upsert_document(user_b_doc, vector=[0.1, 0.9, 0.2])

    a_results = store.search(vector=[0.9, 0.1, 0.2], user_id="user-A", limit=10)
    b_results = store.search(vector=[0.1, 0.9, 0.2], user_id="user-B", limit=10)

    assert all(item["user_id"] == "user-A" for item in a_results["results"])
    assert all(item["user_id"] == "user-B" for item in b_results["results"])

    cross_user = store.search(vector=[0.9, 0.1, 0.2], user_id="user-B", limit=10)
    assert all(item["user_id"] == "user-B" for item in cross_user["results"])
