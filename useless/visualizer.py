import os
from qiskit.visualization import circuit_drawer


def save_circuit_image(qc, output_path="outputs/circuit.png"):
    """
    Saves a quantum circuit visualization as a PNG image.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    circuit_drawer(
        qc,
        output="mpl",
        filename=output_path
    )

    print(f"[INFO] Circuit diagram saved to {output_path}")
