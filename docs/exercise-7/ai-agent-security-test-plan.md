# Exercise 7 — RAG and Tool-Using Agent Security Test Plan

**Candidate:** Saravanan T H  
**Status:** Proposed tests; not executed against a live target  
**Target model:** Internal RAG application with a tool-using AI agent  
**Safety boundary:** Synthetic documents, fake secrets, mocked tools and an isolated authorised test environment only.

## Test 1 — Direct and indirect prompt injection

**Threat:** A user prompt or retrieved document attempts to override system instructions, reveal hidden instructions or make the agent ignore its intended task.

**Test approach:** Submit a harmless direct injection prompt. Add a synthetic RAG document containing instructions to disregard policy and reveal a planted dummy marker. Test each input separately and in combination.

**Expected secure behaviour:** The application treats retrieved text as untrusted data, preserves its system policy and does not reveal protected instructions or the marker.

**Evidence:** Test ID, sanitised prompt, retrieved document ID, response, policy decision and pass/fail result.

**Likely mitigation:** Separate trusted instructions from retrieved content, constrain tool permissions, apply input/output controls and test retrieval-to-action paths. Prompt filtering alone is not a complete defence.

## Test 2 — Cross-user RAG data leakage

**Threat:** A user retrieves another user's restricted document or synthetic secret through direct questions, indirect prompts or ambiguous retrieval queries.

**Test approach:** Create two test identities and separate synthetic documents with unique dummy markers. Query as each identity, including requests that refer indirectly to the other identity's document.

**Expected secure behaviour:** Retrieval and answer generation respect the caller's authorisation. No restricted document, metadata or marker is disclosed across the identity boundary.

**Evidence:** Test identity, document ACL, retrieved document IDs, response and access-control decision. Redact content not needed for the finding.

**Likely mitigation:** Enforce authorisation at retrieval time, propagate user identity to data services, isolate tenant indexes where appropriate and add negative access-control regression tests.

## Test 3 — Excessive agency and unauthorised tool use

**Threat:** Prompt injection or an ordinary request persuades the agent to invoke a tool beyond the caller's permissions or perform a prohibited action.

**Test approach:** Replace real tools with mocks. Ask the agent to access a forbidden record or perform a simulated write action without the required approval. Record whether the tool invocation is attempted and whether the server authorises it.

**Expected secure behaviour:** Server-side authorisation denies the operation. High-impact actions require explicit approval where policy requires it; the model's response alone cannot grant permission.

**Evidence:** Tool-call proposal, authenticated principal, policy decision, mock execution log and approval state.

**Likely mitigation:** Least-privilege tool identities, allowlisted functions and parameters, server-side authorisation, approval gates, rate limits and auditable tool execution.

## Test 4 — Unsafe output handling

**Threat:** The model emits hostile or malformed output that a downstream component interprets as executable HTML, SQL, a shell command or another control-bearing format.

**Test approach:** Use a mocked downstream consumer and synthetic payloads containing HTML/JavaScript-like text, SQL metacharacters and shell metacharacters. Verify that output remains inert data and is never executed.

**Expected secure behaviour:** The application validates the expected schema, encodes output for its destination and uses parameterised APIs. No command, query or script executes from model-generated text.

**Evidence:** Sanitised model output, validation result, mock consumer logs and negative execution checks.

**Likely mitigation:** Treat model output as untrusted input, use context-appropriate encoding, schema validation, parameterised queries and safe APIs. Never pass model text directly to a shell.

## Test 5 — Unbounded consumption and tool-call loops

**Threat:** Repeated prompts, recursive tool calls or oversized retrieval results cause excessive token use, latency, cost or service degradation.

**Test approach:** In an isolated test environment, send a small bounded set of repeated requests and simulate a tool returning repeated or oversized results. Use strict request, token, time and tool-call limits.

**Expected secure behaviour:** The application enforces budgets and timeouts, terminates loops, limits retrieved content and returns a controlled error without affecting unrelated users.

**Evidence:** Request count, tool-call count, token/size metrics where available, elapsed time, limit-trigger events and final response.

**Likely mitigation:** Per-user rate limits, token and context budgets, bounded agent iterations, timeouts, circuit breakers, retrieval limits and alerts for anomalous consumption.

## Release assurance approach

1. **Pull request:** Run deterministic synthetic regression cases for prompt injection, data isolation, output validation and tool authorisation. Block release on confirmed high-impact failures.
2. **Build/release:** Run a bounded Promptfoo suite against a dedicated staging target. Store versioned configuration and sanitised results with the build identifier.
3. **Scheduled assessment:** Use PyRIT for broader, approved adversarial scenarios. Run garak against supported model targets when model-level probing adds value.
4. **Triage:** Assign each finding an owner, severity, reproducible test case and mitigation. Baseline accepted findings with a named owner and expiry.
5. **Retest:** Add confirmed failures to regression tests and verify the fix before promotion.
6. **Governance:** Use synthetic data, approved regions, least-privilege test credentials, restricted egress, bounded execution and privacy-aware evidence retention.

## Framework mapping

Use OWASP Top 10 for LLM Applications 2025 and OWASP Top 10 for Agentic Applications 2026 to organise application risks. Map relevant adversarial behaviours to MITRE ATLAS where useful. Framework mappings guide coverage; they do not by themselves prove that a control is effective.

## Execution record

No live model, production endpoint or external AI provider was tested for this plan. The five cases are proposed tests awaiting an authorised local or staging target.
