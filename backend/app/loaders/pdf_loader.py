"""PDF text extraction with per-page OCR fallback for scanned pages."""

from typing import List, Tuple

from pypdf import PdfReader

from app.config.settings import settings
from app.core.logger import logger

# (page_number starting at 1, page_text)
Page = Tuple[int, str]


def _ocr_page(file_path: str, page_number: int) -> str:
    """OCR a single page. Returns "" if OCR tools are missing or OCR fails."""
    try:
        import pytesseract
        from pdf2image import convert_from_path

        if settings.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

        images = convert_from_path(
            file_path,
            first_page=page_number,
            last_page=page_number,
            poppler_path=settings.POPPLER_PATH or None,
        )
        return "\n".join(pytesseract.image_to_string(img) for img in images).strip()
    except Exception as exc:  # missing binaries, corrupt image, etc.
        # Logged, never written into the document text (it would get embedded).
        logger.warning("OCR failed for %s page %d: %s", file_path, page_number, exc)
        return ""


def load_pdf(file_path: str) -> List[Page]:
    """Return the non-empty pages of a PDF as (page_number, text) pairs."""
    reader = PdfReader(file_path)
    pages: List[Page] = []

    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if not text and settings.ENABLE_OCR:
            text = _ocr_page(file_path, index)
        if text:
            pages.append((index, text))

    return pages
