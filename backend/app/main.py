from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Tambahkan ini
from app.api.routes.ingest import router as ingest_router
from app.core.langsmith import init_langsmith

init_langsmith()

app = FastAPI(title="Meeting RAG System")

# Konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Izinkan semua asal (bisa dipersempit nanti)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router)