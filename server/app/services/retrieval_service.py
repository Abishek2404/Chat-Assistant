import json
from pathlib import Path

from app.services.embedding_service import embedding_service
from app.utils.chunking import chunk_text
from app.utils.logger import get_logger
from app.vectorstore.memory_store import VectorRecord, vector_store

logger = get_logger(__name__)


class RetrievalService:
    def __init__(self, docs_path: Path | None = None) -> None:
        self.docs_path = docs_path or Path(__file__).resolve().parents[2] / "docs.json"
        self.threshold = 0.2
        self.top_k = 3
        self._indexed = False

    def ensure_indexed(self) -> None:
        if self._indexed:
            return

        if not self.docs_path.exists():
            raise RuntimeError(f"Knowledge base not found: {self.docs_path}")

        documents = json.loads(self.docs_path.read_text(encoding="utf-8"))
        for doc_index, document in enumerate(documents):
            title = document.get("title", f"Document {doc_index + 1}")
            content = document.get("content", "")
            source = document.get("source", title)

            for chunk_index, chunk in enumerate(chunk_text(content)):
                embedding = embedding_service.embed(chunk)
                vector_store.add(
                    VectorRecord(
                        title=title,
                        chunk_id=f"{doc_index + 1}-{chunk_index + 1}",
                        source=source,
                        text=chunk,
                        embedding=embedding,
                    )
                )

        self._indexed = True
        logger.info("Indexed %s chunks", len(vector_store.records))

    def retrieve(self, query: str) -> list[dict]:
        self.ensure_indexed()
        query_embedding = embedding_service.embed(query)
        results = vector_store.search(query_embedding, top_k=self.top_k)
        logger.info(
            "Similarity scores: %s",
            [{"chunk_id": item["chunk_id"], "score": round(item["score"], 4)} for item in results],
        )
        return [item for item in results if item["score"] >= self.threshold]


retrieval_service = RetrievalService()
