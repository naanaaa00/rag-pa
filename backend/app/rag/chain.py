from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from app.core.ollama import get_llm

SYSTEM_PROMPT = """
Kamu adalah asisten AI yang menganalisis dokumen rapat.
Jawablah pertanyaan HANYA berdasarkan konteks yang diberikan.
Jika jawaban tidak ditemukan di konteks, katakan dengan jujur.
"""

def format_context(docs: list[Document]) -> str:
    return "\n\n".join(
        f"[{doc.metadata.get('content_type')} - {doc.metadata.get('section', '-')}] {doc.page_content}"
        for doc in docs
    )

def run_rag(query: str, docs: list[Document]) -> str:
    llm = get_llm()

    context = format_context(docs)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "Konteks:\n{context}\n\nPertanyaan:\n{question}")
        ]
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": query
        }
    )

    return response.content
