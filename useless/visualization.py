import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


def save_circuit_image(qc, path):
    qc.draw("mpl").savefig(path)


def save_histogram(counts, path):
    plot_histogram(counts)
    plt.savefig(path)
