import json
from qiskit_aer import AerSimulator
from qiskit import transpile

from src.llm import generate_candidates
from src.validator import normalize_plan
from src.builder import build_circuit
from src.metrics import compute_metrics
from src.visualization import save_circuit_image, save_histogram

TASK = "Create a Bell state"
NUM_QUBITS = 2
NUM_CANDIDATES = 5


def score(m):
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
    raw = generate_candidates(TASK, NUM_QUBITS, NUM_CANDIDATES)

    best_plan = None
    best_metrics = None
    best_counts = None
    best_score = float("inf")

    for plan in raw:
        plan = normalize_plan(plan, NUM_QUBITS)
        if plan is None:
            continue

        qc = build_circuit(plan)
        tqc = transpile(qc, simulator)
        result = simulator.run(tqc, shots=1024).result()

        counts = result.get_counts()
        metrics = compute_metrics(tqc)
        s = score(metrics)

        if s < best_score:
            best_score = s
            best_plan = plan
            best_metrics = metrics
            best_counts = counts
            best_circuit = qc

    if best_plan is None:
        print("⚠ LLM failed — using fallback circuit")
        best_plan = fallback_plan()
        best_circuit = build_circuit(best_plan)
        tqc = transpile(best_circuit, simulator)
        result = simulator.run(tqc, shots=1024).result()
        best_counts = result.get_counts()
        best_metrics = compute_metrics(tqc)

    save_circuit_image(best_circuit, "outputs/circuit.png")
    save_histogram(best_counts, "outputs/measurement_histogram.png")

    with open("outputs/results.json", "w") as f:
        json.dump({
            "task": TASK,
            "plan": best_plan,
            "metrics": best_metrics,
            "counts": best_counts
        }, f, indent=2)

    print("✔ Experiment completed successfully")


if __name__ == "__main__":
    main()
