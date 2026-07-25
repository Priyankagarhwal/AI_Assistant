from pydantic import BaseModel
from typing import Optional


class Workspace(BaseModel):
    workspace_id: str
    name: str
    description: Optional[str] = None