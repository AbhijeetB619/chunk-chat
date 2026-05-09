import os

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

from utils.models import Document

load_dotenv()

_embedding_function = OpenAIEmbeddingFunction(
    api_base=os.getenv("BASE_URL"),
    api_key=os.getenv("GITHUB_TOKEN"),
    model_name=os.getenv("MODEL_NAME", "text-embedding-3-large"),
)

_db_path: str = os.getenv("DB_PATH", "./db/open_ai_embeddings_db")
_collection_name: str = os.getenv("COLLECTION_NAME", "articles")

_chroma_client = chromadb.PersistentClient(path=_db_path)

_collection = _chroma_client.get_or_create_collection(
    name=_collection_name,
    embedding_function=_embedding_function,
)


def upload_documents_to_db(documents: list[Document]) -> None:
    for doc in documents:
        print(f"upserting embeddings for doc: {doc.id}")
        _collection.upsert(ids=doc.id, documents=doc.text, embeddings=doc.embedding)


def are_documents_ingested(doc_ids: list[str]) -> bool:
    # Check if every expected chunk ID is already present in the collection
    result = _collection.get(ids=doc_ids)
    return len(result["ids"]) == len(doc_ids)


def query_documents(question: str, n_results: int = 2) -> list[str]:
    results = _collection.query(query_texts=[question], n_results=n_results)
    # Guard against None returned by ChromaDB for missing fields
    return [doc for sublist in (results["documents"] or []) for doc in sublist]
