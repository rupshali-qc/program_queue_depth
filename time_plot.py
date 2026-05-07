# import pandas as pd
# import matplotlib.pyplot as plt

# # Load your data
# df = pd.read_csv("submission_latency.csv")

# # Ensure numeric (safe)
# df = df.apply(pd.to_numeric, errors='coerce')

# # Plot all columns
# plt.figure(figsize=(10,6))

# for col in df.columns:
#     plt.plot(df.index, df[col], label=col)

# # Labels and title
# plt.xlabel("Sample Index", fontsize=14)
# plt.ylabel("Value", fontsize=14)
# plt.title("Backend Performance Over Time", fontsize=16)

# plt.legend()
# plt.grid(True)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load your data
df = pd.read_csv("submission_latency.csv")

# Ensure numeric (safe)
df = df.apply(pd.to_numeric, errors='coerce')

# Bar positions
x = np.arange(len(df))

plt.figure(figsize=(12,6))

# Width of each bar
width = 0.25

# Plot bars for each column
for i, col in enumerate(df.columns):
    plt.bar(x + i*width, df[col], width=width, label=col)

# Labels and title
plt.xlabel("Sample Index", fontsize=20)
plt.ylabel("Time(s)", fontsize=20)
plt.title("Latency from submission to output", fontsize=25)

# Adjust x ticks to center
plt.xticks(x + width, x, fontsize=18)
plt.yticks(fontsize=18)

plt.legend(fontsize=12)
plt.grid(axis='y')


plt.savefig("time_plot.png")
plt.show()