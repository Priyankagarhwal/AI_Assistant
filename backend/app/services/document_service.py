import os
import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.database.models import Document
from app.rag.ingest import delete_document_vectors


def new_document_id() -> str:
    return str(uuid.uuid4())


def save_document(
    db: Session,
    workspace_id: str,
    filename: str,
    file_path: str,
    document_id: Optional[str] = None,
) -> Document:
    document = Document(
        document_id=document_id or new_document_id(),
        workspace_id=workspace_id,
        filename=filename,
        file_path=file_path,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def get_documents_by_workspace(db: Session, workspace_id: str) -> List[Document]:
    return (
        db.query(Document)
        .filter(Document.workspace_id == workspace_id)
        .order_by(Document.uploaded_at.desc())
        .all()
    )


def remove_file(path: str) -> None:
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except OSError as exc:
        logger.warning("Could not delete file %s: %s", path, exc)


def delete_document(db: Session, document_id: str) -> Optional[Document]:
    """Delete the DB row, its vectors in Chroma and the stored PDF."""
    document = db.query(Document).filter(Document.document_id == document_id).first()
    if not document:
        return None

    # Vectors first: if this fails the row still exists and the delete can be retried.
    delete_document_vectors(document_id)
    db.delete(document)
    db.commit()
    remove_file(document.file_path)
    return document
