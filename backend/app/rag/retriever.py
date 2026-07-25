from app.database.chroma_db import get_vector_db


def retrieve(workspace_id: str, query: str, k: int = 4):

    db = get_vector_db()

    return db.similarity_search(
        query,
        k=k,
        filter={
            "workspace_id": workspace_id
        }
    )