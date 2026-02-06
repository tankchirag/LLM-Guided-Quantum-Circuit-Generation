# src/plots.py

import matplotlib.pyplot as plt


def plot_measurements(counts, output_path):
    states = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(6, 4))
    plt.bar(states, values)
    plt.xlabel("Measured State")
    plt.ylabel("Counts")
    plt.title("Measurement Results")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
