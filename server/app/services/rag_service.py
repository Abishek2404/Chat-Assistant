from app.prompts.rag_prompt import build_rag_prompt
from app.services.history_service import history_service
from app.services.llm_service import llm_service
from app.services.retrieval_service import retrieval_service

FALLBACK_REPLY = (
    "I could not find enough information in the knowledge base to answer this question."
)


class RAGService:
    def answer(self, session_id: str, message: str) -> dict:
        if not session_id.strip():
            raise ValueError("sessionId field is required")

        retrieved_chunks = retrieval_service.retrieve(message)
        if not retrieved_chunks:
            history_service.add_pair(session_id, message, FALLBACK_REPLY)
            return {
                "reply": FALLBACK_REPLY,
                "tokensUsed": None,
                "retrievedChunks": 0,
            }

        context = "\n\n".join(
            f"Source: {chunk['title']} ({chunk['chunk_id']})\n{chunk['text']}"
            for chunk in retrieved_chunks
        )
        history = history_service.get_formatted_history(session_id)
        prompt = build_rag_prompt(context=context, history=history, question=message)
        reply, tokens_used = llm_service.generate(prompt, context)
        history_service.add_pair(session_id, message, reply)

        return {
            "reply": reply,
            "tokensUsed": tokens_used,
            "retrievedChunks": len(retrieved_chunks),
        }


rag_service = RAGService()
