from app.detector import score
from app.schema import Finding


def test_intent_weighting_changes_score():
    severity_weight = {"high": 50, "medium": 30, "low": 10}

    exfil = [
        Finding(
            rule_id="PI-002",
            severity="high",
            confidence=1.0,
            message="exfil",
            attack_type="secret_exfiltration",
            spans=[{"start": 0, "end": 5}],
        )
    ]

    override = [
        Finding(
            rule_id="PI-001",
            severity="high",
            confidence=1.0,
            message="override",
            attack_type="instruction_override",
            spans=[{"start": 0, "end": 5}],
        )
    ]

    exfil_score = score(exfil, severity_weight, source_multiplier=1.0)
    override_score = score(override, severity_weight, source_multiplier=1.0)

    assert exfil_score > override_score
