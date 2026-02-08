from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)


def _generate(prompt, max_new_tokens=128):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def parse_gate_tokens(text: str, num_qubits: int):
    gates = []

    for line in text.splitlines():
        parts = line.strip().split()
        if not parts:
            continue

        try:
            if parts[0] == "H" and len(parts) == 2:
                q = int(parts[1])
                if q < num_qubits:
                    gates.append({"type": "H", "target": q})

            elif parts[0] == "CX" and len(parts) == 3:
                c, t = int(parts[1]), int(parts[2])
                if c < num_qubits and t < num_qubits:
                    gates.append({"type": "CX", "control": c, "target": t})
        except ValueError:
            continue

    if not gates:
        return None

    return {"qubits": num_qubits, "gates": gates}


def generate_with_self_critique(task: str, num_qubits: int):
    # Step 1 — Initial generation
    gen_prompt = f"""
You are a quantum circuit planner.

Task: {task}
Qubits: {num_qubits}

Rules:
- One gate per line
- Allowed gates: H, CX
- No explanations

Example:
H 0
CX 0 1
"""
    draft = _generate(gen_prompt)

    # Step 2 — Self-critique
    critique_prompt = f"""
You previously generated this quantum circuit:

{draft}

Check:
- Are all gates valid?
- Are qubit indices within range 0 to {num_qubits - 1}?
- Is the circuit minimal for the task?

If incorrect, output a corrected version.
If correct, repeat the circuit exactly.

Rules:
- One gate per line
- No explanations
"""
    refined = _generate(critique_prompt)

    return parse_gate_tokens(refined, num_qubits)


def generate_candidates(task: str, num_qubits: int, num_candidates: int = 3):
    plans = []
    for _ in range(num_candidates):
        plan = generate_with_self_critique(task, num_qubits)
        if plan:
            plans.append(plan)
    return plans
