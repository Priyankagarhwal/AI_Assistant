"""Measure retrieval quality on a hand-labelled question set.

Run from backend/ (after uploading the PDFs referenced in the file):

    python -m eval.eval_retrieval eval/questions.example.json

Each item says which file + page actually contains the answer. A question counts as a
hit if any of the top-k retrieved chunks comes from that page. Reports Hit@k and MRR,
plus how often unanswerable questions are correctly rejected by the relevance threshold.
No LLM calls are made, so this is free to run.
"""

import json
import sys

from app.config.settings import settings
from app.rag.retriever import retrieve


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)

    workspace_id = cfg["workspace_id"]
    k = cfg.get("k", settings.RETRIEVAL_K)
    answerable = [q for q in cfg["questions"] if q.get("page") is not None]
    unanswerable = [q for q in cfg["questions"] if q.get("page") is None]

    hits, rr = 0, 0.0
    for q in answerable:
        results = retrieve(workspace_id, q["question"], k=k)
        rank = next(
            (
                i
                for i, (doc, _) in enumerate(results, start=1)
                if doc.metadata.get("filename") == q["filename"]
                and doc.metadata.get("page") == q["page"]
            ),
            None,
        )
        if rank:
            hits += 1
            rr += 1 / rank
        print(f"{'HIT ' if rank else 'MISS'} rank={rank}  {q['question']}")

    rejected = 0
    for q in unanswerable:
        ok = not retrieve(workspace_id, q["question"], k=k)
        rejected += ok
        print(f"{'REJECTED' if ok else 'LEAKED  '}  {q['question']}")

    if answerable:
        print(f"\nHit@{k}: {hits / len(answerable):.1%}   MRR: {rr / len(answerable):.3f}"
              f"   (n={len(answerable)})")
    if unanswerable:
        print(f"Unanswerable correctly rejected: {rejected}/{len(unanswerable)}"
              f"  (MIN_RELEVANCE_SCORE={settings.MIN_RELEVANCE_SCORE})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "eval/questions.example.json")
