# Exercise 1 — Remediation Notes

## Environment
- Python: 3.12.3
- Semgrep: 1.180.0
- Trivy: 0.71.2

## Before
Semgrep reported three blocking findings:
1. MD5 used as a password hash.
2. Insecure MD5 algorithm.
3. subprocess execution with shell=True.

## Remediation
- Replaced SQL string construction with a parameterized query.
- Replaced MD5 password hashing with salted scrypt derivation.
- Replaced shell execution with a fixed executable and argument list.

## Validation
- Unit tests: 4 passed.
- Semgrep before: 3 blocking findings.
- Semgrep after: 0 findings.
- Trivy before and after: scans completed, but no language-specific
  dependency files or configuration files were detected.

## Limitations
This is a local training sample, not a production authentication service.
Dependency and container-image vulnerability coverage is addressed
in subsequent pipeline stages.

## Automated Security Gate

- Evaluator: `scripts/security_gate.py`
- Policy: `devsecops/pipeline/security-gates.md`
- Unit tests: 7 gate-specific tests passed; 11 total tests passed in the existing suite.
- Current image decision: `BLOCK`
- Evidence: `security-gate-result.json`
- Reason: The current Trivy image report contains critical findings and high-severity findings with fixes reported as available.
- Interpretation: The gate correctly prevents this image from being treated as ready for release under the configured policy.
- Limitation: Findings require package-level triage; severity and fix availability alone do not establish exploitability.
