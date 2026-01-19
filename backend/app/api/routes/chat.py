from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.rag.retriever import retrieve_documents
from app.rag.chain import run_rag

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    question: str
    meeting_id: Optional[str] = None
    content_type: Optional[str] = None  # summary | transcript
    date: Optional[str] = None

@router.post("/")
def chat(req: ChatRequest):
    metadata_filter = {}

    # Filter HANYA akan aktif jika isinya bukan null, bukan empty, dan bukan tulisan "string"
    if req.meeting_id and req.meeting_id != "string":
        metadata_filter["meeting_id"] = req.meeting_id

    if req.content_type and req.content_type != "string":
        metadata_filter["content_type"] = req.content_type

    if req.date and req.date != "string":
        metadata_filter["date"] = req.date

    # Kalau metadata_filter {} kosong, retrieve_documents akan mencari di SEMUA dokumen
    docs = retrieve_documents(query=req.question, metadata_filter=metadata_filter)

    if not docs:
        return {
            "answer": "Tidak ditemukan konteks yang relevan berdasarkan metadata yang diberikan."
        }

    answer = run_rag(req.question, docs)

    return {
        "answer": answer,
        "sources": [
            {
                "content_type": d.metadata.get("content_type"),
                "section": d.metadata.get("section"),
                "relevance_score": getattr(d, "metadata", {}).get("relevance_score", None) 
                # FlashRank biasanya memberikan skor relevansi
            }
            for d in docs
        ]
    }
