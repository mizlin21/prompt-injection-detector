from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Chunk:
    index: int
    start: int
    end: int
    text: str


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80) -> List[Chunk]:
    """
    Simple character-based chunker.
    - chunk_size: how big each chunk is
    - overlap: how much to overlap to catch boundary attacks
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be < chunk_size")

    chunks: List[Chunk] = []
    n = len(text)
    start = 0
    idx = 0

    while start < n:
        end = min(n, start + chunk_size)
        chunks.append(Chunk(index=idx, start=start, end=end, text=text[start:end]))
        idx += 1
        start = end - overlap  # overlap
        if start < 0:
            start = 0
        if end == n:
            break

    return chunks
