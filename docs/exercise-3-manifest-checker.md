# Exercise 3 — Kubernetes Manifest Security Checker

## 1. Purpose

This Python utility statically inspects Kubernetes YAML manifests and reports potentially risky workload configurations before deployment. It is designed as a lightweight security gate for local use and CI/CD pipelines. It does not deploy resources or modify manifests.

## 2. Inputs and outputs

**Inputs**
- One or more Kubernetes YAML files.
- Optional `--fail-on` severity threshold.
- Optional `--strict` flag to fail on any finding.

**Supported workload kinds**
- Pod
- Deployment
- StatefulSet
- DaemonSet
- ReplicaSet
- Job
- ReplicationController
- CronJob

**Outputs**
- A Markdown-style findings table containing severity, rule, resource, and finding.
- A summary of finding counts by severity.
- Exit code `0` when the configured gate passes, or `1` when it fails.

Unreadable files and malformed YAML produce an `INPUT_ERROR` finding.

## 3. Security checks

The checker identifies:
- Privileged containers.
- Explicit root execution and missing non-root enforcement.
- `hostPath` volumes.
- `hostNetwork: true`.
- Missing CPU or memory limits and requests.
- Missing Pod-level or container-level security contexts.
- Privilege escalation not explicitly disabled.
- Writable container root filesystems.
- Linux capabilities not fully dropped.
- Mutable image tags, including `latest`.
- Missing container image references.

Findings are classified as CRITICAL, HIGH, MEDIUM, or LOW. The default gate fails on CRITICAL and HIGH findings.

## 4. Prerequisites

- Python 3.9 or later.
- PyYAML installed in the active Python environment.

Install the dependency:

```bash
python -m pip install PyYAML
```

## 5. Usage

Scan an unsafe manifest:

```bash
python scripts/security_manifest_checker.py \
  examples/exercise-3/unsafe-deployment.yaml
```

Scan multiple manifests:

```bash
python scripts/security_manifest_checker.py \
  examples/exercise-3/unsafe-deployment.yaml \
  examples/exercise-3/hardened-deployment.yaml
```

Fail only on CRITICAL findings:

```bash
python scripts/security_manifest_checker.py \
  --fail-on CRITICAL \
  examples/exercise-3/unsafe-deployment.yaml
```

Fail on any finding:

```bash
python scripts/security_manifest_checker.py \
  --strict \
  examples/exercise-3/hardened-deployment.yaml
```

Use the exit code in a pipeline:

```bash
python scripts/security_manifest_checker.py \
  examples/exercise-3/unsafe-deployment.yaml
status=$?
echo "Checker exit code: $status"
```

A nonzero exit code can fail a CI/CD step and prevent the pipeline from proceeding.

## 6. Examples and tests

Example manifests:
- `examples/exercise-3/unsafe-deployment.yaml`
- `examples/exercise-3/hardened-deployment.yaml`
- `examples/exercise-3/invalid.yaml`

Run the tests:

```bash
python -m unittest discover -s tests -v
```

The tests cover an unsafe manifest, a hardened manifest, malformed YAML, and a missing input file.

## 7. Assumptions and limitations

- This is static YAML analysis. It does not query a Kubernetes API server or inspect running workloads.
- It checks the supported workload kinds and their expected Pod template locations; other resource kinds may not be inspected.
- Image-tag checks are heuristic. A version tag is not equivalent to digest pinning.
- Findings indicate policy concerns, not proof of exploitability.
- Some controls require workload-specific exceptions. Exceptions should be reviewed and documented.
- This tool does not replace image scanning, runtime monitoring, cluster configuration review, or admission-time enforcement.

## 8. What a mature policy engine does better

A policy engine such as Kyverno or OPA with Gatekeeper can enforce policy at Kubernetes admission time, manage reusable policies centrally, support audit workflows, and integrate with cluster governance. Depending on the engine and configuration, policy systems may also support resource mutation or generation and controlled exceptions.

This script is useful for fast developer feedback but does not provide equivalent cluster-aware enforcement.

## 9. Production design decision

Use this checker as an early pre-deployment gate, not as the final enforcement boundary. For production, enforce equivalent critical controls at Kubernetes admission time through a centrally managed policy engine. Pin images by digest where appropriate, test policies against representative manifests, and manage exceptions through an auditable approval process.

This layered approach catches issues early in CI/CD while reducing reliance on individual deployment paths.