import os

from app.config.settings import settings
from app.rag import chat as rag_chat
from app.rag.retriever import retrieve
from app.utils.text_splitter import split_pages
from tests.conftest import make_pdf, upload

PAGES = [
    "Photosynthesis converts sunlight water and carbon dioxide into glucose and oxygen inside chloroplasts.",
    "Mitochondria are the powerhouse of the cell and produce ATP through cellular respiration.",
]


# ---------- chunking ----------

def test_split_pages_keeps_page_numbers():
    chunks = split_pages([(1, "a " * 400), (2, "b " * 10)])
    assert {p for p, _ in chunks} == {1, 2}
    assert all(len(text) <= settings.CHUNK_SIZE for _, text in chunks)


# ---------- upload validation ----------

def test_upload_rejects_non_pdf_extension(client, workspace):
    r = client.post(
        "/upload/pdf",
        data={"workspace_id": workspace},
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )
    assert r.status_code == 415


def test_upload_rejects_fake_pdf(client, workspace):
    r = client.post(
        "/upload/pdf",
        data={"workspace_id": workspace},
        files={"file": ("fake.pdf", b"not really a pdf", "application/pdf")},
    )
    assert r.status_code == 415


def test_upload_unknown_workspace_is_404(client):
    assert upload(client, "does-not-exist", PAGES).status_code == 404


def test_upload_filename_cannot_escape_upload_dir(client, workspace):
    r = upload(client, workspace, PAGES, filename="../../evil.pdf")
    assert r.status_code == 201
    body = r.json()
    assert body["filename"] == "evil.pdf"
    stored = os.path.join(settings.UPLOAD_DIR, f"{body['document_id']}.pdf")
    assert os.path.exists(stored)


def test_upload_indexes_pages(client, workspace):
    r = upload(client, workspace, PAGES)
    assert r.status_code == 201
    body = r.json()
    assert body["pages_indexed"] == 2
    assert body["chunks_created"] >= 2
    docs = client.get(f"/documents/{workspace}").json()
    assert [d["filename"] for d in docs] == ["doc.pdf"]


# ---------- chat ----------

def test_chat_returns_page_level_sources(client, workspace):
    upload(client, workspace, PAGES)
    r = client.post("/chat/", json={"workspace_id": workspace, "question": "What do mitochondria produce?"})
    assert r.status_code == 200
    body = r.json()
    assert body["answer"].startswith("Answer based on context")
    top = body["sources"][0]
    assert top["filename"] == "doc.pdf" and top["page"] == 2 and top["id"] == 1


def test_off_topic_question_is_not_answered(client, workspace, fake_llm):
    upload(client, workspace, PAGES)
    r = client.post("/chat/", json={"workspace_id": workspace, "question": "Who won the football world cup?"})
    assert r.json()["answer"] == rag_chat.NOT_FOUND
    assert r.json()["sources"] == []
    # The answer LLM is never called when nothing relevant was retrieved.
    assert all(s != rag_chat.ANSWER_SYSTEM_PROMPT for s, _ in fake_llm.calls)


def test_follow_up_question_is_rewritten_with_history(client, workspace, fake_llm):
    upload(client, workspace, PAGES)
    r = client.post(
        "/chat/",
        json={
            "workspace_id": workspace,
            "question": "What do they produce?",
            "history": [{"question": "Tell me about mitochondria", "answer": "They are organelles."}],
        },
    )
    assert r.status_code == 200
    assert r.json()["standalone_question"].startswith("standalone:")
    assert any(s == rag_chat.REWRITE_SYSTEM_PROMPT for s, _ in fake_llm.calls)


def test_workspaces_are_isolated(client, workspace):
    upload(client, workspace, PAGES)
    other = client.post("/workspace/", json={"name": "Other"}).json()["workspace_id"]
    try:
        assert retrieve(other, "mitochondria ATP") == []
    finally:
        client.delete(f"/workspace/{other}")


def test_chat_saves_history(client, workspace):
    upload(client, workspace, PAGES)
    client.post("/chat/", json={"workspace_id": workspace, "question": "What is photosynthesis?"})
    history = client.get(f"/chat/history/{workspace}").json()
    assert len(history) == 1 and history[0]["question"] == "What is photosynthesis?"


# ---------- deletion consistency ----------

def test_deleting_document_removes_vectors_and_file(client, workspace):
    doc_id = upload(client, workspace, PAGES).json()["document_id"]
    assert retrieve(workspace, "mitochondria ATP")
    assert client.delete(f"/documents/{doc_id}").status_code == 200
    assert retrieve(workspace, "mitochondria ATP") == []
    assert not os.path.exists(os.path.join(settings.UPLOAD_DIR, f"{doc_id}.pdf"))
    assert client.delete(f"/documents/{doc_id}").status_code == 404


def test_deleting_workspace_removes_everything(client):
    ws = client.post("/workspace/", json={"name": "Temp"}).json()["workspace_id"]
    upload(client, ws, PAGES)
    client.post("/chat/", json={"workspace_id": ws, "question": "photosynthesis"})
    assert client.delete(f"/workspace/{ws}").status_code == 200
    assert retrieve(ws, "photosynthesis glucose") == []
    assert client.get(f"/documents/{ws}").json() == []
    assert client.get(f"/chat/history/{ws}").json() == []


# ---------- summary ----------

def test_summary_uses_every_chunk_with_map_reduce(client, workspace, fake_llm, monkeypatch):
    monkeypatch.setattr(settings, "SUMMARY_BATCH_CHARS", 150)
    upload(client, workspace, PAGES)
    r = client.post("/summary/", json={"workspace_id": workspace})
    assert r.status_code == 200
    body = r.json()
    assert body["summary"] == "FINAL SUMMARY"
    map_calls = [c for c in fake_llm.calls if c[0] == rag_chat.MAP_PROMPT]
    assert len(map_calls) >= 2  # content was split across several LLM calls


def test_make_pdf_helper_is_valid():
    from io import BytesIO

    from pypdf import PdfReader

    reader = PdfReader(BytesIO(make_pdf(["hello world"])))
    assert "hello world" in reader.pages[0].extract_text()
