from functools import lru_cache

from langchain_chroma import Chroma

from app.config.settings import settings
from app.embeddings.embedding_model import get_embedding_model


@lru_cache
def get_vector_db() -> Chroma:
    """One persistent Chroma collection; workspaces are isolated with a metadata filter."""
    return Chroma(
        collection_name=settings.CHROMA_COLLECTION,
        persist_directory=settings.CHROMA_DB_PATH,
        embedding_function=get_embedding_model(),
        # Cosine distance matches the normalised embeddings.
        collection_metadata={"hnsw:space": "cosine"},
    )
