from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "KnowledgeHub AI"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "An Intelligent Multi-Source RAG Platform"

    GROQ_API_KEY: str

    MODEL_NAME: str = "llama-3.3-70b-versatile"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    CHROMA_DB_PATH: str = "storage/chroma"

    DOCUMENT_PATH: str = "storage/documents"

    class Config:
        env_file = ".env"


settings = Settings()