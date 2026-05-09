import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_github_token = os.getenv("GITHUB_TOKEN")
_base_url = os.getenv("BASE_URL")

if not _github_token:
    raise ValueError("GITHUB_TOKEN is not set in environment")
if not _base_url:
    raise ValueError("BASE_URL is not set in environment")

_client = OpenAI(
    api_key=_github_token,
    base_url=_base_url,
)

_embedding_model: str = os.getenv("MODEL_NAME", "text-embedding-3-large")
_chat_model: str = os.getenv("CHAT_MODEL", "gpt-4o-mini")


def create_embedding(text: str) -> list[float]:
    response = _client.embeddings.create(model=_embedding_model, input=text)
    return response.data[0].embedding


def generate_llm_response(question: str, relevant_chunks: list[str]) -> str:
    context = "\n\n".join(relevant_chunks)
    system_prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of "
        "retrieved context to answer the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the answer concise."
        f"\n\nContext:\n{context}"
    )
    response = _client.chat.completions.create(
        model=_chat_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content or ""
