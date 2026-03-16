# Requirements: JailbreakForge

**Defined:** 2026-03-16
**Core Value:** A security engineer runs one command targeting an AI model's API and gets a detailed security assessment with a scored breakdown of which attack vectors succeeded.

## v1 Requirements

### CLI

- [ ] **CLI-01**: User can run `jailbreakforge run --target <endpoint> --model <model_name>` to execute a full security audit
- [ ] **CLI-02**: User can run `jailbreakforge run --categories roleplay,encoding` to filter attack categories
- [ ] **CLI-03**: User sees a progress bar/spinner during attack execution with live stats (attacks sent, successes, failures)
- [ ] **CLI-04**: User can set `--max-mutations <N>` to control mutation depth per seed (default: 3)
- [ ] **CLI-05**: CLI displays an ethical use disclaimer before execution

### Attack Engine

- [ ] **ATK-01**: Tool loads seed prompt templates from 8 attack categories
- [ ] **ATK-02**: Attacker LLM generates adapted prompts from seed templates for the specific target
- [ ] **ATK-03**: Attacker LLM mutates failed prompts using evolutionary strategy (max N retries)
- [ ] **ATK-04**: Each attack attempt is logged with: category, seed, mutated prompt, target response, verdict
- [ ] **ATK-05**: Mutation strategy receives Judge feedback to guide next mutation

### Target Connector

- [ ] **TGT-01**: Tool supports OpenAI-compatible API endpoints (OpenAI, Groq, etc.)
- [ ] **TGT-02**: Tool supports Anthropic API format
- [ ] **TGT-03**: Tool supports generic HTTP POST endpoint with configurable request/response mapping
- [ ] **TGT-04**: Target connector handles rate limits (429) with exponential backoff
- [ ] **TGT-05**: Target connector configurable via CLI flags or config file

### Judge (Evaluation)

- [ ] **JDG-01**: Judge LLM evaluates each target response as Blocked or Vulnerable
- [ ] **JDG-02**: Judge returns structured JSON: `{verdict, category, severity, reasoning}`
- [ ] **JDG-03**: Judge detects partial compliance (model hedges but still leaks info)
- [ ] **JDG-04**: Judge classification is independent — never shares context with Attacker

### Storage

- [ ] **DB-01**: SQLite database stores all results for the current run
- [ ] **DB-02**: Each run gets a unique ID with timestamp and target metadata
- [ ] **DB-03**: Schema supports querying by category, verdict, and severity

### Report

- [ ] **RPT-01**: Tool generates a Markdown security report with executive summary
- [ ] **RPT-02**: Report includes Security Score calculated as `(Blocked / Total) × 100`
- [ ] **RPT-03**: Report includes per-category attack matrix showing success/failure rates
- [ ] **RPT-04**: Report includes example prompts and responses for each vulnerability found
- [ ] **RPT-05**: Report includes severity classification (Critical/High/Medium/Low) per vulnerability
- [ ] **RPT-06**: Report includes ethical disclaimer and methodology description

### Privacy & Config

- [ ] **PRIV-01**: API keys loaded from env vars or `.env` file, never hardcoded
- [ ] **PRIV-02**: Target API responses are stored locally only (SQLite), never sent to third parties
- [ ] **CFG-01**: LLM provider (Groq/OpenRouter) configurable via env var or config file
- [ ] **CFG-02**: Attacker and Judge can use different providers/models

## v2 Requirements

### Attack Engine
- **ATK-V2-01**: Multi-turn conversational escalation attacks
- **ATK-V2-02**: Custom seed template loading from user-provided YAML

### Target
- **TGT-V2-01**: Ollama (local model) target connector for offline auditing
- **TGT-V2-02**: Batch testing multiple models in one run

### Report
- **RPT-V2-01**: JSON report output for CI/CD integration
- **RPT-V2-02**: Historical comparison between runs (campaign mode)

## Out of Scope

| Feature | Reason |
|---------|--------|
| Web UI or dashboard | CLI-first — no frontend in v1 |
| Image/multimodal jailbreaks | Text-only for MVP |
| Model fine-tuning or training | Inference only — we use existing models |
| CI/CD pipeline integration | Standalone CLI first |
| Real-time monitoring | Single-run batch execution |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CLI-01 | Phase 1 | Pending |
| CLI-03 | Phase 1 | Pending |
| CLI-05 | Phase 1 | Pending |
| PRIV-01 | Phase 1 | Pending |
| CFG-01 | Phase 1 | Pending |
| CFG-02 | Phase 1 | Pending |
| ATK-01 | Phase 2 | Pending |
| ATK-02 | Phase 2 | Pending |
| ATK-03 | Phase 2 | Pending |
| ATK-04 | Phase 2 | Pending |
| ATK-05 | Phase 2 | Pending |
| TGT-01 | Phase 3 | Pending |
| TGT-02 | Phase 3 | Pending |
| TGT-03 | Phase 3 | Pending |
| TGT-04 | Phase 3 | Pending |
| TGT-05 | Phase 3 | Pending |
| JDG-01 | Phase 4 | Pending |
| JDG-02 | Phase 4 | Pending |
| JDG-03 | Phase 4 | Pending |
| JDG-04 | Phase 4 | Pending |
| DB-01 | Phase 4 | Pending |
| DB-02 | Phase 4 | Pending |
| DB-03 | Phase 4 | Pending |
| CLI-02 | Phase 5 | Pending |
| CLI-04 | Phase 5 | Pending |
| RPT-01 | Phase 5 | Pending |
| RPT-02 | Phase 5 | Pending |
| RPT-03 | Phase 5 | Pending |
| RPT-04 | Phase 5 | Pending |
| RPT-05 | Phase 5 | Pending |
| RPT-06 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 31 total
- Mapped to phases: 31
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-16*
