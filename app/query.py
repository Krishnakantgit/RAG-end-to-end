# app/routes/query.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.retrieval import retrieve_chunks
from app.services.generator import generate_answer

router = APIRouter()

class QueryRequest(BaseModel):
    document_id: str
    question: str

@router.post("/")
async def query_document(request: QueryRequest):
    try:
        relevant_chunks = retrieve_chunks(request.document_id, request.question)
        if not relevant_chunks:
            return {"answer": "No relevant information found in the document."}

        answer = generate_answer(request.question, relevant_chunks)
        return {"answer": answer, "context": relevant_chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
