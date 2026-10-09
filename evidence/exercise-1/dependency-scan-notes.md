# Dependency Vulnerability Scan

## Tool
Trivy filesystem scanner

## Target
devsecops/container-scan/requirements.txt

## Detected result
- Total vulnerabilities: 12
- High: 3
- Medium: 7
- Low: 2
- Critical: 0
- Unknown: 0

## Dependencies
- Flask 2.0.0
- Werkzeug 2.0.0

## Interpretation
These deliberately outdated dependency versions are used only to
demonstrate software composition analysis. The reported findings
must be triaged against the affected component, vulnerability details,
fixed versions, and application exposure.

## Remediation
Upgrade to compatible, supported dependency versions, rerun the scan,
and verify application tests. Do not suppress findings solely to make
the pipeline pass.

## Limitations
The result reflects the Trivy vulnerability database and scan time.
It is not proof that the entire application or its container is secure.
