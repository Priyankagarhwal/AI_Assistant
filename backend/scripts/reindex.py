"""Rebuild the Chroma index from the PDFs recorded in SQLite.

Run from backend/:   python -m scripts.reindex

Use after changing EMBEDDING_MODEL, CHUNK_SIZE / CHUNK_OVERLAP, or upgrading from
v1.0 (which stored vectors without document_id/page metadata).
"""

import os

from app.database.database import SessionLocal
from app.database.models import Document
from app.loaders.pdf_loader import load_pdf
from app.rag.ingest import delete_document_vectors, ingest_chunks
from app.utils.text_splitter import split_pages


def main() -> None:
    db = SessionLocal()
    try:
        documents = db.query(Document).all()
        print(f"Re-indexing {len(documents)} documents...")
        for doc in documents:
            if not os.path.exists(doc.file_path):
                print(f"  SKIP  {doc.filename}: file missing at {doc.file_path}")
                continue
            delete_document_vectors(doc.document_id)
            chunks = split_pages(load_pdf(doc.file_path))
            n = ingest_chunks(chunks, doc.filename, doc.workspace_id, doc.document_id)
            print(f"  OK    {doc.filename}: {n} chunks")
    finally:
        db.close()


if __name__ == "__main__":
    main()
