import pytesseract
from pypdf import PdfReader
from pdf2image import convert_from_path
from PIL import Image
import os

# Windows pe Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Poppler path (pdf2image ke liye)
POPPLER_PATH = r"C:\Program Files\poppler\Library\bin"


def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text and page_text.strip():
            text += page_text + "\n"
        else:
            # Image-based page — OCR use karo
            try:
                images = convert_from_path(
                    file_path,
                    first_page=i + 1,
                    last_page=i + 1,
                    poppler_path=POPPLER_PATH if os.path.exists(POPPLER_PATH) else None,
                )
                for img in images:
                    ocr_text = pytesseract.image_to_string(img)
                    if ocr_text.strip():
                        text += ocr_text + "\n"
            except Exception as e:
                text += f"[Page {i+1} OCR failed: {e}]\n"

    return text