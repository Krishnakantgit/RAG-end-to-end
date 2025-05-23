import os
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_DIR = "vector_store"

# HuggingFace embeddings 
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def retrieve_chunks(document_id: str, query: str, k: int = 5) -> List[str]:
    index_path = os.path.join(VECTOR_DIR, document_id)
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"No vector store found for document ID: {document_id}")

    # Load FAISS index and search
    vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    results = vectorstore.similarity_search(query, k=k)
    return [r.page_content for r in results]
