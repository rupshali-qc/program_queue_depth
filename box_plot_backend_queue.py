from qiskit_ibm_runtime import QiskitRuntimeService
from datetime import datetime
import pandas as pd
import time
import matplotlib.pyplot as plt

# Initialize the service (make sure you're logged in)
your_api_key = "V_5F6RZPUb9GB37hSH3CQrQpdFX7WpfP2kek91zjo0Ml"
your_crn = "crn:v1:bluemix:public:quantum-computing:us-east:a/5e194ca79679454da57a2ad2d3e49a9d:749f65fa-d77a-44f6-913a-5a77858ae7aa::"


QiskitRuntimeService.save_account(
    channel="ibm_cloud",
    token=your_api_key,
    instance="crn:v1:bluemix:public:quantum-computing:us-east:a/5e194ca79679454da57a2ad2d3e49a9d:749f65fa-d77a-44f6-913a-5a77858ae7aa::",
    overwrite=True
)
service = QiskitRuntimeService()


# ---- Backends to monitor ----
backend_names = ["ibm_fez", "ibm_marrakesh","ibm_torino"]

# ---- Sampling parameters ----
interval_minutes = 60
duration_minutes = 86400   # change as needed
num_samples = int(duration_minutes / interval_minutes)

# ---- Storage dict ----
all_data = {name: [] for name in backend_names}
# ---- Sampling loop ----
for i in range(num_samples):

    print(f"\n=== Sample {i+1}/{num_samples} ===")

    for backend_name in backend_names:

        backend = service.backend(backend_name)

        success = False
        attempts = 0

        while not success and attempts < 3:
            try:
                status = backend.status()
                q = status.pending_jobs

                all_data[backend_name].append(q)

                # write immediately to CSV
                pd.DataFrame([[datetime.now(), q]],
                    columns=["timestamp","queue_depth"]
                ).to_csv(
                    f"{backend_name}.csv",
                    mode="a",
                    header=not (i),
                    index=False
                )

                print(f"{backend_name}: {q}")
                success = True

            except Exception as e:
                attempts += 1
                print(f"{backend_name} retrying...", e)
                time.sleep(30)

        if not success:
            all_data[backend_name].append(float("nan"))

    # ---- wait until next sampling time ----
    if i < num_samples - 1:
        time.sleep(interval_minutes * 60)



# ---- Convert to DataFrame ----
df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in all_data.items()]))

# ---- Boxplot ----
plt.figure(figsize=(8,5))
df.boxplot()

plt.title("Queue Depth Distribution by Backend", fontsize=25)
plt.ylabel("Queue Depth", fontsize=20)
plt.xticks(rotation=0)
plt.grid(True)
plt.tight_layout()

plt.savefig("backend_queue_boxplot.png")
plt.show()
