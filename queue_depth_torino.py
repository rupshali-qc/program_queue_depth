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

# Choose a real backend (replace with your desired backend)
backend_name = "ibm_torino"
backend = service.backend(backend_name)

# Sampling parameters
interval_minutes = 10
duration_minutes = 4320 
num_samples = duration_minutes /interval_minutes

# Store data
timestamps = []
queue_depths = []

print(f"Collecting queue depth data for {backend_name}...")

for i in range(int(num_samples)):  # <-- cast here to be safe
    success = False
    attempts = 0
    max_attempts = 3

    # --- Retry logic for network hiccups ---
    while not success and attempts < max_attempts:
        try:
            status = backend.status()
            queue_depth = status.pending_jobs
            timestamps.append(datetime.now())
            queue_depths.append(queue_depth)

            print(f"[{timestamps[-1].strftime('%H:%M:%S')}] Queue depth: {queue_depth}")
            success = True
        except Exception as e:
            attempts += 1
            print(f"⚠️ Attempt {attempts} failed due to: {e}")
            print("Retrying in 30 seconds...")
            time.sleep(30)

    if not success:
        print("❌ Failed after 3 attempts. Logging as NaN.")
        timestamps.append(datetime.now())
        queue_depths.append(float('nan'))

    # Wait for next interval (unless last iteration)
    if i < num_samples - 1:
        print(f"Sleeping for {interval_minutes} minutes... ({i+1}/{num_samples})")
        time.sleep(interval_minutes * 60)

# Create a DataFrame from the collected data
df = pd.DataFrame({
    "timestamp": timestamps,
    "queue_depth": queue_depths
})

df.to_csv("torino_results.csv", index=False)

# Plot
plt.figure(figsize=(10,5))
plt.plot(df["timestamp"], df["queue_depth"], marker="o", linestyle="-")
plt.title(f"Queue Depth for {backend_name}",fontsize=27)
plt.xlabel("Time",fontsize=20)
plt.ylabel("Queue Depth",fontsize=20)
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"queue_depth_{backend_name}.png")
print(f"Plot saved to queue_depth_{backend_name}.png")
plt.show()
