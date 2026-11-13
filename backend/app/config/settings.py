from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All runtime configuration. Every value can be overridden in backend/.env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "KnowledgeHub AI"
    APP_VERSION: str = "1.1.0"
    APP_DESCRIPTION: str = "RAG-based question answering over workspaces of PDF documents"

    # LLM (Groq)
    GROQ_API_KEY: str = ""
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    LLM_TEMPERATURE: float = 0.0

    # Embeddings / vector store
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHROMA_DB_PATH: str = "storage/chroma"
    CHROMA_COLLECTION: str = "knowledgehub"

    # Relational DB + file storage
    DATABASE_URL: str = "sqlite:///knowledgehub.db"
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_MB: int = 25

    # Chunking
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Retrieval
    RETRIEVAL_K: int = 4
    # Chunks scoring below this cosine relevance (0..1) are dropped, so off-topic
    # questions get "not found" instead of an answer built on unrelated text.
    MIN_RELEVANCE_SCORE: float = 0.25
    # Number of previous Q/A turns used to rewrite follow-up questions.
    MAX_HISTORY_TURNS: int = 4

    # Summary (map-reduce): max characters of chunk text per LLM call.
    SUMMARY_BATCH_CHARS: int = 12000

    # OCR for scanned pages (optional). Leave paths empty to use tesseract/poppler from PATH.
    ENABLE_OCR: bool = True
    TESSERACT_CMD: Optional[str] = None
    POPPLER_PATH: Optional[str] = None

    # Comma-separated list of allowed frontend origins.
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
