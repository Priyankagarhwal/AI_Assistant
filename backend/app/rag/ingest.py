from typing import List, Tuple

from langchain_core.documents import Document

from app.database.chroma_db import get_vector_db


def ingest_chunks(
    chunks: List[Tuple[int, str]],
    filename: str,
    workspace_id: str,
    document_id: str,
) -> int:
    """Embed and store chunks. IDs are deterministic so a document can be deleted later."""
    if not chunks:
        return 0

    docs = [
        Document(
            page_content=text,
            metadata={
                "workspace_id": workspace_id,
                "document_id": document_id,
                "filename": filename,
                "page": page,
                "chunk": i,
            },
        )
        for i, (page, text) in enumerate(chunks)
    ]
    ids = [f"{document_id}:{i}" for i in range(len(docs))]

    get_vector_db().add_documents(docs, ids=ids)
    return len(docs)


def delete_document_vectors(document_id: str) -> None:
    get_vector_db().delete(where={"document_id": document_id})


def delete_workspace_vectors(workspace_id: str) -> None:
    get_vector_db().delete(where={"workspace_id": workspace_id})
