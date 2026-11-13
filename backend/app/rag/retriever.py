from typing import List, Optional, Tuple

from langchain_core.documents import Document

from app.config.settings import settings
from app.database.chroma_db import get_vector_db


def retrieve(
    workspace_id: str,
    query: str,
    k: Optional[int] = None,
    min_score: Optional[float] = None,
) -> List[Tuple[Document, float]]:
    """Top-k chunks from one workspace, keeping only those above the relevance threshold."""
    k = k or settings.RETRIEVAL_K
    min_score = settings.MIN_RELEVANCE_SCORE if min_score is None else min_score

    results = get_vector_db().similarity_search_with_relevance_scores(
        query, k=k, filter={"workspace_id": workspace_id}
    )
    return [(doc, score) for doc, score in results if score >= min_score]


def get_workspace_chunks(workspace_id: str) -> List[Document]:
    """Every chunk in a workspace, in document/page/chunk order (used for summaries)."""
    data = get_vector_db().get(
        where={"workspace_id": workspace_id}, include=["documents", "metadatas"]
    )
    docs = [
        Document(page_content=text, metadata=meta or {})
        for text, meta in zip(data["documents"], data["metadatas"])
    ]
    docs.sort(
        key=lambda d: (
            d.metadata.get("filename", ""),
            d.metadata.get("page", 0),
            d.metadata.get("chunk", 0),
        )
    )
    return docs
