from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from .schema import ScanResult


@dataclass
class ChunkScan:
    chunk_index: int
    start_char: int
    end_char: int
    text_preview: str
    result: ScanResult


@dataclass
class DocumentScan:
    doc_id: str
    source: str  # e.g., "retrieved_doc"
    max_risk_score: float
    is_injection: bool
    chunk_scans: List[ChunkScan]
    meta: Dict[str, Any]


@dataclass
class RAGScanResult:
    is_injection: bool
    max_risk_score: float
    documents: List[DocumentScan]
    meta: Dict[str, Any]
