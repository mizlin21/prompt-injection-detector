# Evaluation (Day 2.2)

# Evaluation (Day 2.2)

## Goal
Evaluate PID as a **RAG guardrail** by measuring detection quality on labeled benign vs malicious prompts.

## Setup
- Dataset:
  - `data/eval/benign` (10 benign samples)
  - `data/eval/malicious` (10 prompt injection samples)
- Default evaluation mode:
  - `profile = strict`
  - `source = retrieved_doc`

This reflects a high-risk RAG scenario where false positives must be minimized.

## Metrics
Run:
```bash
python -m app.evaluate

### Results (strict, retrieved_doc)
- Precision: 1.0 (no false positives)
- Recall: 0.8
- F1: 0.889

Two false negatives involved authority-coercion prompts without explicit exfiltration.
This tradeoff was accepted to minimize false positives in RAG contexts.

## Future work: Per-category evaluation
As the labeled corpus grows, results will be reported by attack category (intent taxonomy) to identify weak spots and tuning opportunities.
