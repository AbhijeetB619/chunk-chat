from dataclasses import dataclass
from typing import Optional


@dataclass
class Document:
    id: str
    text: str
    embedding: Optional[list[float]] = None
