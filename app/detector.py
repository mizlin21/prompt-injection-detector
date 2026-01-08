from __future__ import annotations

from .normalize import normalize
from .rules import run_rules
from .schema import ScanResult, Finding
from .config import PROFILES, ProfileName

INTENT_MULTIPLIERS = {
    # highest risk: attempts to extract secrets/system prompt
    "secret_exfiltration": 1.30,

    # high risk: override instruction hierarchy
    "instruction_override": 1.20,

    # moderate-high: forces actions/tools/commands
    "tool_action_forcing": 1.15,

    # moderate: role/authority coercion (often paired with override)
    "authority_role_coercion": 1.10,

    # RAG poisoning is dangerous, but you already weight retrieved_doc via source.
    # Keep multiplier moderate so source weighting does the heavy lifting.
    "rag_poisoning": 1.15,

    # suspicious but not always blocking on its own
    "obfuscation_evasion": 1.10,
}

def score(
    findings: list[Finding],
    severity_weight: dict[str, float],
    source_multiplier: float,
) -> float:
    total = 0.0

    for f in findings:
        base = severity_weight.get(f.severity, 10) * f.confidence

        # Intent-weighted risk contribution
        intent = getattr(f, "attack_type", None)
        intent_mult = INTENT_MULTIPLIERS.get(intent, 1.0)
        contrib = base * intent_mult

        total += contrib

    # Apply source sensitivity once at the end (user vs retrieved_doc vs tool_output)
    total *= source_multiplier

    return min(100.0, round(total, 2))

def detect(
    text: str,
    source: str = "user",
    profile: ProfileName = "balanced",
) -> ScanResult:
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
            "source": source,
            "profile": prof.name,
            "threshold": prof.threshold,
            "raw_length": raw_len,
            "normalized_length": len(norm),
            "version": "0.3.0",
        },
    )
