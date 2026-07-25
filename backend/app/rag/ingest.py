from langchain_core.documents import Document
from app.database.chroma_db import get_vector_db


def ingest_chunks(chunks, filename, workspace_id):

    docs = []

    for i, chunk in enumerate(chunks):
        docs.append(
            Document(
                page_content=chunk,
                metadata={
                    "workspace_id": workspace_id,
                    "filename": filename,
                    "chunk": i
                }
            )
        )

    db = get_vector_db()
    db.add_documents(docs)

    return len(docs)