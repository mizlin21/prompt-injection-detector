from pathlib import Path
from app.evaluate import compute_metrics


def test_compute_metrics_sanity():
    # rows: (filename, true, pred, score)
    rows = [
        ("a", 1, 1, 90.0),  # TP
        ("b", 0, 0, 0.0),   # TN
        ("c", 0, 1, 60.0),  # FP
        ("d", 1, 0, 10.0),  # FN
    ]
    m = compute_metrics(rows)
    assert m["tp"] == 1.0
    assert m["tn"] == 1.0
    assert m["fp"] == 1.0
    assert m["fn"] == 1.0
