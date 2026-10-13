# RLogics Security Analyst Engineer — Practical Assessment

**Candidate:** Saravanan T H  
**Role:** Automation Engineer  
**Repository:** [rlogics-security-assessment](https://github.com/irish-saravananth/rlogics-security-assessment)

## 1. Overview

This repository contains practical security engineering work prepared for the RLogics Solutions Security Analyst Engineer Practical Assessment. It demonstrates security automation, vulnerability assessment, secrets lifecycle management, Kubernetes workload hardening, security architecture, safe adversary-emulation planning, and AI application security research.

The implementation prioritizes reproducibility, explicit security decisions, evidence retention, and safe local testing. Research and proposed test plans are distinguished from activities actually executed.

## 2. Assessment deliverables

| Exercise | Deliverable | Location |
|---|---|---|
| 1 | DevSecOps pipeline, vulnerability analysis, remediation examples, SBOMs, and artifact-signing evidence | `devsecops/`, `evidence/exercise-1/` |
| 2 | OpenBao PKI and dynamic database credential lab | `openbao/`, `docs/exercise-2/`, `evidence/exercise-2/` |
| 3 | Python Kubernetes manifest security checker, examples, and tests | `scripts/security_manifest_checker.py`, `docs/exercise-3-manifest-checker.md`, `examples/exercise-3/` |
| 4 | MITRE Caldera research and safe emulation plan | `docs/exercise-4/caldera-research.md` |
| 5 | Hardened Kubernetes workload, NetworkPolicy, Kyverno policy testing, and scan evidence | `examples/exercise-5/`, `docs/exercise-5/`, `evidence/exercise-5/` |
| 6 | Security implementation architecture with a visual diagram | `docs/architecture/RLogics_Security_Implementation_Architecture_v1.docx` |
| 7 | AI security tool comparison and proposed RAG/agent security tests | `docs/exercise-7/` |

## 3. Technology and tools

- **Languages:** Python, Bash
- **Application and containers:** Flask, Docker
- **Security analysis:** Semgrep, Trivy, Syft, Cosign
- **Secrets and PKI:** OpenBao, PostgreSQL
- **Kubernetes security:** Kubernetes manifests, Kyverno, Trivy configuration scanning
- **Testing:** pytest
- **AI security research:** Promptfoo, Microsoft PyRIT, NVIDIA garak
- **Adversary-emulation research:** MITRE Caldera, MITRE ATT&CK

Tool references describe the technologies used or researched; they do not imply every tool was executed in every exercise.

## 4. Local setup

The verified development environment uses Python 3.12.3 and a Python virtual environment. Commands below assume a Linux shell and that the required project dependencies are installed.

Create or activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies required by the scripts and tests if they are not already installed:

```bash
python -m pip install pytest PyYAML
```

Run the automated tests:

```bash
python -m pytest scripts/tests tests -v
```

Run a Python syntax check:

```bash
python -m compileall -q scripts
```

The recorded validation run completed with **15 passing tests**. Rerun the commands above to verify the current checkout.

## 5. Security automation

### 5.1 Trivy security gate

The gate consumes a Trivy JSON vulnerability report and writes a JSON decision:

```bash
python scripts/security_gate.py \
  --report evidence/exercise-1/trivy-dependencies.json \
  --output /tmp/security-gate-result.json
```

Review the resulting decision:

```bash
cat /tmp/security-gate-result.json
```

The gate evaluates findings according to the policy implemented in `scripts/security_gate.py`. A blocking decision is an expected security outcome when the report meets the blocking conditions; it is not a test-suite failure.

### 5.2 Kubernetes manifest checker

Inspect the hardened example:

```bash
python scripts/security_manifest_checker.py \
  examples/exercise-5/hardened-deployment.yaml
```

Check the deliberately unsafe example:

```bash
python scripts/security_manifest_checker.py \
  --fail-on HIGH \
  examples/exercise-3/unsafe-deployment.yaml
```

The checker inspects supported Kubernetes workload manifests for common risks, including privileged execution, root execution, host namespace use, host-path mounts, missing resource controls, and container security-context weaknesses.

Use `--strict` to return a non-zero exit code for findings at any severity. Review the checker documentation for its supported rules and limitations.

## 6. Evidence and interpretation

### Exercise 1

The `evidence/exercise-1/` directory contains Semgrep and Trivy outputs, remediation notes, SBOMs in SPDX and CycloneDX formats, signing metadata, and a security-gate result.

The recorded scans identified findings. Do not interpret the presence of an SBOM or artifact signature as proof that an artifact is vulnerability-free. Review the scan results and gate decision together.

### Exercise 2

The OpenBao lab evidence documents certificate issuance and dynamic database credential validation, including use and subsequent revocation of a short-lived database credential. The design document describes production considerations.

Local lab credentials and private material must remain outside Git.

### Exercises 3 and 5

The manifest checker includes example inputs and automated tests. Exercise 5 includes hardened Kubernetes manifests, a NetworkPolicy, a Kyverno policy, policy-test evidence, and Trivy configuration-scan results.

Scanner findings and policy outcomes are recorded as observed; they should not be represented as proof of complete security.

### Exercise 4

The Caldera deliverable is a research and safe-emulation plan. Live Caldera execution is not claimed.

### Exercise 6

The architecture document describes the intended security control flow and the distinction between scanning, signing, and deployment approval.

### Exercise 7

The AI security deliverables compare open-source tools and propose five security tests for a RAG application with a tool-using agent. These tests are documented as proposed tests; live testing against an AI target is not claimed.

## 7. Safety and secrets handling

- Run security scans only against systems you own or are explicitly authorized to test.
- Keep adversary emulation limited to the documented benign, isolated lab scope.
- Do not commit API keys, passwords, private keys, live credentials, customer data, or sensitive records.
- Keep local OpenBao state and secret material outside the repository.
- Do not use a production or shared Kubernetes cluster for assessment experiments without explicit authorization.
- Treat evidence as potentially sensitive and sanitize it before sharing.

The repository `.gitignore` excludes virtual environments, local environment files, key files, and local OpenBao data. Ignore rules are not a substitute for reviewing tracked files, file contents, and Git history.

## 8. Known limitations and production improvements

This repository is an assessment lab, not a production-ready platform.

- Vulnerability scan findings remain part of the recorded assessment evidence; review the reports before deciding whether a build should be released.
- Local signing demonstrates an artifact-integrity workflow, not a complete production identity, provenance, or transparency architecture.
- OpenBao's local setup requires production changes for authentication, TLS, durable storage, audit logging, high availability, backup, and recovery.
- Kubernetes manifest checks and local Kyverno tests do not establish that equivalent admission controls are deployed to a production cluster.
- Caldera execution and live AI security tests are not claimed by the research-only deliverables.
- DAST evidence must be evaluated separately; do not assume a successful DAST run unless an actual report is present.
- Production adoption would require centrally managed policies, least-privilege identities, controlled exceptions, CI integration, monitoring, and repeatable release assurance.

## 9. Architecture and supporting documentation

The architecture document is available at:

`docs/architecture/RLogics_Security_Implementation_Architecture_v1.docx`

Additional design notes and evidence are organized under `docs/` and `evidence/`. The separate candidate response template should accompany the repository link and architecture document when submitting the assessment.

## 10. Repository

GitHub: https://github.com/irish-saravananth/rlogics-security-assessment

Share repository access with the assessment team through the agreed channel. Before submission, verify the final repository contents and confirm that no secrets or unreviewed local artifacts are included.