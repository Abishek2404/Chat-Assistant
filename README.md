# GenAI RAG Chat Assistant

This project implements a production-style Retrieval-Augmented Generation chat assistant with a FastAPI backend and a basic HTML/CSS/JavaScript frontend.

## Structure

```text
project/
├── client/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── server/
│   ├── app/
│   ├── docs.json
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
└── README.md
```

## RAG Workflow

1. Load documents from `server/docs.json`.
2. Chunk long document content.
3. Generate embeddings for each chunk.
4. Store chunk vectors and metadata in memory.
5. Embed the user question.
6. Run cosine similarity search.
7. Retrieve the top matching chunks above the threshold.
8. Build a prompt using retrieved context, conversation history, and the question.
9. Call the configured LLM provider.
10. Store the latest conversation messages by `sessionId`.

## Architecture

```text
Browser Client
    |
    v
FastAPI /api/chat
    |
    v
RAG Service
    |
    +--> Embedding Service
    +--> Memory Vector Store
    +--> Retrieval Service
    +--> Prompt Builder
    +--> LLM Service
    +--> History Service
```

## Running Locally

Start the backend:

```bash
cd server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `client/index.html` in a browser.

## Environment

The project can run in mock/local mode without API keys. For real OpenAI calls, update `server/.env`:

```text
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=your_api_key
```