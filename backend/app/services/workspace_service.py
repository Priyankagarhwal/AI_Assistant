import uuid

from sqlalchemy.orm import Session

from app.database.models import Workspace


def create_workspace(db: Session, name: str, description: str):

    workspace = Workspace(
        workspace_id=str(uuid.uuid4()),
        name=name,
        description=description
    )

    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    return workspace


def get_all_workspaces(db: Session):
    return db.query(Workspace).all()


def delete_workspace(db: Session, workspace_id: str):

    workspace = (
        db.query(Workspace)
        .filter(Workspace.workspace_id == workspace_id)
        .first()
    )

    if not workspace:
        return None

    db.delete(workspace)
    db.commit()

    return workspace