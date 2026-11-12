import json
from pathlib import Path

import pandas as pd

RELEASES = [
    "0.1.11", "0.20.1", "0.50.0", "0.71.0", "0.97.0",
    "0.114.2", "0.123.1", "0.135.1", "0.143.1", "0.162.4"
]

# Load file classification
classification_df = pd.read_csv(
    "analysis/public_internal_classification.csv"
)
classification = dict(
    zip(classification_df["file"], classification_df["classification"])
)

# Find files present in every release
inventories = []

for release in RELEASES:
    path = Path(f"raw_data/file_inventory/fastapi-{release}-files.json")

    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    files = {
        component["path"]
        for component in data["components"]
        if component.get("qualifier") == "FIL"
    }

    inventories.append(files)

common_files = set.intersection(*inventories)

if len(common_files) != 20:
    raise ValueError(
        f"Expected 20 common files, but found {len(common_files)}"
    )

# Classify common files
public_files = {
    path for path in common_files if classification[path] == "Public"
}
internal_files = {
    path for path in common_files if classification[path] == "Internal"
}

if len(public_files) != 12 or len(internal_files) != 8:
    raise ValueError("Unexpected public/internal split in common files.")

# Get latest-release bug records
issues = pd.read_csv("raw_data/issues_all.csv", encoding="utf-8-sig")
latest_bugs = issues[
    (issues["release"].astype(str) == "0.162.4")
    & (issues["type"].astype(str).str.upper() == "BUG")
]

bug_files = set(latest_bugs["file"].dropna())

results = []

for category, files in [
    ("Public", public_files),
    ("Internal", internal_files)
]:
    affected = files & bug_files
    clean = len(files) - len(affected)

    results.append({
        "release": "0.162.4",
        "classification": category,
        "total_common_files": len(files),
        "bug_affected_files": len(affected),
        "bug_free_files": clean,
        "bug_free_percent": round(clean / len(files) * 100, 2)
    })

output = pd.DataFrame(results)
output.to_csv("analysis/rq4_common_files_latest.csv", index=False)

print("Common-file analysis completed.")
print(f"Common files across all releases: {len(common_files)}")
print(f"Public common files: {len(public_files)}")
print(f"Internal common files: {len(internal_files)}")
print("\nLatest release results:")
print(output.to_string(index=False))
