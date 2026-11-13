from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.document_service import delete_document, get_documents_by_workspace

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/{workspace_id}")
def get_documents(workspace_id: str, db: Session = Depends(get_db)):
    return get_documents_by_workspace(db, workspace_id)


@router.delete("/{document_id}")
def remove_document(document_id: str, db: Session = Depends(get_db)):
    if not delete_document(db, document_id):
        raise HTTPException(status_code=404, detail="Document not found.")
    return {"success": True, "message": "Document deleted successfully"}
