import os

from utils.chroma_db_util import are_documents_ingested, query_documents, upload_documents_to_db
from utils.document_util import get_chunk_ids, get_chunked_documents
from utils.open_ai_util import create_embedding, generate_llm_response


def set_docs_in_chroma(dir_path: str) -> None:
    # Load and chunk all documents from the given directory
    documents = get_chunked_documents(dir_path)

    # Generate and attach an embedding vector to each chunk
    for document in documents:
        document.embedding = create_embedding(document.text)

    # Persist chunks and their embeddings into ChromaDB
    upload_documents_to_db(documents)


def chat() -> None:
    print("=" * 60)
    print("  chunk-chat")
    print("  Ask questions about your documents.")
    print("  Type 'quit' or 'exit' to stop.")
    print("=" * 60)
    print()

    while True:
        # Read user query
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            continue

        if query.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        # Retrieve relevant chunks and generate answer
        relevant_chunks: list[str] = query_documents(query)
        answer: str = generate_llm_response(query, relevant_chunks)

        print(f"\nAssistant: {answer}\n")
        print("-" * 60)
        print()


# Resolve and validate the documents directory from environment
dir_path: str = os.getenv("DIR_PATH") or ""
if not dir_path:
    raise ValueError("DIR_PATH is not set in environment")

# Ingest documents only if they are not already present in ChromaDB
print("Checking document index...")
expected_ids: list[str] = get_chunk_ids(dir_path)
if not are_documents_ingested(expected_ids):
    print("Ingesting documents for the first time...")
    set_docs_in_chroma(dir_path)
    print("Done.\n")

chat()
