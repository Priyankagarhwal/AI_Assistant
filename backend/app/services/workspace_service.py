import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.database.models import Workspace
from app.rag.ingest import delete_workspace_vectors
from app.services.document_service import remove_file


def create_workspace(db: Session, name: str, description: str) -> Workspace:
    workspace = Workspace(
        workspace_id=str(uuid.uuid4()),
        name=name.strip(),
        description=description.strip(),
    )
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace


def get_workspace(db: Session, workspace_id: str) -> Optional[Workspace]:
    return db.query(Workspace).filter(Workspace.workspace_id == workspace_id).first()


def get_all_workspaces(db: Session) -> List[Workspace]:
    return db.query(Workspace).order_by(Workspace.created_at.desc()).all()


def delete_workspace(db: Session, workspace_id: str) -> Optional[Workspace]:
    """Delete a workspace with its documents, chat history, vectors and stored PDFs."""
    workspace = get_workspace(db, workspace_id)
    if not workspace:
        return None

    file_paths = [d.file_path for d in workspace.documents]
    delete_workspace_vectors(workspace_id)
    db.delete(workspace)  # ORM cascade removes documents + chat history rows
    db.commit()
    for path in file_paths:
        remove_file(path)
    return workspace
