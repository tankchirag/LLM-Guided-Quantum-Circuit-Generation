# experiments/run_experiment.py

import json
from pathlib import Path
from datetime import datetime

from qiskit_aer import AerSimulator
from qiskit import transpile
import matplotlib.pyplot as plt

from src.llm import generate_task
from src.validator import validate_task, ValidationError
from src.builder import build_circuit
from src.metrics import circuit_metrics, normalize_counts
from src.plots import plot_measurements


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

MAX_RETRIES = 2


def main():
    prompt = "Create a Bell state circuit"

    feedback = None
    task = None

    for attempt in range(MAX_RETRIES + 1):
        task = generate_task(prompt, feedback)

        try:
            validate_task(task)
            break
        except ValidationError as e:
            feedback = f"Validation error: {str(e)}"
    else:
        raise RuntimeError("LLM failed to generate valid circuit")

    qc = build_circuit(task)

    # Circuit visualization
    fig = qc.draw("mpl")
    fig.savefig(OUTPUT_DIR / "circuit.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=1024).result()

    counts = result.get_counts()
    metrics = circuit_metrics(qc)

    # Measurement histogram
    plot_measurements(counts, OUTPUT_DIR / "measurement_histogram.png")

    output = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "task": task,
        "metrics": metrics,
        "counts": counts,
        "probabilities": normalize_counts(counts),
        "artifacts": {
            "circuit_image": "outputs/circuit.png",
            "measurement_histogram": "outputs/measurement_histogram.png"
        }
    }

    with open(OUTPUT_DIR / "results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("✔ Circuit, metrics, and measurement histogram generated")


if __name__ == "__main__":
    main()
