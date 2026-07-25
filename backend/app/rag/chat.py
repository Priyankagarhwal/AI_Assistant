from langchain_groq import ChatGroq

from app.config.settings import settings

llm = ChatGroq(
    groq_api_key=settings.GROQ_API_KEY,
    model=settings.MODEL_NAME,
    temperature=0,
)


def ask_llm(context: str, question: str):

    if not context.strip():
        return "I couldn't find relevant information in the selected workspace."

    prompt = f"""
You are KnowledgeHub AI.

Answer ONLY using the provided context.

If the answer is not present in the context,
reply exactly:

"I couldn't find that information in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content.strip()