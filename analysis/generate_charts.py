import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the existing SonarQube results
df = pd.read_csv("raw_data/fastapi_quality_results.csv")

# Ensure releases are displayed in chronological order
df["Release"] = df["Release"].astype(str)

# Create an output directory
output_dir = Path("analysis/charts")
output_dir.mkdir(exist_ok=True)

# Shorten release labels for chart readability
labels = df["Release"].apply(lambda x: "v" + x)

# Common chart formatting
plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 10,
    "figure.figsize": (11, 6)
})

# ------------------------------------------------
# CHART 1: Codebase growth (NCLOC)
# ------------------------------------------------
fig, ax = plt.subplots()

ax.plot(
    labels,
    df["NCLOC"],
    marker="o",
    linewidth=2
)

ax.set_title("FastAPI Codebase Growth Across Releases")
ax.set_xlabel("FastAPI Release")
ax.set_ylabel("Non-Comment Lines of Code (NCLOC)")
ax.grid(True, linestyle="--", alpha=0.5)

plt.xticks(rotation=45)
fig.tight_layout()
fig.savefig(output_dir / "01_codebase_growth.png", dpi=300)
plt.close(fig)


# ------------------------------------------------
# CHART 2: Code duplication
# ------------------------------------------------
fig, ax = plt.subplots()

ax.plot(
    labels,
    df["Duplication Density (%)"],
    marker="o",
    linewidth=2
)

ax.set_title("Code Duplication Across FastAPI Releases")
ax.set_xlabel("FastAPI Release")
ax.set_ylabel("Duplicated Lines (%)")
ax.grid(True, linestyle="--", alpha=0.5)

plt.xticks(rotation=45)
fig.tight_layout()
fig.savefig(output_dir / "02_code_duplication.png", dpi=300)
plt.close(fig)


# ------------------------------------------------
# CHART 3: Detected bugs
# ------------------------------------------------
fig, ax = plt.subplots()

ax.bar(
    labels,
    df["Bugs"]
)

ax.set_title("Detected Bugs Across FastAPI Releases")
ax.set_xlabel("FastAPI Release")
ax.set_ylabel("Number of Bugs")
ax.set_ylim(bottom=0)
ax.grid(axis="y", linestyle="--", alpha=0.5)

plt.xticks(rotation=45)
fig.tight_layout()
fig.savefig(output_dir / "03_detected_bugs.png", dpi=300)
plt.close(fig)


# ------------------------------------------------
# CHART 4: Reliability ratings
# ------------------------------------------------
rating_map = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5
}

rating_values = df["Reliability"].map(rating_map)

if rating_values.isna().any():
    raise ValueError("Unexpected or missing reliability rating in CSV.")

fig, ax = plt.subplots()

ax.plot(
    labels,
    rating_values,
    marker="o",
    linewidth=2
)

ax.set_title("Reliability Rating Across FastAPI Releases")
ax.set_xlabel("FastAPI Release")
ax.set_ylabel("Reliability Rating")

ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(["A (Best)", "B", "C", "D", "E (Worst)"])
ax.set_ylim(5.3, 0.7)

ax.grid(True, linestyle="--", alpha=0.5)

plt.xticks(rotation=45)
fig.tight_layout()
fig.savefig(output_dir / "04_reliability_rating.png", dpi=300)
plt.close(fig)


print("\nSuccessfully generated four charts!")
print("Location:", output_dir.resolve())

for chart in sorted(output_dir.glob("*.png")):
    print("-", chart.name)

