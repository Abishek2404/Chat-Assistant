SYSTEM_INSTRUCTIONS = """You are a helpful assistant.

Use ONLY the provided context to answer the question.
If the context does not contain enough information, say:
"I could not find enough information in the knowledge base to answer this question."
Keep answers concise and factual.
"""


def build_rag_prompt(context: str, history: str, question: str) -> str:
    return f"""{SYSTEM_INSTRUCTIONS}

Context:
{context}

Conversation History:
{history or "No previous conversation."}

Question:
{question}

Answer:
"""
