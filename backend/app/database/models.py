from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    workspace_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    documents = relationship(
        "Document",
        back_populates="workspace",
        cascade="all, delete"
    )

    chats = relationship(
        "ChatHistory",
        back_populates="workspace",
        cascade="all, delete"
    )


class Document(Base):
    __tablename__ = "documents"

    document_id = Column(String, primary_key=True, index=True)
    workspace_id = Column(
        String,
        ForeignKey("workspaces.workspace_id"),
        nullable=False
    )

    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Each document belongs to one workspace
    workspace = relationship(
        "Workspace",
        back_populates="documents"
    )
class ChatHistory(Base):
    __tablename__ = "chat_history"

    chat_id = Column(String, primary_key=True, index=True)

    workspace_id = Column(
        String,
        ForeignKey("workspaces.workspace_id"),
        nullable=False
    )

    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    workspace = relationship(
        "Workspace",
        back_populates="chats"
    )