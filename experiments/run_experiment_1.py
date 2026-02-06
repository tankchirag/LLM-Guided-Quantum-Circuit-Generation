# experiments/run_experiment.py

from src.llm import generate_task_from_prompt
from src.validator import validate_task
from src.builder import build_circuit
from qiskit_aer import AerSimulator
from qiskit import transpile


def main():
    prompt = "Create a Bell state circuit"

    task = generate_task_from_prompt(prompt)
    print("Generated task:", task)

    validate_task(task)

    qc = build_circuit(task)

    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=1024).result()

    print("Measurement results:", result.get_counts())


if __name__ == "__main__":
    main()
