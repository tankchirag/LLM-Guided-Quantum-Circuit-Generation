# LLM-Guided Quantum Circuit Generation ⚛️🤖

**Author:** Chirag Tank  
**Project Status:** Phase 2.7 — Multi-candidate generation & self-critique implemented  
**Frameworks / Libraries:** Qiskit, HuggingFace Transformers, Matplotlib, Python 3.10+  

---

## 🚀 Project Overview

This project implements a **hybrid AI–Quantum pipeline** where a **Large Language Model (LLM)** generates quantum circuit plans, and classical code verifies, validates, and benchmarks them. The system simulates circuits, computes metrics, and selects the **best candidate** based on performance heuristics.

This is **research-grade preparation** for real-world quantum computing applications, combining **LLM reasoning**, **multi-candidate evaluation**, and **visual reporting**.

---

## 🎯 Motivation

Quantum programming is challenging:

- Circuits are **abstract and non-intuitive**
- Errors are **hard to detect**
- Hardware constraints are **complex**

LLMs can:

- Generate **structured plans**
- Recognize **patterns and sequences**
- Provide **self-verification and feedback loops**

Classical code ensures:

- **Validity**
- **Correctness**
- **Performance evaluation**

This combination mirrors **industrial AI + Quantum workflows**.

---

## 🏗️ System Architecture

User Task (e.g., "Create Bell State")
↓
LLM Generates
Multi-candidate Plans
↓
Parser & Validator (normalize + check)
↓
Quantum Circuit Builder (Qiskit)
↓
Simulation & Metrics Computation
↓
Candidate Scoring & Best Selection
↓
Circuit + Histogram Visualizations
↓
Outputs JSON & Images


---

## ⚡ Features Implemented

### Phase 1 — Engineering Quality ✅

- Circuit visualization (PNG)
- Gate count, depth, CX count metrics
- JSON output for reproducibility

### Phase 2 — AI Reasoning ✅

- **LLM self-critique loop**: only validated plans accepted
- Gate-token output for **higher reliability**
- Multi-candidate generation & scoring
- Candidate ranking and **best plan selection**
- Measurement histograms for each candidate
- Full **JSON output including all candidates and metrics**

---

## 📂 Folder Structure

LLM-Guided-Quantum-Circuit-Generation/
│
├── experiments/
│ └── run_experiment.py # Main experiment pipeline
│
├── src/
│ ├── llm.py # LLM interface & candidate generation
│ ├── validator.py # Plan normalization & validation
│ ├── builder.py # Circuit construction from plan
│ ├── metrics.py # Depth, gate count, CX count computation
│ └── plots.py # Circuit & histogram visualizations
│
├── outputs/
│ ├── circuit.png # Best candidate visual
│ ├── measurement_histogram.png
│ ├── candidate_0_circuit.png
│ ├── candidate_0_histogram.png
│ └── results.json # Full multi-candidate data
│
├── README.md
└── requirements.txt # Python dependencies


---

## 🧰 Technical Stack

- **Quantum Simulation:** Qiskit (`AerSimulator`)
- **Deep Learning / LLM:** HuggingFace Transformers (`TinyLlama-1.1B-Chat`)
- **Visualization:** Matplotlib for histograms, Qiskit circuit drawer
- **Python:** 3.10+
- **JSON & Logging:** Full candidate data, metrics, and images

---

## 📈 How It Works

1. **Task Input:** Free-form text (e.g., "Create Bell state")  
2. **Candidate Generation:** LLM generates multiple plans using **gate tokens**  
3. **Self-Critique Loop:** Invalid or inconsistent plans are rejected  
4. **Circuit Building:** Validated plan → Qiskit circuit  
5. **Simulation:** AerSimulator runs shots (1024) → counts  
6. **Metrics Computation:** Depth, gate count, CX count  
7. **Scoring & Ranking:** Heuristic selects the best candidate  
8. **Visualization:**  
   - Circuit image (PNG)  
   - Measurement histogram  
9. **JSON Output:** Full candidate metrics, plans, images  

---

## 🖼️ Example Outputs

**Circuit image (best candidate):**  

![Best Circuit](outputs/circuit.png)

**Measurement histogram:**  

![Histogram](outputs/measurement_histogram.png)

**JSON results example:**

```json
{
  "task": "Create a Bell state",
  "best_index": 3,
  "candidates": [
    {
      "plan": {...},
      "metrics": {"depth": 10, "gate_count": 11, "cx_count": 4},
      "counts": {"01": 517, "11": 507},
      "score": 50,
      "circuit_image": "candidate_0_circuit.png",
      "histogram_image": "candidate_0_histogram.png"
    },
    ...
  ]
}
´´´

##⚡ Next Steps (Phase 2.8+)##

Noise-aware simulation: Use realistic hardware noise models

Constraint-guided decoding: Enforce qubit connectivity & depth limits

RL optimization & QASM export: Research-grade agentic quantum compilation

##📌 Notes##

Designed for research-grade reproducibility

Works with multi-candidate LLM output

Fully modular for future integration with real quantum backends

Compatible with Windows / Linux / macOS

##🛠️ How to Run##

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run experiment
python -m experiments.run_experiment
