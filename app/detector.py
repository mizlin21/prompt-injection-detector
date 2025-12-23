from __future__ import annotations

from .normalize import normalize
from .rules import run_rules
from .schema import ScanResult
from .config import PROFILES, ProfileName


def score(findings, severity_weight, source_mult: float) -> float:
    total = 0.0
    for f in findings:
        total += severity_weight.get(f.severity, 10) * f.confidence
    total *= source_mult
    return min(100.0, round(total, 2))


def detect(text: str, source: str = "user", profile: ProfileName = "balanced") -> ScanResult:
    raw_len = len(text)
    norm = normalize(text)

    prof = PROFILES[profile]
    findings = run_rules(norm)

    source_mult = prof.source_multiplier.get(source, 1.0)
    risk = score(findings, prof.severity_weight, source_mult)

    return ScanResult(
        is_injection=(risk >= prof.threshold),
        risk_score=risk,
        findings=findings,
        meta={
            "source": source,  # user | retrieved_doc | tool_output
            "profile": prof.name,
            "threshold": prof.threshold,
            "raw_length": raw_len,
            "normalized_length": len(norm),
            "version": "0.2.0",
        },
    )
