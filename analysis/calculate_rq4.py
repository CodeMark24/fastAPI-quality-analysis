import json
from pathlib import Path

import pandas as pd

RELEASES = [
    "0.1.11", "0.20.1", "0.50.0", "0.71.0", "0.97.0",
    "0.114.2", "0.123.1", "0.135.1", "0.143.1", "0.162.4"
]

# Load public/internal classification
classification_df = pd.read_csv(
    "analysis/public_internal_classification.csv"
)

classification = dict(
    zip(classification_df["file"], classification_df["classification"])
)

# Load all SonarQube issues
issues = pd.read_csv(
    "raw_data/issues_all.csv",
    encoding="utf-8-sig"
)

issues["release"] = issues["release"].astype(str)
issues["type"] = issues["type"].astype(str).str.upper()

results = []

for release in RELEASES:
    inventory_path = Path(
        f"raw_data/file_inventory/fastapi-{release}-files.json"
    )

    if not inventory_path.exists():
        raise FileNotFoundError(f"Missing inventory: {inventory_path}")

    with inventory_path.open(encoding="utf-8") as file:
        inventory_data = json.load(file)

    # Extract Python file paths from this release
    files = {
        component["path"]
        for component in inventory_data["components"]
        if component.get("qualifier") == "FIL"
        and component.get("path")
    }

    # Every inventory file must have a classification
    unclassified = files - set(classification)

    if unclassified:
        raise ValueError(
            f"{release}: Unclassified files: {sorted(unclassified)}"
        )

    release_issues = issues[issues["release"] == release]

    bug_files = set(
        release_issues.loc[
            release_issues["type"] == "BUG", "file"
        ].dropna()
    )

    vulnerability_files = set(
        release_issues.loc[
            release_issues["type"] == "VULNERABILITY", "file"
        ].dropna()
    )

    # Only count issue-bearing files that belong to this release
    bug_files &= files
    vulnerability_files &= files

    row = {"release": release, "total_files": len(files)}

    for category in ["Public", "Internal"]:
        category_files = {
            path for path in files
            if classification[path] == category
        }

        bug_affected = category_files & bug_files
        vulnerability_affected = category_files & vulnerability_files

        total = len(category_files)

        bug_free = total - len(bug_affected)
        vulnerability_free = total - len(vulnerability_affected)

        prefix = category.lower()

        row[f"{prefix}_files"] = total
        row[f"{prefix}_bug_affected_files"] = len(bug_affected)
        row[f"{prefix}_bug_free_files"] = bug_free
        row[f"{prefix}_bug_free_percent"] = (
            round(bug_free / total * 100, 2) if total else None
        )

        row[f"{prefix}_vulnerability_affected_files"] = len(
            vulnerability_affected
        )
        row[f"{prefix}_vulnerability_free_files"] = vulnerability_free
        row[f"{prefix}_vulnerability_free_percent"] = (
            round(vulnerability_free / total * 100, 2)
            if total else None
        )

    results.append(row)

output = pd.DataFrame(results)

output_path = Path("analysis/rq4_full_inventory_results.csv")
output.to_csv(output_path, index=False)

print("RQ4 full-inventory calculation completed.")
print(f"Releases analysed: {len(output)}")
print(f"Output: {output_path}")

print("\nResults:")
print(output.to_string(index=False))
