from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from app.core.config import settings

def get_llm():
    return ChatOllama(
        model=settings.OLLAMA_LLM_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0
    )

def get_embedding():
    return OllamaEmbeddings(
        model=settings.OLLAMA_EMBEDDING_MODEL,
        base_url=settings.OLLAMA_BASE_URL
    )
