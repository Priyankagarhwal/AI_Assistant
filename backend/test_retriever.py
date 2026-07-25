from app.rag.retriever import retrieve

results = retrieve("What is this document about?")

print(f"Found {len(results)} chunks\n")

for doc in results:
    print(doc.page_content[:200])
    print("-" * 50)