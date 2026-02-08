from qiskit import QuantumCircuit


def build_circuit(plan: dict) -> QuantumCircuit:
    qc = QuantumCircuit(plan["qubits"], plan["qubits"])

    for g in plan["gates"]:
        if g["type"] == "H":
            qc.h(g["target"])
        elif g["type"] == "CX":
            qc.cx(g["control"], g["target"])

    qc.measure(range(plan["qubits"]), range(plan["qubits"]))
    return qc
