import uuid

from sqlalchemy.orm import Session

from app.database.models import Document


def save_document(
    db: Session,
    workspace_id: str,
    filename: str,
    file_path: str
):
    document = Document(
        document_id=str(uuid.uuid4()),
        workspace_id=workspace_id,
        filename=filename,
        file_path=file_path
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_documents_by_workspace(
    db: Session,
    workspace_id: str
):
    return (
        db.query(Document)
        .filter(Document.workspace_id == workspace_id)
        .all()
    )


def delete_document(
    db: Session,
    document_id: str
):
    document = (
        db.query(Document)
        .filter(Document.document_id == document_id)
        .first()
    )

    if document:
        db.delete(document)
        db.commit()

    return document