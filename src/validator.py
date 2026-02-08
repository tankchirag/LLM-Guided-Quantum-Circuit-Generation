def normalize_plan(plan: dict, max_qubits: int):
    if "qubits" not in plan or "gates" not in plan:
        return None

    fixed = []
    for g in plan["gates"]:
        if g["type"] == "H" and g["target"] < max_qubits:
            fixed.append(g)
        elif g["type"] == "CX":
            if g["control"] < max_qubits and g["target"] < max_qubits:
                fixed.append(g)

    if not fixed:
        return None

    plan["gates"] = fixed
    plan["qubits"] = max_qubits
    return plan
