import numpy as np
import qiskit
from qiskit import QuantumCircuit, Aer, transpile, execute
from qiskit.quantum_info import Statevector, partial_trace, Operator
import matplotlib.pyplot as plt

def classical_pca(x):
    """Classical PCA: Computes covariance matrix and eigenvalues"""
    x = np.array(x)
    
    # Center and normalize the data
    x[0] -= np.mean(x[0])
    x[1] -= np.mean(x[1])
    x[0] /= np.linalg.norm(x[0])
    x[1] /= np.linalg.norm(x[1])

    # Compute covariance matrix
    m = np.cov(x)  # Already unbiased
    print("Covariance Matrix:\n", m)

    # Compute classical eigenvalues
    eigvals, _ = np.linalg.eigh(m)
    print(f"Eigenvalues (Classical PCA): {eigvals}")
    return eigvals

def quantum_pca():
    """Quantum PCA using Qiskit & Quantum Phase Estimation (QPE)"""

    # Define the number of qubits
    n_qubits = 3  # 2 for encoding, 1 for phase estimation
    qc = QuantumCircuit(n_qubits, 1)

    # Apply Hadamard gates for superposition
    qc.h(range(n_qubits - 1))

    # Controlled-unitary encoding of covariance matrix (simplified)
    qc.cz(0, 1)  # Entangle qubits
    qc.cx(1, 2)  # Simulate eigenvalue encoding

    # Quantum Phase Estimation (simplified)
    qc.h(range(n_qubits - 1))
    qc.measure(2, 0)  # Measure last qubit

    return qc

# Simulate Quantum PCA
simulator = Aer.get_backend('qasm_simulator')

# Generate a PCA circuit
qc_pca = quantum_pca()
qc_pca.draw('mpl')

# Transpile and execute
transpiled_circuit = transpile(qc_pca, simulator)
result = execute(transpiled_circuit, simulator, shots=1024).result()
counts = result.get_counts()

# Display the measurement results
print("Quantum PCA Results:", counts)
plot_histogram(counts)
plt.show()


