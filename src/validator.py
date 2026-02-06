# src/validator.py

class ValidationError(Exception):
    pass


SUPPORTED_GATES = {"H", "X", "Y", "Z", "CX", "MEASURE"}


def validate_task(task: dict):
    if "num_qubits" not in task or "gates" not in task:
        raise ValidationError("Missing 'num_qubits' or 'gates'")

    n = task["num_qubits"]

    if not isinstance(n, int) or n <= 0:
        raise ValidationError("'num_qubits' must be positive integer")

    for i, gate in enumerate(task["gates"]):
        t = gate.get("type")

        if t not in SUPPORTED_GATES:
            raise ValidationError(f"Gate {i}: unsupported type {t}")

        targets = gate.get("targets", [])
        if not isinstance(targets, list):
            raise ValidationError(f"Gate {i}: targets must be list")

        if not all(0 <= q < n for q in targets):
            raise ValidationError(f"Gate {i}: target index out of range")

        if t == "CX":
            controls = gate.get("controls", [])
            if len(controls) != 1 or len(targets) != 1:
                raise ValidationError("CX must have 1 control and 1 target")
