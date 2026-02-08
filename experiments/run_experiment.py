import json
from qiskit_aer import AerSimulator
from qiskit import transpile
from src.llm import generate_candidates
from src.validator import normalize_plan
from src.builder import build_circuit
from src.metrics import compute_metrics
from src.visualization import save_circuit_image, save_histogram
import os

TASK = "Create a Bell state"
NUM_QUBITS = 2
NUM_CANDIDATES = 5
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def score(m):
    """Simple heuristic to select best circuit"""
    return m["cx_count"] * 10 + m["depth"]


def fallback_plan():
    return {
        "qubits": 2,
        "gates": [
            {"type": "H", "target": 0},
            {"type": "CX", "control": 0, "target": 1}
        ]
    }


def main():
    simulator = AerSimulator()
    raw_candidates = generate_candidates(TASK, NUM_QUBITS, NUM_CANDIDATES)

    candidate_results = []
    best_score = float("inf")
    best_idx = -1

    for idx, plan in enumerate(raw_candidates):
        plan = normalize_plan(plan, NUM_QUBITS)
        if plan is None:
            continue

        qc = build_circuit(plan)
        tqc = transpile(qc, simulator)
        result = simulator.run(tqc, shots=1024).result()
        counts = result.get_counts()
        metrics = compute_metrics(tqc)
        s = score(metrics)

        # Save per-candidate images
        save_circuit_image(qc, f"{OUTPUT_DIR}/candidate_{idx}_circuit.png")
        save_histogram(counts, f"{OUTPUT_DIR}/candidate_{idx}_histogram.png")

        candidate_results.append({
            "plan": plan,
            "metrics": metrics,
            "counts": counts,
            "score": s,
            "circuit_image": f"candidate_{idx}_circuit.png",
            "histogram_image": f"candidate_{idx}_histogram.png"
        })

        if s < best_score:
            best_score = s
            best_idx = idx

    # Handle fallback if no valid candidate
    if best_idx == -1:
        print("⚠ LLM failed — using fallback circuit")
        plan = fallback_plan()
        qc = build_circuit(plan)
        tqc = transpile(qc, simulator)
        result = simulator.run(tqc, shots=1024).result()
        counts = result.get_counts()
        metrics = compute_metrics(tqc)

        save_circuit_image(qc, f"{OUTPUT_DIR}/best_circuit.png")
        save_histogram(counts, f"{OUTPUT_DIR}/best_histogram.png")

        candidate_results.append({
            "plan": plan,
            "metrics": metrics,
            "counts": counts,
            "score": score(metrics),
            "circuit_image": "best_circuit.png",
            "histogram_image": "best_histogram.png"
        })
        best_idx = 0

    # Save overall JSON with all candidates
    for i, c in enumerate(candidate_results):
        if i == best_idx:
            # Also save main best visuals
            save_circuit_image(build_circuit(c["plan"]), f"{OUTPUT_DIR}/circuit.png")
            save_histogram(c["counts"], f"{OUTPUT_DIR}/measurement_histogram.png")

    with open(f"{OUTPUT_DIR}/results.json", "w") as f:
        json.dump({
            "task": TASK,
            "best_index": best_idx,
            "candidates": candidate_results
        }, f, indent=2)

    print("✔ Experiment completed successfully")
    print(f"Best candidate index: {best_idx}")


if __name__ == "__main__":
    main()
