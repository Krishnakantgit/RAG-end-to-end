# app/services/ingestion.py
import os
import tempfile
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.utils.pdf_parser import extract_text_from_pdf
import shutil
from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize FAISS store directory
FAISS_DIR = "vector_store"
os.makedirs(FAISS_DIR, exist_ok=True)

async def process_and_store_document(file, document_id: str) -> List[str]:
    # Save file temporarily
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text from PDF
    text = extract_text_from_pdf(file_path)
    shutil.rmtree(temp_dir)

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)

    # Generate embeddings
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)

    # Save FAISS index with document ID
    doc_store_path = os.path.join(FAISS_DIR, f"{document_id}")
    vectorstore.save_local(doc_store_path)

    return chunks
