cat > README.md <<'EOF'
# FastAPI Code Quality Evolution Analysis

An empirical study of the evolution of code quality in the FastAPI Python framework across ten releases using SonarQube.

## 1. Research Overview

This study investigates how FastAPI's code quality evolved across ten selected releases. Static code analysis was performed using SonarQube, focusing on reliability, security, maintainability, public API quality, and the accuracy of detected bugs.

The study uses a consistent analysis configuration across all selected releases.

## 2. Releases Analysed

The following FastAPI releases were examined:

- 0.1.11
- 0.20.1
- 0.50.0
- 0.71.0
- 0.97.0
- 0.114.2
- 0.123.1
- 0.135.1
- 0.143.1
- 0.162.4

Original project: https://github.com/fastapi/fastapi

## 3. Research Questions

The study addresses five research questions:

- RQ1 – Reliability: How did detected bugs and reliability-related indicators change across releases?
- RQ2 – Security: What security vulnerabilities and security hotspots were identified?
- RQ3 – Maintainability: How did code smells, technical debt, and code duplication evolve?
- RQ4 – Public vs Internal Code: How does code quality differ between documented public API files and internal implementation files?
- RQ5 – Detection Accuracy: How accurate were SonarQube's bug reports when manually inspected?

## 4. Methodology

Static analysis was conducted using:

- SonarQube Community Build 26.11.0.134175
- SonarScanner CLI 8.3.1.16491
- Sonar way quality profile
- Standard Experience
- Python analysis version 3.11

The analysis targeted the `fastapi` production package.

The same general analysis scope and quality profile were maintained across all ten releases. SonarQube metrics, issues, technical debt, security hotspots, and file-level information were exported for further analysis.

Public and internal files were classified using the official FastAPI API reference documentation.

Manual inspection was used to assess selected bug reports from the latest analysed release.

Further methodological decisions and limitations are documented in:

`documentation/methodology_and_decisions.txt`

## 5. Preliminary Findings

The analysis produced the following observations:

- The analysed codebase increased from 2,333 NCLOC in version 0.1.11 to 19,864 NCLOC in version 0.162.4.
- Detected bugs increased from 2 in the earliest release to 3 in the latest release.
- No vulnerabilities were reported across the ten analysed releases.
- Code duplication reached 48.3% in version 0.114.2 and was 37.2% in version 0.162.4.
- SonarQube reported a Maintainability Rating of A and Security Rating of A across all releases.
- The latest release had a Reliability Rating of E.
- The latest release had 3 detected bugs, of which 1 was provisionally classified as a true positive and 2 as false positives during preliminary manual inspection.

These are static-analysis observations, not proof that the software is free of defects or security risks. The manual validation sample is small and should not be generalised.

## 6. Repository Structure

```text
.
├── analysis/
│   ├── charts/
│   ├── generate_charts.py
│   ├── rq4_common_files.txt
│   └── rq4_results.csv
├── configuration/
│   └── sonar-project.properties
├── documentation/
│   └── methodology_and_decisions.txt
└── raw_data/
    ├── debt_metrics/
    ├── file_inventory/
    ├── hotspots/
    ├── issues/
    ├── fastapi_quality_results.csv
    ├── issues_all.csv
    └── sonar_metrics.jsonl]
