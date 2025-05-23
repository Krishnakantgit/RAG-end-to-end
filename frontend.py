# frontend.py
import streamlit as st
import requests
import json

st.set_page_config(page_title="RAG PDF QA", layout="centered")
st.title("📄 Upload PDF + Ask Questions (RAG App)")

API_URL = "http://localhost:8000"

# --- Upload PDF ---
st.header("Step 1: Upload a PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file and st.button("Upload"):
    with st.spinner("Uploading and processing..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post(f"{API_URL}/upload/", files=files)

    if response.status_code == 200:
        data = response.json()
        st.success("Uploaded successfully!")
        st.session_state["document_id"] = data["document_id"]
        st.write("**Document ID:**", data["document_id"])
        st.write("**Chunks stored:**", data["chunk_count"])
    else:
        st.error(f"Upload failed: {response.text}")

# --- Ask Questions ---
st.header("Step 2: Ask a Question")
document_id = st.text_input("Document ID", value=st.session_state.get("document_id", ""))
question = st.text_area("Enter your question")

if st.button("Get Answer") and document_id and question:
    with st.spinner("Thinking..."):
        payload = {"document_id": document_id, "question": question}
        response = requests.post(f"{API_URL}/query/", json=payload)

    if response.status_code == 200:
        answer = response.json().get("answer", "No answer returned.")
        st.success("Answer:")
        st.write(answer)
    else:
        st.error(f"Query failed: {response.text}")

# --- Metadata View ---
st.sidebar.title("📚 Uploaded Documents")
if st.sidebar.button("Show Metadata"):
    response = requests.get(f"{API_URL}/upload/metadata/")
    if response.status_code == 200:
        docs = response.json()
        for doc in docs:
            st.sidebar.markdown(f"**{doc['filename']}**\n- ID: `{doc['document_id']}`")
    else:
        st.sidebar.error("Failed to load metadata.")
