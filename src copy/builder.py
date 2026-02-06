# src/builder.py

from qiskit import QuantumCircuit


def build_circuit(task: dict) -> QuantumCircuit:
    qc = QuantumCircuit(task["num_qubits"], task["num_qubits"])

    for gate in task["gates"]:
        t = gate["type"]

        if t == "H":
            qc.h(gate["targets"][0])

        elif t == "X":
            qc.x(gate["targets"][0])

        elif t == "Y":
            qc.y(gate["targets"][0])

        elif t == "Z":
            qc.z(gate["targets"][0])

        elif t == "CX":
            qc.cx(gate["controls"][0], gate["targets"][0])

        elif t == "MEASURE":
            for q in gate["targets"]:
                qc.measure(q, q)

    return qc
