import json
from src.validator import validate_task

with open("data/example_tasks/ghz.json") as f:
    task = json.load(f)

validate_task(task)
print("Validation passed")
