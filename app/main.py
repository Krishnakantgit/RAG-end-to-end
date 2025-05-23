# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, query, metadata

app = FastAPI(title="RAG Document QA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(metadata.router, prefix="/upload/metadata", tags=["Metadata"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Pipeline API"}
