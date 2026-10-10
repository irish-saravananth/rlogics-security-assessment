cat > docs/exercise-3-manifest-checker.md <<'MD'
# Exercise 3 — Kubernetes Manifest Security Checker

## 1. Purpose

This Python utility statically inspects Kubernetes YAML manifests and
reports potentially risky workload configurations before deployment.

It is intended as a lightweight security gate that can run locally or
as part of a CI/CD pipeline.

The checker does not deploy resources or modify input manifests.

## 2. Inputs and outputs

### Inputs

- One or more Kubernetes YAML files.
- YAML documents representing Pods or supported workload controllers.
- An optional severity threshold supplied with `--fail-on`.
- An optional `--strict` flag to fail on any reported finding.

Supported Pod workload types include:

- Pod
- Deployment
- StatefulSet
- DaemonSet
- ReplicaSet
- Job
- ReplicationController
- CronJob

### Outputs

The checker prints a Markdown-style findings table containing severity,
rule identifier, resource, and a remediation-oriented message.

It also prints a summary of finding counts by severity.

Exit codes:

- `0`: No findings meet the configured failure policy.
- `1`: The configured failure policy is triggered.

Malformed or unreadable input produces an `INPUT_ERROR` finding.

## 3. Security checks

The checker looks for configurations including:

| Check | Why it matters |
|---|---|
| Privileged containers | Can grant a container excessive host-level capabilities. |
| Root execution | Increases the impact of a container compromise. |
| `hostPath` volumes | Can expose host filesystem paths to a workload. |
| `hostNetwork: true` | Shares the node's network namespace. |
| Missing CPU or memory limits | Can allow workloads to consume excessive resources. |
| Missing resource requests | Makes workload resource planning less predictable. |
| Missing security contexts | Leaves important security settings unenforced. |
| Privilege escalation | Can allow a process to gain additional privileges. |
| Writable root filesystem | Allows writes to the container's root filesystem. |
| Linux capabilities not dropped | May leave unnecessary process capabilities available. |
| Mutable image tags | Can cause an image reference to resolve to different content over time. |
| Missing container image | Indicates an incomplete container specification. |

Findings are assigned CRITICAL, HIGH, MEDIUM, or LOW severity.
The default gate fails on CRITICAL and HIGH findings.

## 4. Prerequisites

- Python 3.9 or later.
- PyYAML installed in the active Python environment.

Install the dependency:

```bash
python -m pip install PyYAML