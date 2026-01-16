# Evidence: Intent-Aware Prompt Injection Detection

This document captures concrete evidence demonstrating how the Prompt Injection Detector (PID)
detects, classifies, and scores prompt injection attempts using **intent-aware risk modeling**.

The goal is to show **observable behavior**, **risk differentiation**, and **auditability** —
not just code claims.

---

## 1. Test Environment

- Detector version: `v0.3.0`
- Profile: `balanced`
- CLI entrypoint: `python -m app.cli`
- Test input: `data/attacks/injection_01.txt`
- Evaluation performed locally and validated via GitHub Actions CI

---

## 2. Intent-Aware Detection (User Input)

### Command
```bash
python -m app.cli scan data/attacks/injection_01.txt --source user --profile balanced
```

### Result
```json
{
  "is_injection": true,
  "risk_score": 98.55,
  "findings": [
    {
      "rule_id": "PI-001",
      "severity": "high",
      "confidence": 0.85,
      "message": "Attempt to override instruction hierarchy (classic injection pattern).",
      "attack_type": "instruction_override"
    }
  ]
}
```
### Interpretation

- The detector correctly identifies an instruction override attempt
- The finding is explicitly classified as instruction_override
- Risk score reflects:
    - Severity (high)
    - Confidence (0.85)
    - Intent-aware weighting
- Output is explainable and auditable, rather than a binary block/allow decision

--- 

## 3. Intent-Aware Detection (Retrieved Document / RAG Context)
### Command
```bash
python -m app.cli scan data/attacks/injection_01.txt --source retrieved_doc --profile balanced
```
### Result
```json
{
  "is_injection": true,
  "risk_score": 100.0,
  "findings": [
    {
      "rule_id": "PI-002",
      "severity": "high",
      "confidence": 0.9,
      "message": "Attempt to exfiltrate hidden/system/developer instructions.",
      "attack_type": "secret_exfiltration"
    }
  ]
}
```

### Interpretation

- Same textual pattern produces higher risk when originating from `retrieved_doc`
- Secret exfiltration is weighted more heavily than instruction override
- Source-aware + intent-aware scoring reflects real-world RAG threat models
- Demonstrates why context matters, not just pattern matching

---

## 4. Risk Differentiation Summary
| Scenario             | Attack Type            | Source        | Risk Score |
| -------------------- | ---------------------- | ------------- | ---------- |
| Instruction override | `instruction_override` | user          | ~98.5      |
| Secret exfiltration  | `secret_exfiltration`  | retrieved_doc | 100.0      |

### This confirms that:
- Not all prompt injections are equal
- Intent classification directly influences risk scoring
- RAG content is treated as higher trust-risk by design

---

## 5. Test Coverage & Regression Protection

### The following safeguards are enforced via automated tests:
- Intent-weighted scoring produces different outcomes for different attack intents
- All rules must declare an `attack_type`
- CI blocks changes that silently bypass intent classification

### Example test:

```python
def test_rules_have_attack_type():
    from app.rules import RULES
    assert all("attack_type" in r for r in RULES)
```

### This prevents silent scoring regressions as the rule set evolves.

---

## 6. CI Validation

### All changes are validated by GitHub Actions:
- Test suite passes on every push
- Intent taxonomy and scoring logic are continuously enforced
- Evidence corresponds to a successful CI run

---

## 7. Why This Matters

### This evidence demonstrates a shift from:
- Pattern detection → security reasoning
- Regex flags → intent-aware risk modeling
- Toy blocking → auditable guardrails
- PID is designed to support safe LLM enablement, not blanket restriction.