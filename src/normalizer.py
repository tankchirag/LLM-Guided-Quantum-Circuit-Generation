GATE_ALIASES = {
    "CNOT": "CX",
    "CONTROLLED_NOT": "CX"
}


def normalize_task(raw: dict):
    """
    Convert LLM output into canonical internal schema.
    """

    if "circuit" in raw:
        raw = raw["circuit"]

    # --- Qubit count ---
    if "num_qubits" in raw:
        num_qubits = raw["num_qubits"]
    elif "qubits" in raw:
        num_qubits = raw["qubits"]
    else:
        raise ValueError("Missing qubit count")

    # --- Gates ---
    gates = []
    for g in raw.get("gates", raw.get("operations", [])):
        gate = {}

        gtype = g.get("type") or g.get("name")
        if gtype in GATE_ALIASES:
            gtype = GATE_ALIASES[gtype]

        gate["type"] = gtype

        if "control" in g:
            gate["controls"] = [g["control"]]
        if "controls" in g:
            gate["controls"] = g["controls"]

        if "target" in g:
            gate["targets"] = [g["target"]]
        if "targets" in g:
            gate["targets"] = g["targets"]

        gates.append(gate)

    return {
        "num_qubits": num_qubits,
        "gates": gates
    }
