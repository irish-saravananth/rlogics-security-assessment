# Exercise 7 — AI Security Tool Comparison

**Candidate:** Saravanan T H  
**Assessment:** RLogics Solutions Security Analyst Engineer Practical Assessment  
**Status:** Research and recommendation; no live AI target tested

## 1. Objective and threat model

Assess open-source tools for repeatable security testing of an internal retrieval-augmented generation (RAG) application and a tool-using AI agent. The principal risks include prompt injection, sensitive information disclosure, data poisoning, unsafe output handling, excessive agency, unauthorised tool use and unbounded consumption.

Reference frameworks:
- OWASP Top 10 for LLM Applications 2025.
- OWASP Top 10 for Agentic Applications 2026.
- MITRE ATLAS, the evolving knowledge base of adversarial tactics and techniques against AI-enabled systems.

## 2. Tool comparison

| Dimension | Promptfoo | Microsoft PyRIT | NVIDIA garak |
|---|---|---|---|
| Primary purpose | LLM application evaluation and red teaming | Flexible generative-AI risk identification and adversarial testing | LLM vulnerability scanning using probes and detectors |
| Threat coverage | Prompt injection, jailbreaks, RAG risks, data leakage and custom policies | Configurable adversarial scenarios, multi-turn attacks and response scoring | Model-level probes for prompt injection, leakage, jailbreaks and other failure modes |
| Target support | Model providers, HTTP endpoints and custom application workflows | Multiple model providers, custom HTTP endpoints and extensible targets | Hugging Face models, APIs, REST-accessible targets and supported local model interfaces |
| Local execution | Scanner runs locally; target and attack-generation providers may still be remote | Can be configured for local or remote targets and scorers | Can use local models; remote providers may require credentials |
| CI/CD suitability | Strong: CLI, declarative configuration and CI integrations | Scriptable and extensible; requires more integration work | CLI-based and scriptable, with machine-readable JSONL reports |
| Evidence | Evaluation and red-team results suitable for regression workflows | Attack results, scores and conversation history; supports configurable storage/export | JSONL run reports and hit logs |
| Operational fit | Accessible for developer-led, repeatable application tests | Flexible for deeper, customised red-team scenarios | Useful complementary model-level scanner |
| Main limitation | Results depend on target configuration, attack strategy and graders; hosted providers can expose test data | More engineering effort; provider/scorer configuration and result interpretation require expertise | Probe coverage does not prove application-level authorisation or secure agent tool execution |

## 3. Open-source status and data considerations

- **Promptfoo:** MIT-licensed open-source project. Its scanner can run locally, but hosted attack generation, grading, cloud features or remote target providers may transmit prompts or outputs outside the environment. Configure local providers and review telemetry and data-handling settings before testing sensitive systems.
- **PyRIT:** MIT-licensed open-source framework. Target, scorer, storage and attack strategy choices determine whether data stays local. Review provider configuration and persistence settings.
- **garak:** Apache-2.0-licensed open-source scanner. Local execution is possible with supported local models, while remote generators may send test inputs to external services. Its JSONL output supports evidence collection and analysis.

Licensing statements refer to the projects' published licenses; production adoption still requires dependency and licence-policy review.

## 4. Recommendation

**Primary combination: Promptfoo + PyRIT.**

Use Promptfoo for repeatable application-level regression tests in pull requests and release pipelines. Use PyRIT for scheduled, deeper adversarial assessments of RAG and agent workflows, with controlled scenarios and reviewed scoring.

Retain garak as a complementary option for model-level probes or use it when a focused scanner is more appropriate. It is not a substitute for testing application authorisation, retrieval isolation or tool execution controls.

## 5. Safety and operating boundaries

- Test only a locally controlled target or an explicitly authorised test environment.
- Use synthetic documents, fake identities and dummy secrets.
- Begin with deterministic, low-impact tests; do not execute destructive agent actions.
- Disable real external side effects and constrain network egress.
- Keep test credentials out of source control and redact sensitive evidence.
- Review attack-generation and scoring providers before every run.
- Treat scanner results as evidence requiring triage, not as proof of security or compliance.

## 6. Official references

1. OWASP Top 10 for LLM Applications 2025:
   https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
2. OWASP Top 10 for Agentic Applications 2026:
   https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
3. MITRE ATLAS:
   https://atlas.mitre.org/
4. Promptfoo red-team documentation:
   https://www.promptfoo.dev/docs/red-team/
5. Microsoft PyRIT:
   https://github.com/microsoft/PyRIT
6. NVIDIA garak:
   https://github.com/NVIDIA/garak
