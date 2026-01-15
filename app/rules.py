import re
from typing import List, Dict, Any

from .schema import Finding


# Baseline rules (v0.1). Expand later with obfuscation + multilingual patterns.
RULES: List[Dict[str, Any]] = [
    {
        "id": "PI-001",
        "severity": "high",
        "attack_type": "instruction_override",
        "pattern": r"(ignore|disregard|override)\s+(all\s+)?(previous|prior)\s+(instructions|rules)",
        "message": "Attempt to override instruction hierarchy (classic injection pattern).",
        "confidence": 0.85,
    },
    {
        "id": "PI-002",
        "severity": "high",
        "attack_type": "secret_exfiltration",
        "pattern": r"(reveal|show|print)\s+(the\s+)?(system prompt|hidden instructions|developer message)",
        "message": "Attempt to exfiltrate hidden/system/developer instructions.",
        "confidence": 0.90,
    },
    {
        "id": "PI-003",
        "severity": "medium",
        "attack_type": "authority_role_coercion",
        "pattern": r"(you are now|act as)\s+(an?|the)\s+(admin|root|developer|system)",
        "message": "Role escalation / authority impersonation attempt.",
        "confidence": 0.70,
    },
    {
        "id": "PI-004",
        "severity": "medium",
        "attack_type": "instruction_override",
        "pattern": r"(do not|never)\s+(follow|obey)\s+(the|any)\s+(above|previous)\s+(instructions|rules)",
        "message": "Direct instruction to refuse higher-priority constraints.",
        "confidence": 0.75,
    },
    {
        "id": "PI-005",
        "severity": "high",
        "attack_type": "tool_action_forcing",
        "pattern": r"(call|use|invoke)\s+(the\s+)?(tool|api|function)|execute\s+(a\s+)?(command|request)",
        "message": "Potential tool/API invocation attempt (risk of agent/tool hijack).",
        "confidence": 0.70,
    },
    {
        "id": "PI-006",
        "severity": "high",
        "attack_type": "secret_exfiltration",
        "pattern": r"(api key|secret key|access token|password|private key|ssh key)",
        "message": "Potential secret/token exfiltration cue.",
        "confidence": 0.65,
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
                attack_type=rule.get("attack_type"),
                spans=[{"start": m.start(), "end": m.end()}],
            )
        )

    return findings
