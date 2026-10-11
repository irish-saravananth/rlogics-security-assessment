# Exercise 5 — Kubernetes Security Review

**Candidate:** Saravanan T H
**Status:** Static manifest scan completed; Kyverno enforcement and live NetworkPolicy behavior not tested.

## 1. Risk-ranked findings in the supplied unsafe manifest

1. **Critical — Privileged container:** `privileged: true` weakens container isolation and can expose host-level capabilities.
2. **Critical — Host root mounted into the container:** `hostPath: /` exposes the host filesystem and may enable host compromise.
3. **High — Root execution:** `runAsUser: 0` increases the potential impact of process compromise.
4. **High — Default service account:** A dedicated workload identity and explicitly scoped permissions are preferable.
5. **High — Hard-coded environment password:** Credentials in manifests can leak through source control, API access or diagnostic output.
6. **High — Mutable image tag:** `nginx:latest` is not an immutable artifact reference. Use an approved image digest and verify provenance.
7. **Medium — Missing resource requests and limits:** Resource exhaustion can affect the workload and neighbouring services.
8. **Medium — Missing privilege-escalation, capability and seccomp controls:** Explicit hardening reduces the available attack surface.
9. **Medium — No network isolation:** Unrestricted connectivity increases opportunities for unwanted communication.
10. **Medium — Writable root filesystem:** Writable filesystem locations can increase the impact of compromise.

Risk levels are qualitative triage ratings. Actual severity depends on cluster privileges, node configuration, exposure and compensating controls.

## 2. Hardened deployment

Artifact: `examples/exercise-5/hardened-deployment.yaml`

The example defines a dedicated namespace and service account, disables automatic service-account token mounting, runs as non-root, drops Linux capabilities, disables privilege escalation, configures RuntimeDefault seccomp, uses a read-only root filesystem and sets resource requests and limits. It removes hostPath mounts and inline passwords.

### Remaining image considerations

The configured image is `nginxinc/nginx-unprivileged:1.27`. Trivy reported `KSV-0125` (MEDIUM), flagging the image registry as untrusted under its configured checks. The image is also tag-based rather than digest-pinned. Before production use, select an approved image source, verify the image and pin the approved digest.

Trivy also reported:
- `KSV-0020` (LOW): configured UID 101 is at or below 10000.
- `KSV-0021` (LOW): configured GID 101 is at or below 10000.

UID/GID 101 are non-root identities for this example. Do not change them blindly: confirm the image's expected user and filesystem permissions before choosing an alternative identity. These findings are scanner recommendations, not proof that the process runs as root.

## 3. Namespace, service account and RBAC

The example uses a dedicated namespace and service account. It defines no Role or RoleBinding because the web workload has no demonstrated need to call the Kubernetes API. If API access becomes necessary, grant only the required verbs and resources.

The namespace requests Pod Security Admission `restricted` enforcement. Actual enforcement must be verified against the target cluster and its Kubernetes configuration.

## 4. NetworkPolicy

Artifact: `examples/exercise-5/network-policy.yaml`

The policy restricts ingress to labelled peer pods and egress to pods matching the configured CoreDNS labels on TCP/UDP port 53.

Before deployment, verify the DNS labels, application dependencies, and intended ingress path. The policy does not create an external ingress path by itself. Enforcement depends on a NetworkPolicy-capable CNI. No live connectivity test has been performed for this assessment.

## 5. Trivy configuration scan

Evidence:
- `evidence/exercise-5/trivy-config-scan.json`
- `evidence/exercise-5/trivy-config-scan.txt`
- `evidence/exercise-5/trivy-scan-notes.md`

Trivy 0.71.2 scanned three YAML configuration files. The HIGH/CRITICAL-filtered scan reported zero findings at those severities. The full saved report contains three findings: KSV-0020 (LOW), KSV-0021 (LOW), and KSV-0125 (MEDIUM).

This is a static configuration scan, not a live cluster posture assessment, runtime test, or guarantee of security. Results depend on the Trivy version and checks bundle used.

## 6. kube-bench

`kube-bench` checks Kubernetes configuration against CIS benchmark recommendations. Its coverage depends on access to relevant node and control-plane configuration. A local kind cluster may not expose all host-level settings. Unsupported or unavailable checks must be recorded as limitations, not passes. No kube-bench run is claimed here.

## 7. Kyverno policy

Artifact: `examples/exercise-5/kyverno-no-privileged.yaml`

The intended policy denies privileged containers in regular, init and ephemeral container lists. The policy has been YAML-parsed and included in the Trivy configuration scan, but these checks do not establish Kyverno schema compatibility or enforcement behavior.

Kyverno CLI is not installed, and no policy has been applied to the existing cluster. Allow/deny behavior remains untested. Validate the policy against the intended Kyverno version and use a disposable isolated environment for enforcement tests. Record both a privileged workload rejection and an unprivileged workload acceptance before claiming the test passed.

## 8. Cosign admission verification

Cosign verification can be integrated with Kyverno image-verification policies. Admission controls should verify an approved image digest and trusted signer identity/key or certificate identity, with required attestations where applicable. Signing alone does not prove that an image is safe; combine provenance and signature verification with vulnerability policy and deployment controls.

No Cosign admission policy has been deployed or tested as part of this exercise.

## 9. CI, admission and runtime controls

- **CI:** SAST, SCA, secret scanning, image scanning, SBOM generation, manifest validation and signature/attestation generation.
- **Admission:** Enforce workload invariants, approved image sources, digest/signature requirements, security settings and documented exceptions.
- **Runtime:** Detect suspicious process behavior, policy drift, anomalous network activity and unexpected privilege or workload changes; route actionable alerts to incident response.

## 10. Evidence status and limitations

- Static YAML parsing: passed for all three YAML files.
- Trivy HIGH/CRITICAL-filtered configuration scan: zero findings reported.
- Full Trivy report: three findings, documented above.
- Unsafe manifest deployment: not performed.
- Kyverno schema validation and allow/deny testing: not performed.
- NetworkPolicy enforcement test: not performed.
- kube-bench run: not performed.
- Cosign admission verification: design described; not tested.

No claim is made that live cluster enforcement or production readiness has been demonstrated.