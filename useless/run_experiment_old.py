import json
from qiskit import Aer, execute
from src.builder import build_circuit
from src.validator import validate_task

def main():
    # Load example JSON
    with open("data/example_tasks/bell_task.json") as f:
        task = json.load(f)

    # Validate JSON
    validate_task(task)

    # Build circuit
    qc = build_circuit(task)
    print(qc.draw())

    # Run simulation
    simulator = Aer.get_backend("qasm_simulator")
    job = execute(qc, simulator, shots=1024)
    result = job.result()
    counts = result.get_counts(qc)
    print("Measurement results:", counts)

if __name__ == "__main__":
    main()
