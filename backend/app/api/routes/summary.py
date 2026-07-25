from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.retriever import retrieve
from app.rag.chat import ask_llm

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)


class SummaryRequest(BaseModel):
    workspace_id: str


@router.post("/")
def generate_summary(req: SummaryRequest):

    docs = retrieve(
        workspace_id=req.workspace_id,
        query="Summarize the complete document",
        k=100
    )

    if not docs:
        return {
            "summary": "No documents found in this workspace."
        }

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = """
Summarize the following documents.

Provide:

1. Overall Summary
2. Key Points
3. Important Skills (if any)
4. Projects (if any)
5. Important Technologies (if any)

Be concise.
"""

    summary = ask_llm(
        context=context,
        question=prompt
    )

    return {
        "workspace_id": req.workspace_id,
        "summary": summary
    }