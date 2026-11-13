from typing import Iterable, List, Tuple

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import settings


def _splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )


def split_text(text: str) -> List[str]:
    return _splitter().split_text(text)


def split_pages(pages: Iterable[Tuple[int, str]]) -> List[Tuple[int, str]]:
    """Split page by page so every chunk keeps the page number it came from."""
    splitter = _splitter()
    chunks: List[Tuple[int, str]] = []
    for page_number, text in pages:
        for chunk in splitter.split_text(text):
            chunks.append((page_number, chunk))
    return chunks
