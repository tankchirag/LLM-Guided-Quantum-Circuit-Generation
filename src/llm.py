from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)


def parse_gate_tokens(text: str, num_qubits: int):
    """
    Parse gate tokens like:
    H 0
    CX 0 1
    """
    gates = []

    for line in text.splitlines():
        parts = line.strip().split()
        if not parts:
            continue

        if parts[0] == "H" and len(parts) == 2:
            q = int(parts[1])
            if q < num_qubits:
                gates.append({"type": "H", "target": q})

        elif parts[0] == "CX" and len(parts) == 3:
            c, t = int(parts[1]), int(parts[2])
            if c < num_qubits and t < num_qubits:
                gates.append({"type": "CX", "control": c, "target": t})

    if not gates:
        return None

    return {
        "qubits": num_qubits,
        "gates": gates
    }


def generate_candidates(task: str, num_qubits: int, num_candidates: int = 3):
    prompt = f"""
You are a quantum circuit planner.

Task: {task}
Number of qubits: {num_qubits}

Rules:
- One gate per line
- Allowed gates: H, CX
- No explanations
- No JSON

Example:
H 0
CX 0 1
"""

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=128,
        do_sample=True,
        temperature=0.7,
        num_return_sequences=num_candidates
    )

    plans = []
    for out in outputs:
        text = tokenizer.decode(out, skip_special_tokens=True)
        plan = parse_gate_tokens(text, num_qubits)
        if plan:
            plans.append(plan)

    return plans
