# app/services/generator.py
import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOpenAI(
    model="meta-llama/llama-3.3-8b-instruct:free",
    temperature=0.3,
    base_url=os.getenv("OPENAI_API_BASE"), 
)


def generate_answer(question: str, context_chunks: List[str]) -> str:
    context = "\n\n".join(context_chunks)

    messages = [
        SystemMessage(content="You are a helpful assistant. Answer based only on the provided context."),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {question}")
    ]

    response = llm(messages)
    return response.content.strip()
