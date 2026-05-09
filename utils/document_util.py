import os

from utils.models import Document


def get_chunked_documents(
    dir_path: str, chunk_size: int = 1000, chunk_overlap: int = 20
) -> list[Document]:
    documents = load_documents_from_dir(dir_path)
    chunked: list[Document] = []
    for doc in documents:
        for idx, chunk in enumerate(split_into_chunks(doc.text, chunk_size, chunk_overlap)):
            chunked.append(Document(id=f"{doc.id}_chunk_{idx}", text=chunk))
    return chunked


def load_documents_from_dir(dir_path: str) -> list[Document]:
    documents: list[Document] = []
    for file in os.listdir(dir_path):
        # Skip non-text files and hidden files
        if not file.endswith(".txt"):
            continue
        with open(os.path.join(dir_path, file), encoding="utf-8") as f:
            documents.append(Document(id=file, text=f.read()))
    return documents


def get_chunk_ids(
    dir_path: str, chunk_size: int = 1000, chunk_overlap: int = 20
) -> list[str]:
    # Return only the IDs of all chunks without loading embeddings
    return [doc.id for doc in get_chunked_documents(dir_path, chunk_size, chunk_overlap)]


def split_into_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 20) -> list[str]:
    chunks: list[str] = []
    start = 0
    # Use < len(text) so the final partial chunk is always included
    while start < len(text):
        chunks.append(text[start : start + chunk_size])
        start += chunk_size - chunk_overlap
    return chunks
