from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Ollama
    OLLAMA_BASE_URL: str
    OLLAMA_LLM_MODEL: str
    OLLAMA_EMBEDDING_MODEL: str

    # Database
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
