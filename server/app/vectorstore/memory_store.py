from dataclasses import dataclass

import numpy as np


@dataclass
class VectorRecord:
    title: str
    chunk_id: str
    source: str
    text: str
    embedding: list[float]


class MemoryVectorStore:
    def __init__(self) -> None:
        self.records: list[VectorRecord] = []

    def add(self, record: VectorRecord) -> None:
        self.records.append(record)

    def search(self, query_embedding: list[float], top_k: int = 3) -> list[dict]:
        if not self.records:
            return []

        query = np.array(query_embedding, dtype=float)
        query_norm = np.linalg.norm(query)
        if query_norm == 0:
            return []

        scored_results = []
        for record in self.records:
            vector = np.array(record.embedding, dtype=float)
            vector_norm = np.linalg.norm(vector)
            if vector_norm == 0:
                score = 0.0
            else:
                score = float(np.dot(query, vector) / (query_norm * vector_norm))

            scored_results.append(
                {
                    "score": score,
                    "title": record.title,
                    "chunk_id": record.chunk_id,
                    "source": record.source,
                    "text": record.text,
                }
            )

        return sorted(scored_results, key=lambda item: item["score"], reverse=True)[
            :top_k
        ]


vector_store = MemoryVectorStore()
