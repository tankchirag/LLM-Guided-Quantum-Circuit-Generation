import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


def save_circuit_image(qc, path):
    fig = qc.draw("mpl")
    fig.savefig(path)
    plt.close(fig)


def save_histogram(counts, path):
    fig = plot_histogram(counts)
    fig.savefig(path)
    plt.close(fig)
