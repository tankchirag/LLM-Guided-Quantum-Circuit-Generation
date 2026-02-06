from src.llm import generate_task_from_prompt
from src.validator import validate_task, ValidationError
from src.builder import build_circuit, visualize_circuit, simulate_circuit

def main():
    prompt = "Create a 2-qubit Bell state circuit with measurement"
    try:
        task = generate_task_from_prompt(prompt)
        print("Generated task:", task)
        validate_task(task)
        qc = build_circuit(task)
        visualize_circuit(qc)
        simulate_circuit(qc)
    except ValidationError as ve:
        print("Validation Error:", ve)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
