from langchain_chroma import Chroma
from app.embeddings.embedding_model import get_embedding_model

DB_PATH = "storage/chroma"

vector_db = Chroma(
    persist_directory=DB_PATH,
    embedding_function=get_embedding_model(),
)


def get_vector_db():
    return vector_db