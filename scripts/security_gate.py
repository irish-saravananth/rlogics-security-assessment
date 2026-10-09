#!/usr/bin/env python3
"""Evaluate a Trivy JSON report against the assessment's security gates."""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


BLOCKING_SEVERITIES = {"CRITICAL"}
WARNING_SEVERITIES = {"MEDIUM", "LOW", "UNKNOWN"}


def evaluate_report(report: dict[str, Any]) -> dict[str, Any]:
    """Return a gate decision from a parsed Trivy report."""
    if not isinstance(report, dict) or not isinstance(report.get("Results"), list):
        raise ValueError("Not a valid Trivy report: expected a Results list")

    counts: Counter[str] = Counter()
    findings: list[dict[str, str]] = []
    blockers: list[str] = []
    warnings: list[str] = []

    for result in report["Results"]:
        if not isinstance(result, dict):
            raise ValueError("Malformed Trivy report: each result must be an object")

        vulnerabilities = result.get("Vulnerabilities") or []
        if not isinstance(vulnerabilities, list):
            raise ValueError("Malformed Trivy report: Vulnerabilities must be a list")

        target = str(result.get("Target", "unknown target"))

        for vuln in vulnerabilities:
            if not isinstance(vuln, dict):
                raise ValueError("Malformed Trivy report: vulnerability must be an object")

            severity = str(vuln.get("Severity", "UNKNOWN")).upper()
            vuln_id = str(vuln.get("VulnerabilityID", "UNKNOWN-ID"))
            package = str(vuln.get("PkgName", "unknown package"))
            fixed_version = str(vuln.get("FixedVersion") or "").strip()

            counts[severity] += 1
            finding = {
                "id": vuln_id,
                "package": package,
                "severity": severity,
                "target": target,
                "fixed_version": fixed_version,
            }
            findings.append(finding)

            if severity in BLOCKING_SEVERITIES:
                blockers.append(f"{vuln_id}: CRITICAL vulnerability in {package}")
            elif severity == "HIGH" and fixed_version:
                blockers.append(
                    f"{vuln_id}: HIGH vulnerability in {package}; "
                    f"fixed version available: {fixed_version}"
                )
            elif severity == "HIGH":
                warnings.append(
                    f"{vuln_id}: HIGH vulnerability in {package}; "
                    "no fixed version reported"
                )
            elif severity in WARNING_SEVERITIES:
                warnings.append(f"{vuln_id}: {severity} vulnerability in {package}")
            else:
                warnings.append(
                    f"{vuln_id}: unrecognized severity {severity!r} in {package}"
                )

    decision = "BLOCK" if blockers else ("WARN" if warnings else "PASS")

    return {
        "policy_version": "1.0",
        "artifact": report.get("ArtifactName", "unknown artifact"),
        "decision": decision,
        "summary": {
            "total_vulnerabilities": len(findings),
            "by_severity": dict(sorted(counts.items())),
            "blocking_findings": len(blockers),
            "warnings": len(warnings),
        },
        "blockers": blockers,
        "warnings": warnings,
        "findings": findings,
        "limitations": [
            "This evaluator handles Trivy vulnerability results only.",
            "It does not establish exploitability or assess business context.",
            "A reported fix does not guarantee that an upgrade is safe.",
            "Misconfigurations, secrets, licenses, and other scanner result types "
            "are not evaluated by this policy.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate Trivy JSON vulnerability results."
    )
    parser.add_argument("--report", required=True, help="Path to Trivy JSON report")
    parser.add_argument("--output", required=True, help="Path for gate decision JSON")
    args = parser.parse_args()

    report_path = Path(args.report)
    output_path = Path(args.output)

    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        result = evaluate_report(report)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        result = {
            "policy_version": "1.0",
            "decision": "BLOCK",
            "summary": {
                "total_vulnerabilities": 0,
                "blocking_findings": 1,
                "warnings": 0,
            },
            "blockers": [f"Unable to evaluate required Trivy report: {exc}"],
            "warnings": [],
            "findings": [],
        }

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(result, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        print(f"ERROR: cannot write gate report: {exc}", file=sys.stderr)
        return 2

    print(f"Security gate: {result['decision']}")
    print(f"Decision report: {output_path}")
    for blocker in result["blockers"]:
        print(f"BLOCK: {blocker}")
    for warning in result["warnings"]:
        print(f"WARN: {warning}")

    return 1 if result["decision"] == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
