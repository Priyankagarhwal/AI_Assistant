from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.core.logger import logger
from app.database.database import get_db
from app.database.models import ChatHistory
from app.rag.chat import LLMNotConfiguredError, answer_question, condense_question
from app.rag.retriever import retrieve
from app.services.chat_service import save_chat
from app.services.workspace_service import get_workspace

router = APIRouter(prefix="/chat", tags=["Chat"])


class Turn(BaseModel):
    question: str
    answer: str


class ChatRequest(BaseModel):
    workspace_id: str
    question: str = Field(..., min_length=1, max_length=2000)
    # Previous turns of the current conversation (sent by the client), used to
    # resolve follow-up questions such as "what are its limitations?".
    history: List[Turn] = Field(default_factory=list)


# Plain `def`: the Groq and embedding calls are blocking, so this runs in the thread pool.
@router.post("/")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    if get_workspace(db, req.workspace_id) is None:
        raise HTTPException(status_code=404, detail="Workspace not found.")

    question = req.question.strip()
    history = [(t.question, t.answer) for t in req.history[-settings.MAX_HISTORY_TURNS:]]

    try:
        search_query = condense_question(question, history)
        results = retrieve(workspace_id=req.workspace_id, query=search_query)
        docs = [doc for doc, _ in results]
        answer = answer_question(search_query, docs)
    except LLMNotConfiguredError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # Groq rate limit / network errors
        logger.exception("Chat failed")
        raise HTTPException(status_code=502, detail="The language model request failed.") from exc

    save_chat(db=db, workspace_id=req.workspace_id, question=question, answer=answer)

    # Sources are numbered in the same order as the [n] citations in the answer.
    sources = [
        {
            "id": i,
            "filename": doc.metadata.get("filename", "unknown"),
            "page": doc.metadata.get("page"),
            "score": round(score, 3),
            "snippet": doc.page_content[:200],
        }
        for i, (doc, score) in enumerate(results, start=1)
    ]

    return {
        "workspace_id": req.workspace_id,
        "question": question,
        "standalone_question": search_query,
        "answer": answer,
        "sources": sources,
    }


@router.get("/history/{workspace_id}")
def get_chat_history(workspace_id: str, db: Session = Depends(get_db)):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.workspace_id == workspace_id)
        .order_by(ChatHistory.created_at.desc())
        .all()
    )


@router.delete("/{chat_id}")
def delete_chat(chat_id: str, db: Session = Depends(get_db)):
    chat_row = db.query(ChatHistory).filter(ChatHistory.chat_id == chat_id).first()
    if not chat_row:
        raise HTTPException(status_code=404, detail="Chat not found.")
    db.delete(chat_row)
    db.commit()
    return {"success": True, "message": "Chat deleted successfully"}
