# src/builder.py

from qiskit import QuantumCircuit

def build_circuit(plan: dict) -> QuantumCircuit:
    """
    Build a Qiskit QuantumCircuit from a plan dictionary.
    - Skips invalid CX gates (control == target)
    - Ensures all qubits are measured at least once
    """
    num_qubits = plan.get("qubits", plan.get("num_qubits", 2))
    qc = QuantumCircuit(num_qubits, num_qubits)
    measured_qubits = set()

    for g in plan["gates"]:
        t = g["type"]

        if t in {"H", "X", "Y", "Z"}:
            target = g.get("target") or (g.get("targets")[0] if g.get("targets") else None)
            if target is not None and 0 <= target < num_qubits:
                if t == "H":
                    qc.h(target)
                elif t == "X":
                    qc.x(target)
                elif t == "Y":
                    qc.y(target)
                elif t == "Z":
                    qc.z(target)

        elif t == "CX":
            control = g.get("control")
            target = g.get("target")
            # Skip invalid CX
            if control is not None and target is not None and control != target:
                qc.cx(control, target)

        elif t == "MEASURE":
            targets = g.get("targets") or [0]
            for q in targets:
                if 0 <= q < num_qubits:
                    qc.measure(q, q)
                    measured_qubits.add(q)

    # Ensure all qubits are measured at least once
    for q in range(num_qubits):
        if q not in measured_qubits:
            qc.measure(q, q)

    return qc
