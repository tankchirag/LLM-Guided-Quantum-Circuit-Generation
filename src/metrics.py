def compute_metrics(qc):
    return {
        "depth": qc.depth(),
        "gate_count": len(qc.data),
        "cx_count": sum(1 for g in qc.data if g.operation.name == "cx")
    }
