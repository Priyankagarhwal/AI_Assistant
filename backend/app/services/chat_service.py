import uuid

from sqlalchemy.orm import Session

from app.database.models import ChatHistory


def save_chat(
    db: Session,
    workspace_id: str,
    question: str,
    answer: str
):

    chat = ChatHistory(
        chat_id=str(uuid.uuid4()),
        workspace_id=workspace_id,
        question=question,
        answer=answer
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat