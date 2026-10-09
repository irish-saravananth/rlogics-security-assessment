# DevSecOps Pipeline Security Gates

## Pipeline stages

1. Source checkout
2. Unit tests
3. Semgrep SAST scan
4. Dependency and secret scanning
5. Container image build
6. Trivy image vulnerability and misconfiguration scan
7. SBOM generation using Syft
8. SBOM signing and verification using Cosign
9. Deploy to an isolated test environment
10. DAST using OWASP ZAP against the local test target
11. Publish reports and deployment evidence

## Initial release policy

| Finding or condition | Decision | Reason |
|---|---|---|
| Any CRITICAL vulnerability finding | BLOCK by default | Validate findings; document and approve any exception |
| High vulnerability with a fix available | BLOCK by default | Remediate or approve a documented exception |
| Medium vulnerability | WARN or BLOCK based on context | Assess exploitability and exposure |
| Low vulnerability | WARN and track | Remediate through normal prioritization |
| Confirmed secret exposure | BLOCK | Remove and rotate the secret |
| SAST finding confirmed as exploitable | BLOCK | Fix before release |
| Missing SBOM | BLOCK | Required supply-chain evidence |
| Invalid artifact signature | BLOCK | Artifact integrity cannot be established |
| DAST finding confirmed as critical | BLOCK | Remediate before release |
| False positive | EXCEPTION with evidence | Require owner, rationale, and expiry |

## Exception requirements

Every exception must record:
- Finding identifier and affected component
- Business and technical justification
- Risk owner and approver
- Compensating controls
- Expiration date
- Remediation ticket

Exceptions must be time-limited and reviewed before expiry.

## Evidence from this assessment

- Semgrep before/after reports
- Trivy dependency manifest scan
- Trivy container image scan
- CycloneDX and SPDX SBOMs
- Cosign SBOM signature bundle
- Successful local signature verification

## Current limitations

- The container scan reports a large number of OS package findings.
- Findings require validation and prioritization; counts alone do not establish exploitability.
- The signing exercise skipped transparency-log verification.
- The sample application is a lab artifact, not a production service.
