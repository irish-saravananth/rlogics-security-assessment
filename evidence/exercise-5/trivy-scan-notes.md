# Exercise 5 — Trivy Configuration Scan Evidence

- **Scan date:** 2026-10-11
- **Tool:** Trivy 0.71.2
- **Target:** `examples/exercise-5/`
- **Configuration files detected:** 3
- **HIGH/CRITICAL-filtered result:** 0 findings reported
- **Full report:** `trivy-config-scan.json`
- **Text report:** `trivy-config-scan.txt`

## Full-report findings

| Check ID | Severity | Finding |
|---|---|---|
| KSV-0020 | LOW | Container UID is at or below 10000 |
| KSV-0021 | LOW | Container GID is at or below 10000 |
| KSV-0125 | MEDIUM | Image registry flagged as untrusted by the configured check |

The UID/GID findings concern the configured non-root identity (101). Confirm image compatibility and filesystem permissions before changing it. The registry finding requires review of the image source and registry trust policy; digest pinning and provenance verification are recommended before production use.

## Scope and limitations

This was a static configuration scan of local YAML files. It did not deploy resources, assess live cluster state, verify Kyverno enforcement, test NetworkPolicy traffic, or prove image safety. Results are specific to the installed Trivy version and checks bundle at scan time.