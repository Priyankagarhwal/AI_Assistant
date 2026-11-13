from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.database.database import get_db
from app.rag.chat import LLMNotConfiguredError, summarize
from app.rag.retriever import get_workspace_chunks
from app.services.workspace_service import get_workspace

router = APIRouter(prefix="/summary", tags=["Summary"])


class SummaryRequest(BaseModel):
    workspace_id: str


@router.post("/")
def generate_summary(req: SummaryRequest, db: Session = Depends(get_db)):
    if get_workspace(db, req.workspace_id) is None:
        raise HTTPException(status_code=404, detail="Workspace not found.")

    # A summary must cover the whole workspace, so we read every chunk in order
    # instead of running a similarity search for the word "summarize".
    docs = get_workspace_chunks(req.workspace_id)
    if not docs:
        return {"workspace_id": req.workspace_id, "summary": "No documents found in this workspace."}

    try:
        summary = summarize(docs)
    except LLMNotConfiguredError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Summary failed")
        raise HTTPException(status_code=502, detail="The language model request failed.") from exc

    return {"workspace_id": req.workspace_id, "chunks_used": len(docs), "summary": summary}
