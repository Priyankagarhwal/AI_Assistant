"""LLM calls: grounded answering, follow-up rewriting and map-reduce summarisation."""

from functools import lru_cache
from typing import List, Sequence, Tuple

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage

from app.config.settings import settings

NOT_FOUND = "I couldn't find that information in the uploaded documents."

ANSWER_SYSTEM_PROMPT = f"""You are KnowledgeHub AI, an assistant that answers questions \
using ONLY the numbered context passages provided.

Rules:
- Use only facts stated in the context. Do not use outside knowledge.
- After each claim, cite the passage(s) it came from, like [1] or [2][3].
- If the context does not contain the answer, reply exactly: "{NOT_FOUND}"
- Be concise and direct."""

REWRITE_SYSTEM_PROMPT = """Rewrite the user's latest question as a single standalone \
question that can be understood without the conversation. Resolve pronouns such as \
"it", "they" or "that" using the conversation. If it is already standalone, return it \
unchanged. Return only the question."""

MAP_PROMPT = """Summarise the following document excerpts in 5-8 bullet points. \
Keep names, numbers and key terms exactly as written. Use only the excerpts."""

REDUCE_PROMPT = """Combine these partial summaries of the same workspace into one summary with:
1. Overview (2-3 sentences)
2. Key points (bullets)
3. Important terms, entities or figures (bullets)
Do not add information that is not in the partial summaries."""


class LLMNotConfiguredError(RuntimeError):
    pass


@lru_cache
def get_llm():
    if not settings.GROQ_API_KEY:
        raise LLMNotConfiguredError("GROQ_API_KEY is not set in backend/.env")
    from langchain_groq import ChatGroq

    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.MODEL_NAME,
        temperature=settings.LLM_TEMPERATURE,
    )


def _invoke(system: str, user: str) -> str:
    response = get_llm().invoke([SystemMessage(content=system), HumanMessage(content=user)])
    return response.content.strip()


def format_context(docs: Sequence[Document]) -> str:
    blocks = []
    for i, doc in enumerate(docs, start=1):
        src = f"{doc.metadata.get('filename', 'unknown')}, page {doc.metadata.get('page', '?')}"
        blocks.append(f"[{i}] ({src})\n{doc.page_content}")
    return "\n\n".join(blocks)


def condense_question(question: str, history: List[Tuple[str, str]]) -> str:
    """Turn a follow-up ("what about its limitations?") into a standalone search query."""
    if not history:
        return question
    convo = "\n".join(f"User: {q}\nAssistant: {a}" for q, a in history)
    rewritten = _invoke(
        REWRITE_SYSTEM_PROMPT,
        f"Conversation:\n{convo}\n\nLatest question: {question}",
    )
    return rewritten or question


def answer_question(question: str, docs: Sequence[Document]) -> str:
    if not docs:
        return NOT_FOUND
    return _invoke(
        ANSWER_SYSTEM_PROMPT,
        f"Context:\n{format_context(docs)}\n\nQuestion: {question}",
    )


def _batches(texts: Sequence[str], max_chars: int) -> List[str]:
    batches, current, size = [], [], 0
    for text in texts:
        if current and size + len(text) > max_chars:
            batches.append("\n\n".join(current))
            current, size = [], 0
        current.append(text)
        size += len(text)
    if current:
        batches.append("\n\n".join(current))
    return batches


def summarize(docs: Sequence[Document]) -> str:
    """Map-reduce: summarise batches that fit the context window, then merge them."""
    batches = _batches([d.page_content for d in docs], settings.SUMMARY_BATCH_CHARS)
    partials = [_invoke(MAP_PROMPT, batch) for batch in batches]
    if len(partials) == 1:
        return _invoke(REDUCE_PROMPT, partials[0])
    # Reduce repeatedly in case the partial summaries themselves are too long.
    while len(partials) > 1:
        merged = _batches(partials, settings.SUMMARY_BATCH_CHARS)
        partials = [_invoke(REDUCE_PROMPT, m) for m in merged]
    return partials[0]
