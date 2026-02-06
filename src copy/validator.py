# src/validator.py

class ValidationError(Exception):
    pass


SUPPORTED_GATES = {"H", "X", "Y", "Z", "CX", "MEASURE"}


def validate_task(task: dict):
    if "num_qubits" not in task or "gates" not in task:
        raise ValidationError("Task must contain 'num_qubits' and 'gates'.")

    if not isinstance(task["num_qubits"], int) or task["num_qubits"] <= 0:
        raise ValidationError("'num_qubits' must be a positive integer.")

    for i, gate in enumerate(task["gates"]):
        if "type" not in gate:
            raise ValidationError(f"Gate {i}: missing 'type'")

        if gate["type"] not in SUPPORTED_GATES:
            raise ValidationError(f"Unsupported gate type: {gate['type']}")

        if "targets" not in gate:
            raise ValidationError(f"Gate {i}: missing 'targets'")
