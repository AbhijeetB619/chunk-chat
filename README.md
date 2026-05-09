# chunk-chat

A local RAG (Retrieval-Augmented Generation) chatbot that lets you have a conversation with your own text documents. Run it in the terminal, ask questions in plain English, and get concise answers grounded in your document collection. Documents are chunked, embedded, and stored in a persistent ChromaDB vector database — ingestion only happens once.

---

## How It Works

```
Documents (txt files)
       │
       ▼
  Chunking (1000 chars, 20 char overlap)
       │
       ▼
  Embedding (text-embedding-3-large via GitHub Models)
       │
       ▼
  ChromaDB (persistent local vector store)
       │
  User query (terminal)
       │
       ▼
  Semantic search (ChromaDB) ──► Relevant chunks ──► LLM (gpt-4o-mini) ──► Answer
       │
       └──► Next question... (loop continues until user types 'quit')
```

Ingestion is skipped automatically on subsequent runs — documents are only embedded and uploaded if their chunk IDs are not already present in ChromaDB.

---

## Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager
- A [GitHub Models](https://github.com/marketplace/models) token with access to `text-embedding-3-large` and `gpt-4o-mini`

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repo-url>
cd chunk-chat
```

### 2. Install uv

If you don't have [uv](https://github.com/astral-sh/uv) installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Get a GitHub Models token

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens) and generate a new token
2. No special scopes are needed — a default token works with GitHub Models

### 5. Configure environment

```bash
cp .env.example .env
```

Open `.env` and set your `GITHUB_TOKEN`. All other values work out of the box:

| Variable          | Description                                              | Default                        |
|-------------------|----------------------------------------------------------|--------------------------------|
| `GITHUB_TOKEN`    | GitHub Models API token                                  | *(required)*                   |
| `BASE_URL`        | Embedding and chat API endpoint                          | GitHub Models inference URL    |
| `MODEL_NAME`      | Embedding model                                          | `text-embedding-3-large`       |
| `CHAT_MODEL`      | Chat completion model                                    | `gpt-4o-mini`                  |
| `DIR_PATH`        | Directory containing `.txt` documents to ingest          | `./data/new_articles`          |
| `DB_PATH`         | Local path where ChromaDB persists its data              | `./db/open_ai_embeddings_db`   |
| `COLLECTION_NAME` | ChromaDB collection name                                 | `articles`                     |

### 6. Add your documents

Place `.txt` files in the directory specified by `DIR_PATH` (default: `./data/new_articles`):

```bash
mkdir -p data/new_articles
cp your-documents/*.txt data/new_articles/
```

---

## Usage

### 7. Run the chatbot

```bash
uv run main.py
```

On **first run**, documents are chunked, embedded, and stored in ChromaDB — this may take a moment depending on the number of files. On **subsequent runs** ingestion is skipped and the chatbot starts immediately.

```
Checking document index...
============================================================
  chunk-chat
  Ask questions about your documents.
  Type 'quit' or 'exit' to stop.
============================================================

You: tell me about ai powered supply chain

---

Assistant: AI-powered supply chain systems use machine learning to...

------------------------------------------------------------

You: quit
Goodbye!
```

---

## Project Structure

```
chunk-chat/
├── main.py                  # Entry point — ingestion check + chat loop
├── utils/
│   ├── models.py            # Document dataclass
│   ├── document_util.py     # File loading, chunking, chunk ID helpers
│   ├── open_ai_util.py      # Embedding and LLM response via OpenAI client
│   └── chroma_db_util.py    # ChromaDB persistence, ingestion check, querying
├── data/
│   └── new_articles/        # Place .txt documents here
├── db/                      # ChromaDB persistent storage (auto-created)
├── pyproject.toml
├── .env.example             # Environment variable template (copy to .env)
└── .env                     # Your local config — not committed
```

---

## Dependencies

| Package          | Purpose                              |
|------------------|--------------------------------------|
| `chromadb`       | Local vector database                |
| `openai`         | Embeddings and chat completions      |
| `python-dotenv`  | Load environment variables from .env |
