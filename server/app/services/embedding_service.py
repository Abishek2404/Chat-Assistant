import hashlib
import os
import re
from typing import Iterable

from dotenv import load_dotenv
from openai import APIConnectionError, APITimeoutError, AuthenticationError, OpenAI, RateLimitError

load_dotenv()

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "do",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "what",
    "where",
    "with",
    "your",
}


class EmbeddingService:
    def __init__(self) -> None:
        self.provider = os.getenv("EMBEDDING_PROVIDER", "local").lower()
        self.model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        self.api_key = os.getenv("EMBEDDING_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def embed(self, text: str) -> list[float]:
        if self.provider == "openai":
            return self._openai_embed(text)
        return self._local_hash_embed(text)

    def embed_many(self, texts: Iterable[str]) -> list[list[float]]:
        return [self.embed(text) for text in texts]

    def _openai_embed(self, text: str) -> list[float]:
        if not self.client:
            raise RuntimeError("OpenAI embedding API key is missing")

        try:
            response = self.client.embeddings.create(model=self.model, input=text)
        except AuthenticationError as exc:
            raise RuntimeError("Invalid embedding API key") from exc
        except RateLimitError as exc:
            raise RuntimeError("Embedding rate limit or quota exceeded") from exc
        except APITimeoutError as exc:
            raise RuntimeError("Embedding request timeout") from exc
        except APIConnectionError as exc:
            raise RuntimeError("Embedding provider connection error") from exc
        except Exception as exc:
            raise RuntimeError(f"Embedding provider error: {exc}") from exc

        return response.data[0].embedding

    def _local_hash_embed(self, text: str, dimensions: int = 1536) -> list[float]:
        vector = [0.0] * dimensions
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        for token in tokens:
            if token in STOPWORDS:
                continue
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % dimensions
            vector[index] += 1.0
        return vector


embedding_service = EmbeddingService()
