"""Test setup: isolated temp storage, an offline embedder and a fake LLM.

No network, no Groq key and no model download are needed to run the suite.
"""

import hashlib
import math
import os
import re
import sys
import tempfile

import pytest

_TMP = tempfile.mkdtemp(prefix="kh-tests-")
os.environ.update(
    {
        "GROQ_API_KEY": "test-key",
        "DATABASE_URL": f"sqlite:///{_TMP}/test.db",
        "CHROMA_DB_PATH": f"{_TMP}/chroma",
        "UPLOAD_DIR": f"{_TMP}/uploads",
        "ENABLE_OCR": "false",
        "CHUNK_SIZE": "300",
        "CHUNK_OVERLAP": "50",
    }
)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.embeddings import Embeddings  # noqa: E402


class BagOfWordsEmbeddings(Embeddings):
    """Deterministic hashed bag-of-words vectors: texts sharing words score higher."""

    dim = 512

    def _embed(self, text: str):
        vec = [0.0] * self.dim
        for token in re.findall(r"[a-z0-9]+", text.lower()):
            idx = int(hashlib.md5(token.encode()).hexdigest(), 16) % self.dim
            vec[idx] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def embed_documents(self, texts):
        return [self._embed(t) for t in texts]

    def embed_query(self, text):
        return self._embed(text)


class FakeLLM:
    """Records prompts and returns predictable answers."""

    def __init__(self):
        self.calls = []

    def __call__(self, system: str, user: str) -> str:
        from app.rag import chat as rag_chat

        self.calls.append((system, user))
        if system == rag_chat.REWRITE_SYSTEM_PROMPT:
            return "standalone: " + user.rsplit("Latest question:", 1)[-1].strip()
        if system == rag_chat.ANSWER_SYSTEM_PROMPT:
            return "Answer based on context [1]"
        if system == rag_chat.MAP_PROMPT:
            return f"- partial summary of {len(user)} chars"
        return "FINAL SUMMARY"


def make_pdf(pages):
    """Build a minimal valid PDF with one line of text per page (no extra deps)."""
    objects = []
    n = len(pages)
    font_id = 3 + 2 * n
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(n))
    objects.append("<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {n} >>")
    for i, text in enumerate(pages):
        safe = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream = f"BT /F1 10 Tf 40 750 Td ({safe}) Tj ET"
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {4 + 2 * i} 0 R >>"
        )
        objects.append(f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream")
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    out = b"%PDF-1.4\n"
    offsets = []
    for num, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{num} 0 obj\n{body}\nendobj\n".encode("latin-1")
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return out


@pytest.fixture(scope="session", autouse=True)
def _offline_embeddings():
    from app.database import chroma_db

    chroma_db.get_vector_db.cache_clear()
    chroma_db.get_embedding_model = lambda: BagOfWordsEmbeddings()
    yield


@pytest.fixture()
def fake_llm(monkeypatch):
    from app.rag import chat as rag_chat

    llm = FakeLLM()
    monkeypatch.setattr(rag_chat, "_invoke", llm)
    return llm


@pytest.fixture()
def client(fake_llm):
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def workspace(client):
    r = client.post("/workspace/", json={"name": "Test WS", "description": "d"})
    assert r.status_code == 201
    ws_id = r.json()["workspace_id"]
    yield ws_id
    client.delete(f"/workspace/{ws_id}")


def upload(client, workspace_id, pages, filename="doc.pdf"):
    return client.post(
        "/upload/pdf",
        data={"workspace_id": workspace_id},
        files={"file": (filename, make_pdf(pages), "application/pdf")},
    )
