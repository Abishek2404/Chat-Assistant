import os

from dotenv import load_dotenv
from openai import APIConnectionError, APITimeoutError, AuthenticationError, OpenAI, RateLimitError

load_dotenv()


class LLMService:
    def __init__(self) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "mock").lower()
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate(self, prompt: str, context: str) -> tuple[str, int | None]:
        if self.provider == "openai":
            return self._openai_generate(prompt)
        return self._mock_generate(context), None

    def _openai_generate(self, prompt: str) -> tuple[str, int | None]:
        if not self.client:
            raise RuntimeError("OpenAI LLM API key is missing")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                timeout=30,
            )
        except AuthenticationError as exc:
            raise RuntimeError("Invalid LLM API key") from exc
        except RateLimitError as exc:
            raise RuntimeError("LLM rate limit or quota exceeded") from exc
        except APITimeoutError as exc:
            raise RuntimeError("LLM request timeout") from exc
        except APIConnectionError as exc:
            raise RuntimeError("LLM provider connection error") from exc
        except Exception as exc:
            raise RuntimeError(f"LLM provider error: {exc}") from exc

        reply = response.choices[0].message.content or ""
        tokens = response.usage.total_tokens if response.usage else None
        return reply.strip(), tokens

    def _mock_generate(self, context: str) -> str:
        if not context:
            return "I could not find enough information in the knowledge base to answer this question."
        first_context_block = context.split("\n\n")[0]
        lines = first_context_block.splitlines()
        if lines and lines[0].startswith("Source: "):
            lines = lines[1:]
        return "\n".join(lines).strip()


llm_service = LLMService()
