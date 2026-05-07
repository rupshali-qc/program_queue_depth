import pandas as pd
import matplotlib.pyplot as plt

# Read CSV files
df1 = pd.read_csv("ibm_fez.csv")
df2 = pd.read_csv("ibm_marrakesh.csv")
df3 = pd.read_csv("ibm_torino.csv")
# df = pd.read_csv("submission_latency.csv", sep="\t")
# df.columns = df.columns.str.strip()

# df = df[["ibm_fez", "ibm_torino", "ibm_marrakesh"]]
# print(df.columns)
# Select ONLY numeric queue_depth column
combined_df = pd.concat(
    [
        pd.to_numeric(df1["queue_depth"], errors="coerce").rename("ibm_fez"),
        pd.to_numeric(df2["queue_depth"], errors="coerce").rename("ibm_marrakesh"),
        pd.to_numeric(df3["queue_depth"], errors="coerce").rename("ibm_torino")
    ],
    axis=1
)

# Drop NaNs (important if conversion failed anywhere)
combined_df = combined_df.dropna()

# Plot
plt.figure(figsize=(8,5))
combined_df.boxplot()
# df.boxplot()

plt.title("Queue Depth Distribution by Backend", fontsize=25)
plt.ylabel("Queue Depth", fontsize=20)
plt.xticks(rotation=0, fontsize=20)
plt.grid(True)
plt.tight_layout()

plt.savefig("new_new_queue.png")
plt.show()