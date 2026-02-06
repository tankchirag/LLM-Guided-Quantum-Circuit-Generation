# src/llm.py

from transformers import pipeline
import json

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

generator = pipeline(
    "text-generation",
    model=MODEL_NAME,
    device=-1
)


def _extract_first_json(text: str) -> dict:
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON found")

    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])

    raise ValueError("Incomplete JSON")


def generate_task(prompt: str, feedback: str | None = None) -> dict:
    system_prompt = f"""
You are a quantum circuit planner.

Return ONLY valid JSON.
No explanations.

Schema:
{{
  "num_qubits": 2,
  "gates": [
    {{"type": "H", "targets": [0]}},
    {{"type": "CX", "controls": [0], "targets": [1]}},
    {{"type": "MEASURE", "targets": [0,1]}}
  ]
}}

Task:
{prompt}
"""

    if feedback:
        system_prompt += f"\nFeedback:\n{feedback}\nRevise the circuit."

    output = generator(
        system_prompt,
        max_new_tokens=256,
        do_sample=False
    )[0]["generated_text"]

    return _extract_first_json(output)
