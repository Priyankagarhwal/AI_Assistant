from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.document_service import (
    get_documents_by_workspace,
    delete_document
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.get("/{workspace_id}")
def get_documents(
    workspace_id: str,
    db: Session = Depends(get_db)
):
    return get_documents_by_workspace(db, workspace_id)


@router.delete("/{document_id}")
def remove_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    document = delete_document(db, document_id)

    if not document:
        return {
            "success": False,
            "message": "Document not found"
        }

    return {
        "success": True,
        "message": "Document deleted successfully"
    }