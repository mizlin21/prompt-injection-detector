from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Literal


Severity = Literal["low", "medium", "high"]


@dataclass
class Finding:
    rule_id: str
    severity: Severity
    confidence: float  # 0.0 - 1.0
    message: str
    spans: Optional[List[Dict[str, int]]] = None  # [{"start": 10, "end": 42}]


@dataclass
class ScanResult:
    is_injection: bool
    risk_score: float  # 0 - 100
    findings: List[Finding]
    meta: Dict[str, Any]
