# Exercise 5 — Kyverno Policy Validation Evidence

- **CLI:** Kyverno v1.15.2
- **Policy:** `examples/exercise-5/kyverno-no-privileged.yaml`
- **Execution mode:** Offline CLI evaluation
- **Cluster modified:** No
- **Policy applied to a live cluster:** No

## Test 1 — Privileged Pod

Resource: `examples/exercise-5/policy-tests/privileged-pod.yaml`

Result: **PASS — expected denial observed**

Output summary:
- Policy rule: `privileged-containers-forbidden`
- Result: validation failure
- Message: `Privileged containers are not permitted.`
- Pass: 0, Fail: 1, Error: 0

## Test 2 — Unprivileged Pod

Resource: `examples/exercise-5/policy-tests/unprivileged-pod.yaml`

Result: **PASS — expected acceptance observed**

Output summary:
- Pass: 1, Fail: 0, Error: 0

## Limitations

These tests demonstrate local policy evaluation against two sample Pod resources. They do not prove that Kyverno is installed, that admission enforcement is enabled in a cluster, or that every container configuration and policy edge case is covered. Live admission testing was intentionally not performed against the existing cluster.
