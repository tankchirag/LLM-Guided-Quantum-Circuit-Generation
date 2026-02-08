# metrics.py (example)
def compute_metrics(qc):
    return {
        "depth": qc.depth(),
        "gate_count": qc.size(),
        "cx_count": qc.count_ops().get("cx", 0)
    }
