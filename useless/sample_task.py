task = {
    "num_qubits": 2,
    "gates": [
        {"type": "H", "targets": [0]},
        {"type": "CX", "controls": [0], "targets": [1]},
        {"type": "MEASURE", "targets": [0, 1]}
    ]
}
