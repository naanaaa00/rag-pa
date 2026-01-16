from langchain_postgres import PGVector
from app.core.config import settings
from app.core.ollama import get_embedding

COLLECTION_NAME = "meeting_docs"

def get_vectorstore():
    return PGVector(
        embeddings=get_embedding(),
        collection_name=COLLECTION_NAME,
        connection=settings.DATABASE_URL,
        use_jsonb=True,  # metadata searchable
    )
