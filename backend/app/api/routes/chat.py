from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import ChatHistory
from app.rag.retriever import retrieve
from app.rag.chat import ask_llm
from app.services.chat_service import save_chat

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    workspace_id: str
    question: str


@router.post("/")
async def chat(
    req: ChatRequest,
    db: Session = Depends(get_db)
):

    # Retrieve relevant chunks
    docs = retrieve(
        workspace_id=req.workspace_id,
        query=req.question
    )

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Generate answer
    answer = ask_llm(
        context=context,
        question=req.question
    )

    # Save chat in SQLite
    save_chat(
        db=db,
        workspace_id=req.workspace_id,
        question=req.question,
        answer=answer
    )

    # Return response
    return {
        "workspace_id": req.workspace_id,
        "question": req.question,
        "answer": answer,
        "sources": list(
            {
                doc.metadata.get("filename", "Unknown")
                for doc in docs
            }
        )
    }


@router.get("/history/{workspace_id}")
def get_chat_history(
    workspace_id: str,
    db: Session = Depends(get_db)
):

    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.workspace_id == workspace_id)
        .order_by(ChatHistory.created_at.desc())
        .all()
    )

    return chats