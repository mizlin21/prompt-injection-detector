# Design Decisions & Tradeoffs — Prompt Injection Detector (PID)

This document explains *why* key design decisions were made, what alternatives
were considered, and what tradeoffs were accepted.

The goal is to make PID **auditable, explainable, and maintainable** — not just functional.

---

## 1. Rules-Based Detection (Initial Layer)

### Decision
PID uses explicit, rules-based detection as its first layer instead of a
pure ML classifier.

### Rationale
- Rules are transparent and auditable
- Findings can be explained to humans
- Behavior is deterministic and reproducible
- Easy to test and enforce in CI
- Safer for early-stage guardrails

### Tradeoffs
- Requires manual curation
- Limited coverage for novel phrasing
- Can be bypassed by creative attackers

### Why This Was Acceptable
PID is designed as a **guardrail**, not a complete defense.
Transparency and trust were prioritized over coverage.

This choice also allows security behavior to be reviewed independently of model behavior.

---

## 2. Intent Taxonomy (Security Reasoning Layer)

### Decision
Each rule is mapped to an explicit attack intent (e.g. instruction override,
secret exfiltration, tool hijacking).

### Rationale
- Not all prompt injections are equal
- Risk depends on attacker goal, not just pattern
- Enables intent-aware risk scoring
- Aligns with threat modeling practices

### Tradeoffs
- Requires taxonomy maintenance
- Misclassification risk exists
- Adds design complexity

### Why This Was Acceptable
Intent modeling enables **reasoned security decisions** instead of binary blocking.

---

## 3. Source-Aware Weighting (Context Sensitivity)

### Decision
PID weights findings differently based on source (user vs retrieved_doc vs tool_output).

### Rationale
- RAG introduces higher trust risk
- Retrieved data is harder to audit
- Tool outputs can indirectly carry attacker influence
- Same text is not equally dangerous in all contexts

### Tradeoffs
- Requires correct source labeling
- Incorrect classification can skew risk
- Adds configuration complexity

### Why This Was Acceptable
Context-aware scoring reflects real-world LLM deployment risk models.

---

## 4. Deterministic Scoring (Auditability)

### Decision
PID uses deterministic scoring instead of probabilistic classification.

### Rationale
- Enables audit trails
- Makes behavior predictable
- Simplifies debugging
- Supports CI enforcement
- Reduces operator surprise

### Tradeoffs
- Less adaptive than ML-based scoring
- Requires manual tuning
- Slower to evolve automatically

### Why This Was Acceptable
Guardrails must be **predictable before they are adaptive**.

---

## 5. Small, Transparent Evaluation Set

### Decision
PID uses a small labeled evaluation corpus instead of a large opaque dataset.

### Rationale
- Easy to inspect and audit
- Supports reproducibility
- Encourages understanding failure modes
- Avoids overclaiming performance

### Tradeoffs
- Not statistically representative
- Lower confidence in generalization
- Requires careful interpretation

### Why This Was Acceptable
The goal is **methodology demonstration**, not benchmark competition.

---

## 6. CI Enforcement of Security Invariants

### Decision
Security invariants (e.g. every rule must declare attack_type) are enforced via tests.

### Rationale
- Prevents silent regressions
- Locks in security assumptions
- Makes safety a build-time concern
- Encourages disciplined changes

### Tradeoffs
- Adds friction to development
- Requires test updates when taxonomy evolves

### Why This Was Acceptable
Security regressions are more expensive than developer friction.

---

## 7. Deferred / Future Decisions

Some decisions are intentionally deferred:

- ML-assisted detection layer
- Multilingual attack coverage
- Advanced obfuscation handling
- Semantic intent inference
- Adaptive thresholds

These are deferred to keep the system **understandable, auditable, and safe**.

---

## 8. Design Philosophy

PID favors:
- clarity over cleverness
- reasoning over reaction
- auditability over opacity
- guardrails over blocking
- security enablement over restriction

This philosophy guided every tradeoff above.
