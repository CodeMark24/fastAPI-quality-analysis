import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

output_dir = Path("analysis/charts")
output_dir.mkdir(parents=True, exist_ok=True)

# Chart 1: Full inventory across all releases
df = pd.read_csv("analysis/rq4_full_inventory_results.csv")

plt.figure(figsize=(11, 6))
plt.plot(
    df["release"],
    df["public_bug_free_percent"],
    marker="o",
    label="Public files"
)
plt.plot(
    df["release"],
    df["internal_bug_free_percent"],
    marker="s",
    label="Internal files"
)

plt.title("Bug-Free File Percentage Across FastAPI Releases")
plt.xlabel("FastAPI Release")
plt.ylabel("Bug-Free Files (%)")
plt.ylim(0, 105)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(output_dir / "05_rq4_full_inventory.png", dpi=300)
plt.close()

# Chart 2: Latest release, common 20 files
common = pd.read_csv("analysis/rq4_common_files_latest.csv")

plt.figure(figsize=(7, 5))
plt.bar(
    common["classification"],
    common["bug_free_percent"]
)

plt.title("Bug-Free Percentage of 20 Common Files (FastAPI 0.162.4)")
plt.xlabel("File Classification")
plt.ylabel("Bug-Free Files (%)")
plt.ylim(0, 105)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(output_dir / "06_rq4_common_files.png", dpi=300)
plt.close()

print("RQ4 charts generated successfully.")
print(f"Output directory: {output_dir}")
print("05_rq4_full_inventory.png")
print("06_rq4_common_files.png")
