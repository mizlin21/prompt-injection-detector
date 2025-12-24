from __future__ import annotations

from typing import Any, Dict, List

from .chunker import chunk_text
from .detector import detect
from .rag_schema import ChunkScan, DocumentScan, RAGScanResult
from .config import ProfileName


def rag_scan(
    documents: List[Dict[str, Any]],
    profile: ProfileName = "strict",
    chunk_size: int = 400,
    overlap: int = 80,
) -> RAGScanResult:
    """
    Scan retrieved documents for prompt injection before they are appended to the LLM context.
    Input docs format:
      [{"doc_id": "doc1", "text": "...", "source": "retrieved_doc"}, ...]
    """
    doc_scans: List[DocumentScan] = []
    global_max = 0.0
    global_injection = False

    for doc in documents:
        doc_id = str(doc.get("doc_id", "unknown"))
        text = str(doc.get("text", ""))
        source = str(doc.get("source", "retrieved_doc"))

        chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

        chunk_scans: List[ChunkScan] = []
        doc_max = 0.0
        doc_injection = False

        for c in chunks:
            r = detect(c.text, source=source, profile=profile)
            doc_max = max(doc_max, r.risk_score)
            doc_injection = doc_injection or r.is_injection

            preview = c.text.strip().replace("\n", " ")
            if len(preview) > 140:
                preview = preview[:140] + "..."

            chunk_scans.append(
                ChunkScan(
                    chunk_index=c.index,
                    start_char=c.start,
                    end_char=c.end,
                    text_preview=preview,
                    result=r,
                )
            )

        global_max = max(global_max, doc_max)
        global_injection = global_injection or doc_injection

        doc_scans.append(
            DocumentScan(
                doc_id=doc_id,
                source=source,
                max_risk_score=doc_max,
                is_injection=doc_injection,
                chunk_scans=chunk_scans,
                meta={
                    "chunk_size": chunk_size,
                    "overlap": overlap,
                    "profile": profile,
                    "text_length": len(text),
                },
            )
        )

    return RAGScanResult(
        is_injection=global_injection,
        max_risk_score=global_max,
        documents=doc_scans,
        meta={
            "profile": profile,
            "documents_scanned": len(documents),
        },
    )
