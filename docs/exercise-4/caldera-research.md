# Exercise 4 — MITRE Caldera Research and Safe Emulation

**Candidate:** Saravanan T H  
**Status:** Research and execution plan; live Caldera execution not yet performed  
**Scope:** Disposable, isolated lab and benign discovery only

## 1. Purpose

MITRE Caldera is an adversary-emulation platform designed to help
security teams evaluate defensive controls using controlled,
repeatable operations. It can execute configured adversary behaviours
against authorised agents and collect results to assess detection
coverage.

This document describes a safe local validation plan. It does not

claim that Caldera was installed or executed during this assessment.

## 2. Architecture concepts

- **Core server:** Coordinates operations, manages configuration and
  provides the interface/API used by operators and components.
- **Plugins:** Extend functionality with additional abilities,
  integrations, interfaces and supporting capabilities.
- **Agents:** Endpoints that receive authorised tasks and return results.
  Agents must be confined to disposable lab systems.
- **Abilities:** Individual actions representing a behaviour, often
  mapped to MITRE ATT&CK techniques.
- **Adversary profiles:** Collections of abilities describing a
  selected behaviour or emulation scenario.
- **Operations:** A controlled run of an adversary profile against
  selected agents under configured constraints.
- **Planners:** Determine how abilities are selected and scheduled
  during an operation.
- **Facts:** Contextual information used by abilities and planners,
  such as host or environment attributes.

The exact available components depend on the installed Caldera version
and enabled plugins. Verify component names and ability definitions
against the version used in any future demonstration.

## 3. Three benign discovery scenarios

These are planned scenarios, not claims of live execution. Select
only the corresponding benign discovery ability from the installed
and reviewed plugin. Review its commands before running it.

| Planned action | ATT&CK mapping | Expected telemetry and detection idea |
|---|---|---|
| Identify the current user or account context | T1033 — System Owner/User Discovery | Process creation, shell/interpreter audit events and the process command line where collected. Alert on unexpected discovery commands from unusual parent processes or service accounts. |
| Identify operating system and host details | T1082 — System Information Discovery | Process execution and endpoint telemetry for system-information commands; correlate with host identity and initiating process. |
| List running processes | T1057 — Process Discovery | Process creation events and endpoint process telemetry. Baseline expected administrative activity and investigate unusual enumeration by an application workload. |

ATT&CK technique mappings describe the behaviour being emulated; they
do not imply that every command or event is malicious. Detection should
consider identity, parent process, host role, command context and
baseline behaviour.

## 4. Safe operation plan

1. Use a disposable VM or isolated local endpoint dedicated to this test.
2. Keep the Caldera server and endpoint on an isolated lab network.
   Do not expose the management interface or agent listener publicly.
3. Use synthetic test data and a dedicated, low-privilege lab identity.
4. Review the selected ability's full command and prerequisites before
   execution. Confirm it performs only the intended discovery.
5. Select one test endpoint and one benign ability at a time.
6. Record the test time, endpoint identifier, ability/technique,
   expected telemetry, observed telemetry and detection outcome.
7. Stop the operation and remove the test agent using the documented
   cleanup procedure. Destroy the disposable endpoint if appropriate.
8. Verify that no test agent, listener, credential or temporary
   configuration remains. Preserve sanitised evidence only.

Do not run credential dumping, persistence, lateral movement, evasion,
destructive actions or exfiltration. Do not target public or third-party
systems.

## 5. How emulation improves defence

- **Detection engineering:** Compare expected and observed telemetry,
  identify missing events and refine detection logic.
- **Control validation:** Verify that endpoint monitoring, audit
  collection and alert routing work end to end.
- **Coverage measurement:** Track which behaviours were tested, detected,
  missed or not applicable, with explicit limitations.
- **Deception security:** In an authorised lab, validate whether
  monitored decoy assets or canary resources produce useful alerts when
  accessed unexpectedly. Keep deception tests separate from production
  systems unless formally approved.
- **Regression testing:** Repeat approved benign scenarios after
  logging, agent, endpoint or detection-rule changes.

A missed alert should lead to a documented investigation and retest,
not an assumption that the endpoint is compromised.

## 6. Isolation, limitations and evidence

The assessment uses existing local Docker and Kubernetes labs. Caldera
has not yet been executed for this exercise, so no Caldera UI screenshots,
agent results or live-operation evidence are claimed.

Before any live demonstration, confirm network isolation, disposable
endpoint ownership, restricted permissions, approved benign commands,
monitoring availability and cleanup steps. If these prerequisites
cannot be met without affecting existing workloads, use the research
plan for the interview and explain the limitation.

## 7. Production considerations

A production emulation programme should use approved test windows,
written scope, a dedicated management plane, authenticated access,
least-privilege agents, change approval, central audit logging, rollback
procedures and explicit stop conditions. Ability updates should be
reviewed before use. Results should be versioned and linked to detection
rules, owners, remediation tasks and retest evidence.

## 8. Interview show-and-tell

Demonstrate the architecture and the three discovery-to-telemetry
mappings. Explain how the lab would be isolated, what telemetry should
appear, how a detection would be validated and what would be recorded
if no alert fired. Clearly state that this is a research plan unless a
live run is subsequently performed and evidenced.

## References to verify before submission

- MITRE Caldera official documentation: https://caldera.mitre.org/
- MITRE ATT&CK T1033: https://attack.mitre.org/techniques/T1033/
- MITRE ATT&CK T1082: https://attack.mitre.org/techniques/T1082/
- MITRE ATT&CK T1057: https://attack.mitre.org/techniques/T1057/

Confirm current Caldera documentation, plugin availability, ability
commands and licensing for the version selected for any demonstration.