# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the app
uv run main.py
```

## Environment Setup

Copy `.env` and populate the following variables:

| Variable | Purpose |
|---|---|
| `BASE_URL` | Embedding API endpoint (e.g. `https://models.github.ai/inference`) |
| `MODEL_NAME` | Embedding model name (e.g. `text-embedding-3-large`) |
| `GITHUB_TOKEN` | API key for the GitHub Models endpoint (used as `api_key` in the OpenAI client) |

The LLM response generation in `open_ai_util.py` uses `gpt-4o-mini` hardcoded and relies on `GITHUB_TOKEN` as well.

## Architecture

This is a RAG (Retrieval-Augmented Generation) pipeline with three stages:

**1. Ingestion** (`set_docs_in_chroma` in `main.py`) — one-time, commented out after first run:
- `document_util.py` loads `.txt` files from `./data/new_articles/`, chunks them (default 1000 chars, 20-char overlap), and returns `[{id, text}]`
- `open_ai_util.createEmbedding` calls the GitHub Models embedding endpoint for each chunk
- `chroma_db_util.upload_documents_to_db` upserts chunks + embeddings into ChromaDB

**2. Retrieval** (`query_documents` in `chroma_db_util.py`):
- ChromaDB is persisted locally at `./db/open_ai_embeddings_db`
- Collection is named `"articles"` and uses `OpenAIEmbeddingFunction` for query-time embedding
- Returns top-`n_results` (default 2) matching text chunks

**3. Generation** (`generate_llm_response` in `open_ai_util.py`):
- Joins retrieved chunks into a context string and calls `gpt-4o-mini` via the same GitHub Models endpoint
- Prompt instructs the model to answer in 3 sentences max using only the provided context

## Data Flow

```
./data/new_articles/ → document_util → chunked docs
                                          ↓
                               open_ai_util (embeddings)
                                          ↓
                               chroma_db_util (upsert)
                                          ↓
query string → chroma_db_util (query) → relevant chunks
                                          ↓
                               open_ai_util (LLM) → answer
```
