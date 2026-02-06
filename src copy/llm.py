# src/llm.py
"""
Local LLM interface with robust JSON extraction.
"""

from transformers import pipeline
import json

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

generator = pipeline(
    "text-generation",
    model=MODEL_NAME,
    device=-1  # CPU
)


def _extract_first_json(text: str) -> dict:
    """
    Extracts the FIRST valid JSON object from a string.
    """
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON object found in LLM output")

    brace_count = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            brace_count += 1
        elif text[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                json_str = text[start:i + 1]
                return json.loads(json_str)

    raise ValueError("Incomplete JSON object")


def generate_task_from_prompt(prompt: str) -> dict:
    system_prompt = f"""
You are a quantum compiler assistant.

Return ONLY valid JSON.
No explanations.
No markdown.

JSON schema:
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

    output = generator(
        system_prompt,
        max_new_tokens=256,
        do_sample=False
    )[0]["generated_text"]

    try:
        task = _extract_first_json(output)
    except Exception as e:
        print("RAW LLM OUTPUT:\n", output)
        raise ValueError("Failed to extract valid JSON from LLM") from e

    return task
