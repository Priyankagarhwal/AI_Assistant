from app.embeddings.embedding_model import get_embedding_model

model = get_embedding_model()

vector = model.embed_query("KnowledgeHub AI")

print(len(vector))
print(vector[:10])