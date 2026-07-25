from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.workspace_service import create_workspace, get_all_workspaces, delete_workspace

router = APIRouter(
    prefix="/workspace",
    tags=["Workspace"]
)


class WorkspaceRequest(BaseModel):
    name: str
    description: str = ""


@router.get("/")
def get_workspaces(db: Session = Depends(get_db)):
    return get_all_workspaces(db)


@router.post("/")
def create(
    req: WorkspaceRequest,
    db: Session = Depends(get_db)
):
    return create_workspace(
        db=db,
        name=req.name,
        description=req.description
    )


@router.delete("/{workspace_id}")
def remove_workspace(
    workspace_id: str,
    db: Session = Depends(get_db)
):
    workspace = delete_workspace(db, workspace_id)
    if not workspace:
        return {"success": False, "message": "Workspace not found"}
    return {"success": True, "message": "Workspace deleted successfully"}