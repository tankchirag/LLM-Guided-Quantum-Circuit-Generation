# src/metrics.py

def circuit_metrics(qc):
    return {
        "depth": qc.depth(),
        "gate_count": qc.size(),
        "cx_count": qc.count_ops().get("cx", 0)
    }


def normalize_counts(counts):
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
