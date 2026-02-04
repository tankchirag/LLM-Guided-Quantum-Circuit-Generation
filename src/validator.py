# src/validator.py

from src.schema import SUPPORTED_GATES

class ValidationError(Exception):
    pass


def validate_task(task_json):
    if "num_qubits" not in task_json:
        raise ValidationError("Missing 'num_qubits'")

    if "gates" not in task_json:
        raise ValidationError("Missing 'gates'")

    num_qubits = task_json["num_qubits"]

    if not isinstance(num_qubits, int) or num_qubits <= 0:
        raise ValidationError("num_qubits must be positive integer")

    for i, gate in enumerate(task_json["gates"]):
        if "type" not in gate:
            raise ValidationError(f"Gate {i}: missing type")

        if gate["type"] not in SUPPORTED_GATES:
            raise ValidationError(f"Unsupported gate: {gate['type']}")

        for key in ["target", "control"]:
            if key in gate:
                if not (0 <= gate[key] < num_qubits):
                    raise ValidationError(
                        f"Gate {i}: {key} index out of bounds"
                    )
