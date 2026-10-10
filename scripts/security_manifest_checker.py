#!/usr/bin/env python3
"""Static security checks for Kubernetes YAML manifests."""

import argparse
import sys
from pathlib import Path

import yaml


SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def finding(severity, rule, message, resource):
    return {
        "severity": severity,
        "rule": rule,
        "resource": resource,
        "message": message,
    }


def resource_name(doc):
    kind = doc.get("kind", "Unknown")
    metadata = doc.get("metadata") or {}
    name = metadata.get("name", "<unnamed>")
    namespace = metadata.get("namespace", "default")
    return f"{kind}/{namespace}/{name}"


def pod_spec(doc):
    """Return a PodSpec for Pods and common workload controllers."""
    kind = doc.get("kind")
    spec = doc.get("spec") or {}

    if kind == "Pod":
        return spec

    if kind in {
        "Deployment", "StatefulSet", "DaemonSet", "ReplicaSet",
        "Job", "ReplicationController",
    }:
        template = spec.get("template") or {}
        return template.get("spec") or {}

    if kind == "CronJob":
        job_template = spec.get("jobTemplate") or {}
        job_spec = job_template.get("spec") or {}
        template = job_spec.get("template") or {}
        return template.get("spec") or {}

    return None


def inspect_document(doc, source):
    findings = []

    if not isinstance(doc, dict):
        return [finding(
            "HIGH", "INVALID_DOCUMENT",
            "YAML document must be a Kubernetes resource mapping.",
            f"{source}/<document>",
        )]

    kind = doc.get("kind")
    if not isinstance(kind, str) or not kind:
        return [finding(
            "HIGH", "MISSING_KIND",
            "Resource is missing a valid 'kind' field.",
            resource_name(doc),
        )]

    name = resource_name(doc)
    spec = pod_spec(doc)

    if spec is None:
        return findings

    pod_security = spec.get("securityContext") or {}
    containers = []

    for field in ("containers", "initContainers", "ephemeralContainers"):
        value = spec.get(field, [])
        if not isinstance(value, list):
            findings.append(finding(
                "HIGH", "INVALID_CONTAINER_LIST",
                f"'{field}' must be a list.",
                name,
            ))
            continue
        containers.extend((field, c) for c in value)

    if spec.get("hostNetwork") is True:
        findings.append(finding(
            "HIGH", "HOST_NETWORK",
            "hostNetwork exposes the Pod to the node network namespace.",
            name,
        ))

    for volume in spec.get("volumes") or []:
        if isinstance(volume, dict) and "hostPath" in volume:
            findings.append(finding(
                "CRITICAL", "HOST_PATH",
                f"Volume '{volume.get('name', '<unnamed>')}' uses hostPath.",
                name,
            ))

    if not pod_security:
        findings.append(finding(
            "MEDIUM", "MISSING_POD_SECURITY_CONTEXT",
            "Pod-level securityContext is not defined.",
            name,
        ))

    for field, container in containers:
        if not isinstance(container, dict):
            findings.append(finding(
                "HIGH", "INVALID_CONTAINER",
                f"An entry in '{field}' is not a container mapping.",
                name,
            ))
            continue

        cname = container.get("name", "<unnamed>")
        target = f"{name} container/{cname}"
        security = container.get("securityContext") or {}
        image = container.get("image", "")

        if security.get("privileged") is True:
            findings.append(finding(
                "CRITICAL", "PRIVILEGED_CONTAINER",
                "Container runs in privileged mode.",
                target,
            ))

        run_as_user = security.get("runAsUser", pod_security.get("runAsUser"))
        run_as_non_root = security.get(
            "runAsNonRoot", pod_security.get("runAsNonRoot")
        )

        if run_as_user == 0:
            findings.append(finding(
                "CRITICAL", "RUN_AS_ROOT",
                "Container explicitly sets runAsUser: 0.",
                target,
            ))
        elif run_as_non_root is not True:
            findings.append(finding(
                "HIGH", "NON_ROOT_NOT_ENFORCED",
                "runAsNonRoot: true is not enforced at container or Pod level.",
                target,
            ))

        if security.get("allowPrivilegeEscalation") is not False:
            findings.append(finding(
                "HIGH", "PRIVILEGE_ESCALATION",
                "Set allowPrivilegeEscalation: false.",
                target,
            ))

        if security.get("readOnlyRootFilesystem") is not True:
            findings.append(finding(
                "MEDIUM", "WRITABLE_ROOT_FILESYSTEM",
                "readOnlyRootFilesystem: true is not configured.",
                target,
            ))

        capabilities = security.get("capabilities") or {}
        if "ALL" not in (capabilities.get("drop") or []):
            findings.append(finding(
                "MEDIUM", "CAPABILITIES_NOT_DROPPED",
                "Drop all Linux capabilities where compatible.",
                target,
            ))

        if not security:
            findings.append(finding(
                "MEDIUM", "MISSING_CONTAINER_SECURITY_CONTEXT",
                "Container has no securityContext.",
                target,
            ))

        if not isinstance(image, str) or not image:
            findings.append(finding(
                "HIGH", "MISSING_IMAGE",
                "Container image is missing.",
                target,
            ))
        elif image.endswith(":latest") or (
            ":" not in image.rsplit("/", 1)[-1]
            and "@" not in image
        ):
            findings.append(finding(
                "MEDIUM", "MUTABLE_IMAGE_TAG",
                f"Image '{image}' is not pinned to a specific version or digest.",
                target,
            ))

        resources = container.get("resources") or {}
        limits = resources.get("limits") or {}
        requests = resources.get("requests") or {}

        if not limits.get("cpu") or not limits.get("memory"):
            findings.append(finding(
                "HIGH", "MISSING_RESOURCE_LIMITS",
                "Both CPU and memory limits should be specified.",
                target,
            ))

        if not requests.get("cpu") or not requests.get("memory"):
            findings.append(finding(
                "MEDIUM", "MISSING_RESOURCE_REQUESTS",
                "Both CPU and memory requests should be specified.",
                target,
            ))

    return findings


def scan_file(path):
    results = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            documents = list(yaml.safe_load_all(handle))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return [finding(
            "HIGH", "INPUT_ERROR",
            f"Cannot read or parse YAML: {exc.__class__.__name__}.",
            str(path),
        )]

    if not documents:
        return [finding(
            "LOW", "EMPTY_FILE",
            "File contains no YAML documents.",
            str(path),
        )]

    for index, doc in enumerate(documents, start=1):
        label = str(path) if len(documents) == 1 else f"{path}#document-{index}"
        results.extend(inspect_document(doc, label))

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Check Kubernetes YAML manifests for common security risks."
    )
    parser.add_argument(
        "paths", nargs="+", type=Path,
        help="YAML manifest files to inspect.",
    )
    parser.add_argument(
        "--fail-on", choices=("CRITICAL", "HIGH", "MEDIUM", "LOW"),
        default="HIGH",
        help="Exit non-zero if findings at this severity or higher exist (default: HIGH).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero for any finding, including low severity.",
    )
    args = parser.parse_args()

    results = []
    for path in args.paths:
        if not path.is_file():
            results.append(finding(
                "HIGH", "INPUT_ERROR", "Input path is not a regular file.", str(path)
            ))
        else:
            results.extend(scan_file(path))

    results.sort(key=lambda item: (
        SEVERITY_ORDER.get(item["severity"], 99),
        item["resource"],
        item["rule"],
    ))

    print("| Severity | Rule | Resource | Finding |")
    print("|---|---|---|---|")
    for item in results:
        message = item["message"].replace("|", "\\|").replace("\n", " ")
        print(
            f"| {item['severity']} | {item['rule']} | "
            f"{item['resource']} | {message} |"
        )

    counts = {}
    for item in results:
        counts[item["severity"]] = counts.get(item["severity"], 0) + 1

    print("\nSummary: " + (
        ", ".join(f"{level}={counts[level]}" for level in SEVERITY_ORDER if counts.get(level))
        or "No findings"
    ))

    threshold = SEVERITY_ORDER[args.fail_on]
    blocking = any(
        SEVERITY_ORDER.get(item["severity"], 99) <= threshold
        for item in results
    )
    if args.strict and results:
        blocking = True

    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
