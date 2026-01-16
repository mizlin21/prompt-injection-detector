# Prompt Injection Detector (PID)
![CI](https://github.com/mizlin21/prompt-injection-detector/actions/workflows/ci.yml/badge.svg)

A **rules-based, RAG-aware prompt injection detector** that scans user input and retrieved documents **before they enter an LLM context**.

PID produces **auditable, explainable findings** (rule ID, severity, confidence, spans) and supports **tunable detection profiles** to balance false positives vs recall.

---

## Why this matters
Prompt injection is one of the most common failure modes in LLM applications — especially when using **retrieval-augmented generation (RAG)** or tools.

PID is designed as a **guardrail layer** that can run:
- before model inference
- inside API gateways
- inside RAG pipelines
- in CI for safety testing

--- 

## Motivation

Modern LLM applications increasingly rely on retrieval-augmented generation (RAG) and tool execution.
While powerful, these patterns introduce new attack surfaces where untrusted content can influence
model behavior through prompt injection.

This project explores how prompt injection can be detected *before model execution*, using
transparent, auditable rules rather than opaque black-box filtering.

The goal is not to claim perfect detection, but to demonstrate how security engineers can reason
about risk, tradeoffs, and evaluation when building guardrails for AI systems.

---

## Key features
- **Profiles:** `strict`, `balanced`, `permissive`
- **Source-aware scoring:** higher sensitivity for `retrieved_doc` and tool output
- **RAG scanning:** chunk-level analysis with overlap + document-level aggregation
- **Explainable output:** rule ID, severity, confidence, and span-level metadata
- **Evaluation:** labeled corpus with precision / recall / F1
- **CI:** GitHub Actions automatically runs tests
- **Attack intent taxonomy:** detections map to categories (see `docs/ATTACK_TAXONOMY.md`)
- **Intent-aware scoring:** findings are classified by attack intent (e.g., instruction override, secret exfiltration) and weighted accordingly (see `docs/EVIDENCE.md`)

---

## High-level architecture
```text
User Input / Retrieved Documents
          |
          v
+----------------------+
| Prompt Injection     |
| Detector (PID)       |
+----------------------+
          |
          v
Risk Score + Findings
          |
          v
Allow / Block / Review
```

## Quickstart

Install dependencies:
```bash
pip install -r requirements.txt
```

## Run tests:
```bash
pytest -q
```

## Scan a single input
```bash
python -m app.cli scan data/attacks/injection_01.txt --source user --profile balanced
```

### Example of output
```json
{
  "is_injection": true,
  "risk_score": 98.55,
  "findings": [
    {
      "rule_id": "PI-001",
      "severity": "high",
      "confidence": 0.85
      "attack_type": "instruction_override"
    }
  ]
}
```

## RAG scanning (retrieved documents)
Scan retrieved documents before they are injected into an LLM context:
```bash
python -m app.cli rag data/rag_bundle.json --profile strict
```

### Scanner behavior:

- splits documents into overlapping chunks
- analyzes each chunk independently
- aggregates document-level risk
- flags only high-confidence injections

---

## Evaluation
```bash
python -m app.evaluate
```

### Results (strict, retrieved_doc)

- Precision: 1.0
- Recall: 0.8
- F1: 0.889
- Accuracy: 0.9

See docs/EVALUATION.md for:
- false positive / false negative analysis
- tradeoffs and tuning rationale

These metrics are intentionally measured on a small, transparent dataset to
demonstrate evaluation methodology rather than claim production-level coverage.
The goal is explainability, reproducibility, and safe iteration.

---

## Design notes (non-toy decisions)

- Optimized for low false positives in RAG pipelines
- Source-aware weighting reflects real deployment risk
- Chunk overlap prevents boundary-based bypass
- Rules are explicit and auditable (SOC-friendly)
- Evaluation is part of the development loop
- Detection (rules), intent classification, and risk scoring are deliberately separated to support auditability and safe iteration

---

## Repository structure
```text
app/                Core detector, CLI, RAG scanner
tests/              Pytest test suite
data/               Example inputs + evaluation corpus
docs/               Evaluation notes and design docs
.github/workflows/   CI pipeline
```

## Roadmap

- Expand evaluation corpus
- Add authority-coercion weighting
- Add obfuscation handling
- Optional ML-assisted scoring layer
- Multilingual prompt injection detection

---

## License 
MIT

