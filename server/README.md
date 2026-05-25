# RAG Chat Assistant Server

FastAPI backend for a simple Retrieval-Augmented Generation chat assistant.

## Setup

```bash
cd server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`.

## API

- `GET /health`
- `POST /api/chat`

Example request:

```json
{
  "sessionId": "abc123",
  "message": "How do I reset my password?"
}
```

## Providers

The default `.env.example` uses:

- `LLM_PROVIDER=mock`
- `EMBEDDING_PROVIDER=local`

This lets the project run without paid API keys. For real OpenAI-backed generation and embeddings, set both providers to `openai` and provide an API key.
