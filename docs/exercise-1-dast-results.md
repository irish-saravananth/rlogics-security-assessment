# Exercise 1 — DAST Baseline Assessment

## Scope

- Target: `http://127.0.0.1:5000`
- Application container: `secure-banking-app`
- Image: `secure-banking-portal:v1`
- Tool: OWASP ZAP Baseline Scan
- Assessment type: Automated spidering and passive security checks
- Date: 2026-10-13

## Evidence

- `evidence/exercise-1/dast/zap-baseline-report.html`
- `evidence/exercise-1/dast/zap-baseline-report.json`
- `evidence/exercise-1/dast/zap.yaml`

## Results

The ZAP console reported 55 passing checks, 12 warning categories, zero new failure alerts, and no in-progress alerts. The JSON report contains 15 alert types, including informational alerts.

Important findings included:

- Absence of anti-CSRF tokens
- Content Security Policy (CSP) header not set
- Missing anti-clickjacking header
- Subresource Integrity (SRI) attributes missing
- Cookie without a SameSite attribute
- Missing X-Content-Type-Options header
- Server version information disclosure
- Missing Permissions Policy and cross-origin policy headers

Alert counts represent occurrences reported by ZAP, not necessarily distinct vulnerabilities. The console warning count and JSON alert-type count use different groupings.

## Limitations

This was a baseline scan, not a full penetration test. Passive findings require contextual validation. The absence of an alert does not prove the absence of a vulnerability. Authentication-dependent functionality, business logic, authorization boundaries, and transaction workflows require separate testing.

No claim is made that the application is vulnerability-free. Findings should be triaged, remediated where appropriate, and reassessed.
