from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
import os
import shutil

from app.database.database import get_db
from app.database.models import Workspace
from app.loaders.pdf_loader import load_pdf
from app.rag.ingest import ingest_chunks
from app.services.document_service import save_document
from app.utils.text_splitter import split_text

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/pdf")
async def upload_pdf(
    workspace_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        workspace = (
            db.query(Workspace)
            .filter(Workspace.workspace_id == workspace_id)
            .first()
        )

        if workspace is None:
            return {
                "success": False,
                "message": "Workspace not found."
            }

        if not file.filename.endswith(".pdf"):
            return {
                "success": False,
                "message": "Only PDF files are allowed."
            }

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = save_document(
            db=db,
            workspace_id=workspace_id,
            filename=file.filename,
            file_path=file_path
        )

        text = load_pdf(file_path)

        chunks = split_text(text)

        stored = ingest_chunks(
            chunks=chunks,
            filename=file.filename,
            workspace_id=workspace_id
        )

        return {
            "success": True,
            "document_id": document.document_id,
            "workspace_id": workspace_id,
            "filename": file.filename,
            "chunks_created": len(chunks),
            "chunks_stored": stored
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }