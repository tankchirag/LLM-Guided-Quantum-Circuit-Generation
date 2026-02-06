import json
import os
import re
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"


def generate_task_from_prompt(prompt: str) -> dict:
    """
    Uses a local open-source LLM to generate a quantum circuit task in JSON.
    """

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto"
    )

    system_prompt = (
        "You are a quantum compiler assistant.\n"
        "Return ONLY valid JSON.\n"
        "Schema:\n"
        "{\n"
        '  "num_qubits": int,\n'
        '  "gates": [\n'
        '    {"type": "H", "targets": [int]},\n'
        '    {"type": "CX", "controls": [int], "targets": [int]},\n'
        '    {"type": "MEASURE", "targets": [int]}\n'
        "  ]\n"
        "}\n"
    )

    full_prompt = system_prompt + "\nUser request:\n" + prompt

    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        do_sample=True
    )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("LLM did not return JSON")

    try:
        return json.loads(match.group())
    except json.JSONDecodeError as e:
        raise ValueError("Failed to parse LLM JSON output") from e
