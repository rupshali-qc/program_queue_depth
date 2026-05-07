
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler, Session
from qiskit import QuantumCircuit, transpile, generate_preset_pass_manager

import time, pandas as pd

your_api_key = "oo3vlJy52o0lZFn4xU5BwViL_saygcTzplRUc98JBTQP"
your_crn = "crn:v1:bluemix:public:quantum-computing:us-east:a/42a5828957c240928a47d1d83e259865:3190d47c-e527-4cb6-aa6f-4a673fd84a62::"

times=[]
QiskitRuntimeService.save_account(
    channel="ibm_cloud",
    token=your_api_key,
    instance="crn:v1:bluemix:public:quantum-computing:us-east:a/42a5828957c240928a47d1d83e259865:3190d47c-e527-4cb6-aa6f-4a673fd84a62::",
    overwrite=True
)
service = QiskitRuntimeService()
backend = service.backend("ibm_torino")  # get the backend object, not string

from qiskit import QuantumCircuit
import random
shots = 1024  # single-shot execution


def random_circuit_fixed_depth_2q(n_qubits, depth, num_two_qubit):
    qc = QuantumCircuit(n_qubits)
    layers = [[] for _ in range(depth)]

    # ---- Step 1: randomly assign 2-qubit gates to layers ----
    for _ in range(num_two_qubit):
        layer = random.randint(0, depth - 1)
        q1, q2 = random.sample(range(n_qubits), 2)
        layers[layer].append(("cx", q1, q2))

    # ---- Step 2: fill remaining slots with 1-qubit gates ----
    one_qubit_gates = ["rx", "ry", "rz"]
    for d in range(depth):
        used_qubits = set()
        # Mark qubits used by 2-qubit gates in this layer
        for gate in layers[d]:
            _, q1, q2 = gate
            used_qubits.add(q1)
            used_qubits.add(q2)
        # Add random 1-qubit gates to unused qubits
        for q in range(n_qubits):
            if q not in used_qubits:
                g = random.choice(one_qubit_gates)
                θ = random.random() * 3.14159
                layers[d].append((g, q, θ))

    # ---- Step 3: Build circuit in order ----
    for d in range(depth):
        for gate in layers[d]:
            if gate[0] == "cx":
                _, q1, q2 = gate
                qc.cx(q1, q2)
            else:
                g, q, θ = gate
                getattr(qc, g)(θ, q)

    return qc

for i in range(5,11):
    for _ in range(50):
# Example usage:
        qc = random_circuit_fixed_depth_2q(
            n_qubits=i,
            depth=10,
            num_two_qubit=15
        )

        qc.measure_all()

        # --- Transpile circuit for backend ---
        qc_transpiled = transpile(qc, backend=backend, optimization_level=3)

        # --- Run via SamplerV2 ---
        sampler = Sampler(mode=backend)

        # print("Submitting transpiled QFT circuit to backend...")
        t0 = time.time()
        job = sampler.run([qc_transpiled], shots=shots)  # wrapped in lis-
        result = job.result()
        t1 = time.time()

        elapsed = t1 - t0
        times.append(elapsed)

        print(f"\n✅ Total elapsed time (submission → result): {elapsed:.2f} seconds")



    import matplotlib.pyplot as plt
    df = pd.DataFrame({"elapsed_time": times})
    df.to_csv(f"runtime_results_{i}.csv", index=False)

    plt.plot(times)
    plt.xlabel("Run index")
    plt.ylabel("Elapsed time (s)")
    plt.title(f"Execution Times for Random Circuits (n={i})")
    plt.savefig(f"time_plot_{i}.png")
    plt.show()


