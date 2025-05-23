# app/routes/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ingestion import process_and_store_document
from app.db.metadata import save_metadata
import uuid

router = APIRouter()

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        document_id = str(uuid.uuid4())
        chunks = await process_and_store_document(file, document_id)
        save_metadata(document_id=document_id, filename=file.filename, chunks=chunks)
        return {
            "status": "success",
            "document_id": document_id,
            "chunk_count": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
