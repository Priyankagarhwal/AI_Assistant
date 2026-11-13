from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.workspace_service import (
    create_workspace,
    delete_workspace,
    get_all_workspaces,
)

router = APIRouter(prefix="/workspace", tags=["Workspace"])


class WorkspaceRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field("", max_length=500)


@router.get("/")
def get_workspaces(db: Session = Depends(get_db)):
    return get_all_workspaces(db)


@router.post("/", status_code=201)
def create(req: WorkspaceRequest, db: Session = Depends(get_db)):
    if not req.name.strip():
        raise HTTPException(status_code=422, detail="Workspace name cannot be empty.")
    return create_workspace(db=db, name=req.name, description=req.description)


@router.delete("/{workspace_id}")
def remove_workspace(workspace_id: str, db: Session = Depends(get_db)):
    if not delete_workspace(db, workspace_id):
        raise HTTPException(status_code=404, detail="Workspace not found.")
    return {"success": True, "message": "Workspace deleted successfully"}
