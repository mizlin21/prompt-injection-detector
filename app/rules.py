import re
from typing import List, Dict, Any

from .schema import Finding


# Baseline rules (v0.1). Expand later with obfuscation + multilingual patterns.
RULES: List[Dict[str, Any]] = [
    {
        "id": "PI-001",
        "severity": "high",
        "pattern": r"(ignore|disregard|override)\s+(all|previous|prior)\s+(instructions|rules)",
        "message": "Attempt to override instruction hierarchy (classic injection pattern).",
        "confidence": 0.85,
    },
    {
        "id": "PI-002",
        "severity": "high",
        "pattern": r"(reveal|show|print)\s+(the\s+)?(system prompt|hidden instructions|developer message)",
        "message": "Attempt to exfiltrate hidden/system/developer instructions.",
        "confidence": 0.90,
    },
    {
        "id": "PI-003",
        "severity": "medium",
        "pattern": r"(you are now|act as)\s+(an?|the)\s+(admin|root|developer|system)",
        "message": "Role escalation / authority impersonation attempt.",
        "confidence": 0.70,
    },
    {
        "id": "PI-004",
        "severity": "medium",
        "pattern": r"(do not|never)\s+(follow|obey)\s+(the|any)\s+(above|previous)\s+(instructions|rules)",
        "message": "Direct instruction to refuse higher-priority constraints.",
        "confidence": 0.75,
    },
]


def run_rules(text: str) -> List[Finding]:
    findings: List[Finding] = []

    for rule in RULES:
        m = re.search(rule["pattern"], text)
        if not m:
            continue

        findings.append(
            Finding(
                rule_id=rule["id"],
                severity=rule["severity"],
                confidence=float(rule["confidence"]),
                message=rule["message"],
                spans=[{"start": m.start(), "end": m.end()}],
            )
        )

    return findings
