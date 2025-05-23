# tests/test_retrieval_query.py
import os
import uuid
import shutil
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.ingestion import process_and_store_document
from app.services.retrieval import retrieve_chunks
from app.services.generator import generate_answer

client = TestClient(app)

TEST_FILE = "tests/sample.pdf"
VECTOR_STORE_DIR = "vector_store"

def setup_module(module):
    
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

def teardown_module(module):

    shutil.rmtree(VECTOR_STORE_DIR, ignore_errors=True)

@pytest.mark.asyncio
async def test_document_ingestion_and_retrieval():
    document_id = str(uuid.uuid4())

    with open(TEST_FILE, "rb") as f:
        class DummyFile:
            filename = "sample.pdf"
            async def read(self): return f.read()

        dummy_file = DummyFile()
        chunks = await process_and_store_document(dummy_file, document_id)
        assert isinstance(chunks, list)
        assert len(chunks) > 0

    retrieved = retrieve_chunks(document_id, "test")
    assert isinstance(retrieved, list)
    assert len(retrieved) > 0

    answer = generate_answer("What is this about?", retrieved)
    assert isinstance(answer, str)
    assert len(answer) > 0

def test_query_endpoint_missing_doc():
    response = client.post("/query/", json={
        "document_id": "fake-id",
        "question": "What is this?"
    })
    assert response.status_code == 500
    assert "No vector store found" in response.json()["detail"]
