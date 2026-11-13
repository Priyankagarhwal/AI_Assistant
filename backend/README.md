# KnowledgeHub AI — Backend

FastAPI service for ingestion, retrieval and answering. See the [root README](../README.md) for setup and the API table.

```
app/
├── api/routes/     HTTP endpoints (workspace, upload, documents, chat, summary, dashboard, health)
├── config/         Pydantic settings, all overridable from .env
├── database/       SQLAlchemy (SQLite) models + Chroma vector store
├── embeddings/     Hugging Face sentence-transformers model (lazy-loaded)
├── loaders/        PDF text extraction with per-page OCR fallback
├── rag/            ingest · retriever (threshold) · chat (rewrite, answer, map-reduce summary)
├── services/       DB logic incl. consistent deletes (rows + vectors + files)
└── utils/          Page-aware text splitter
eval/               Retrieval evaluation (Hit@k, MRR)
scripts/            reindex.py — rebuild Chroma from stored PDFs
tests/              Offline pytest suite
```

```bash
pytest -q                                   # run tests
python -m scripts.reindex                   # rebuild vector index
python -m eval.eval_retrieval <file.json>   # measure retrieval quality
```
