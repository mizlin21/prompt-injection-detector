from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Tuple

from .detector import detect
from .config import ProfileName


def load_text_files(folder: Path) -> List[Path]:
    return sorted([p for p in folder.glob("*.txt") if p.is_file()])


def evaluate_folder(folder: Path, label: int, source: str, profile: ProfileName) -> List[Tuple[str, int, int, float]]:
    """
    Returns rows: (filename, true_label, pred_label, risk_score)
    label: 1=malicious, 0=benign
    """
    rows = []
    for p in load_text_files(folder):
        text = p.read_text(encoding="utf-8")
        r = detect(text, source=source, profile=profile)
        pred = 1 if r.is_injection else 0
        rows.append((p.name, label, pred, r.risk_score))
    return rows


def compute_metrics(rows: List[Tuple[str, int, int, float]]) -> Dict[str, float]:
    tp = fp = tn = fn = 0
    for _, y, yhat, _ in rows:
        if y == 1 and yhat == 1:
            tp += 1
        elif y == 0 and yhat == 1:
            fp += 1
        elif y == 0 and yhat == 0:
            tn += 1
        elif y == 1 and yhat == 0:
            fn += 1

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) else 0.0

    return {
        "tp": float(tp),
        "fp": float(fp),
        "tn": float(tn),
        "fn": float(fn),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "accuracy": round(accuracy, 3),
    }


def main() -> None:
    base = Path("data/eval")
    benign_dir = base / "benign"
    mal_dir = base / "malicious"

    profile: ProfileName = "strict"
    source = "retrieved_doc"  # evaluation assumes RAG context by default

    benign_rows = evaluate_folder(benign_dir, label=0, source=source, profile=profile)
    mal_rows = evaluate_folder(mal_dir, label=1, source=source, profile=profile)
    rows = benign_rows + mal_rows

    metrics = compute_metrics(rows)

    # Show top false positives / false negatives for tuning
    false_positives = sorted([r for r in rows if r[1] == 0 and r[2] == 1], key=lambda x: -x[3])
    false_negatives = sorted([r for r in rows if r[1] == 1 and r[2] == 0], key=lambda x: x[3])

    print("=== PID Evaluation ===")
    print(f"profile={profile} source={source}")
    print(metrics)

    if false_positives:
        print("\nTop False Positives:")
        for name, y, yhat, score in false_positives[:5]:
            print(f"  {name} score={score}")

    if false_negatives:
        print("\nFalse Negatives:")
        for name, y, yhat, score in false_negatives[:5]:
            print(f"  {name} score={score}")


if __name__ == "__main__":
    main()
