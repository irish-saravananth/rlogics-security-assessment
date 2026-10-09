import json
import subprocess
import sys

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from security_gate import evaluate_report


def report_with(*vulnerabilities):
    return {
        "ArtifactName": "test-image",
        "Results": [
            {
                "Target": "test-image",
                "Vulnerabilities": list(vulnerabilities),
            }
        ],
    }


def vulnerability(severity, fixed_version="", vuln_id="CVE-TEST"):
    return {
        "VulnerabilityID": vuln_id,
        "PkgName": "test-package",
        "Severity": severity,
        "FixedVersion": fixed_version,
    }


def test_critical_finding_blocks():
    result = evaluate_report(
        report_with(vulnerability("CRITICAL", "2.0", "CVE-CRITICAL"))
    )
    assert result["decision"] == "BLOCK"
    assert result["summary"]["blocking_findings"] == 1


def test_high_with_fix_blocks():
    result = evaluate_report(report_with(vulnerability("HIGH", "2.0")))
    assert result["decision"] == "BLOCK"


def test_high_without_fix_warns():
    result = evaluate_report(report_with(vulnerability("HIGH")))
    assert result["decision"] == "WARN"
    assert result["summary"]["warnings"] == 1


def test_medium_and_low_warn():
    result = evaluate_report(
        report_with(
            vulnerability("MEDIUM", vuln_id="CVE-MEDIUM"),
            vulnerability("LOW", vuln_id="CVE-LOW"),
        )
    )
    assert result["decision"] == "WARN"
    assert result["summary"]["total_vulnerabilities"] == 2


def test_no_vulnerabilities_passes_within_scope():
    result = evaluate_report(
        {"ArtifactName": "clean-test-image", "Results": []}
    )
    assert result["decision"] == "PASS"


def test_malformed_report_is_rejected():
    with pytest.raises(ValueError):
        evaluate_report({"ArtifactName": "invalid"})


def test_missing_report_fails_closed(tmp_path):
    output = tmp_path / "gate.json"
    missing = tmp_path / "missing-trivy.json"

    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "security_gate.py"),
            "--report",
            str(missing),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 1
    assert json.loads(output.read_text())["decision"] == "BLOCK"
