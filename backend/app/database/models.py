from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class Workspace(Base):
    __tablename__ = "workspaces"

    workspace_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=_utcnow)

    documents = relationship(
        "Document", back_populates="workspace", cascade="all, delete-orphan"
    )
    chats = relationship(
        "ChatHistory", back_populates="workspace", cascade="all, delete-orphan"
    )


class Document(Base):
    __tablename__ = "documents"

    document_id = Column(String, primary_key=True, index=True)
    workspace_id = Column(
        String,
        ForeignKey("workspaces.workspace_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    filename = Column(String, nullable=False)  # original name shown in the UI
    file_path = Column(String, nullable=False)  # stored as <document_id>.pdf on disk
    uploaded_at = Column(DateTime, default=_utcnow)

    workspace = relationship("Workspace", back_populates="documents")


class ChatHistory(Base):
    __tablename__ = "chat_history"

    chat_id = Column(String, primary_key=True, index=True)
    workspace_id = Column(
        String,
        ForeignKey("workspaces.workspace_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    created_at = Column(DateTime, default=_utcnow)

    workspace = relationship("Workspace", back_populates="chats")
