from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Workspace, Document, ChatHistory

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def get_dashboard(db: Session = Depends(get_db)):

    total_workspaces = db.query(Workspace).count()
    total_documents = db.query(Document).count()
    total_chats = db.query(ChatHistory).count()

    return {
        "total_workspaces": total_workspaces,
        "total_documents": total_documents,
        "total_chats": total_chats
    }