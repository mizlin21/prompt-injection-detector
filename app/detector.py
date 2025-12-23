from .normalize import normalize
from .rules import run_rules
from .schema import ScanResult

SEVERITY_WEIGHT = {"low": 10, "medium": 25, "high": 45}


def score(findings) -> float:
    """
    Explainable baseline risk score (0-100).
    Later we can add source-aware weighting + profiles (strict/balanced/permissive).
    """
    total = 0.0
    for f in findings:
        total += SEVERITY_WEIGHT.get(f.severity, 10) * f.confidence
    return min(100.0, round(total, 2))


def detect(text: str, source: str = "user") -> ScanResult:
    raw_len = len(text)
    norm = normalize(text)

    findings = run_rules(norm)
    risk = score(findings)

    return ScanResult(
        is_injection=(risk >= 50.0),
        risk_score=risk,
        findings=findings,
        meta={
            "source": source,  # user | retrieved_doc | tool_output
            "raw_length": raw_len,
            "normalized_length": len(norm),
            "version": "0.1.0",
        },
    )
