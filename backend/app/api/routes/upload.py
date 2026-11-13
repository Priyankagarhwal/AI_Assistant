import os
import shutil

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.core.logger import logger
from app.database.database import get_db
from app.loaders.pdf_loader import load_pdf
from app.rag.ingest import delete_document_vectors, ingest_chunks
from app.services.document_service import new_document_id, remove_file, save_document
from app.services.workspace_service import get_workspace
from app.utils.text_splitter import split_pages

router = APIRouter(prefix="/upload", tags=["Upload"])


# Plain `def` (not async): parsing, OCR and embedding are CPU-bound, so FastAPI runs
# this in its thread pool instead of blocking the event loop.
@router.post("/pdf", status_code=201)
def upload_pdf(
    workspace_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if get_workspace(db, workspace_id) is None:
        raise HTTPException(status_code=404, detail="Workspace not found.")

    # The browser-sent name is only used for display, never as a path on disk,
    # which prevents path traversal ("../../x.pdf") and overwriting other uploads.
    original_name = os.path.basename(file.filename or "").strip() or "document.pdf"
    if not original_name.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Only PDF files are allowed.")

    # Check file signature, not just the extension.
    if file.file.read(5) != b"%PDF-":
        raise HTTPException(status_code=415, detail="File is not a valid PDF.")
    file.file.seek(0, os.SEEK_END)
    size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)
    if size_mb > settings.MAX_UPLOAD_MB:
        raise HTTPException(
            status_code=413, detail=f"File exceeds {settings.MAX_UPLOAD_MB} MB limit."
        )

    document_id = new_document_id()
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, f"{document_id}.pdf")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        pages = load_pdf(file_path)
        chunks = split_pages(pages)
        if not chunks:
            raise HTTPException(
                status_code=422,
                detail="No readable text found in this PDF (and OCR found none).",
            )
        stored = ingest_chunks(
            chunks=chunks,
            filename=original_name,
            workspace_id=workspace_id,
            document_id=document_id,
        )
        # The DB row is written only after indexing succeeds, so a failed upload
        # never leaves a document that the UI lists but chat cannot find.
        save_document(
            db=db,
            workspace_id=workspace_id,
            filename=original_name,
            file_path=file_path,
            document_id=document_id,
        )
    except HTTPException:
        remove_file(file_path)
        raise
    except Exception as exc:
        logger.exception("Upload failed for %s", original_name)
        delete_document_vectors(document_id)
        remove_file(file_path)
        raise HTTPException(status_code=500, detail="Failed to process PDF.") from exc

    logger.info("Indexed %s: %d pages, %d chunks", original_name, len(pages), stored)
    return {
        "success": True,
        "document_id": document_id,
        "workspace_id": workspace_id,
        "filename": original_name,
        "pages_indexed": len(pages),
        "chunks_created": stored,
    }
