from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import circuit_drawer
import os


def build_circuit(task):
    qc = QuantumCircuit(task["num_qubits"], task["num_qubits"])

    for gate in task["gates"]:
        gtype = gate["type"]

        if gtype == "H":
            qc.h(gate["targets"][0])

        elif gtype == "CX":
            qc.cx(gate["controls"][0], gate["targets"][0])

        elif gtype == "MEASURE":
            for q in gate["targets"]:
                qc.measure(q, q)

    return qc


def visualize_circuit(qc, save_path="outputs/circuit.png"):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    circuit_drawer(qc, output="mpl", filename=save_path)
    print(f"[INFO] Circuit diagram saved to {save_path}")


def execute_circuit(qc, shots=1024):
    backend = Aer.get_backend("qasm_simulator")
    job = execute(qc, backend=backend, shots=shots)
    result = job.result()
    return result.get_counts()
