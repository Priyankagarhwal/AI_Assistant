from functools import lru_cache

from app.config.settings import settings


@lru_cache
def get_embedding_model():
    """Load the sentence-transformers model once, on first use (not at import time)."""
    from langchain_huggingface import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        # Normalised vectors -> cosine similarity, so relevance scores fall in [0, 1].
        encode_kwargs={"normalize_embeddings": True},
    )
