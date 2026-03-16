# Roadmap: JailbreakForge

## Overview

JailbreakForge is built as a strict pipeline: seed prompts flow through an Attacker LLM (which mutates them), into a Target model API, through a Judge LLM evaluator, and into a SQLite database and Markdown report. The roadmap mirrors that pipeline — each phase delivers one complete, independently testable pipeline stage. Phase 5 wires the full pipeline end-to-end and validates the core value proposition: one command, full security audit, scored report.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Foundation** — CLI scaffold, config loading, data contracts, LLM provider abstraction
- [ ] **Phase 2: Attack Engine** — Seed templates, Attacker LLM prompt generation, mutation strategy
- [ ] **Phase 3: Target Connector** — HTTP connectors for OpenAI, Anthropic, and generic endpoints
- [ ] **Phase 4: Judge & Storage** — LLM-as-Judge evaluator, SQLite persistence, structured verdicts
- [ ] **Phase 5: Report & Integration** — Markdown report generator, full pipeline wiring, Security Score

## Phase Details

### Phase 1: Foundation
**Goal**: Developer can invoke JailbreakForge commands, load config securely, and the data contracts are established for all downstream phases
**Depends on**: Nothing (first phase)
**Requirements**: CLI-01, CLI-03, CLI-05, PRIV-01, CFG-01, CFG-02
**Success Criteria** (what must be TRUE):
  1. Running `jailbreakforge --help` displays available commands without error
  2. Running `jailbreakforge run` without API keys fails with a clear human-readable error, not a stack trace
  3. API keys are loaded from `.env` or env vars and never appear in logs or output
  4. A progress indicator is visible during operations that take more than one second
  5. Core data contracts (Attack, Result, Campaign) exist as dataclasses
  6. LLM provider abstraction supports Groq and OpenRouter with a factory pattern
**Plans**: 2 plans

Plans:
- [ ] 01-01-PLAN.md — Scaffold package, config loading, data contracts, .env handling
- [ ] 01-02-PLAN.md — LLM provider abstraction (Groq + OpenRouter), factory, retry decorator

---

### Phase 2: Attack Engine
**Goal**: JailbreakForge can generate and mutate jailbreak prompts across 8 categories using the Attacker LLM
**Depends on**: Phase 1
**Requirements**: ATK-01, ATK-02, ATK-03, ATK-04, ATK-05
**Success Criteria** (what must be TRUE):
  1. Seed templates exist for all 8 attack categories in a structured format (YAML/JSON)
  2. Attacker LLM generates adapted prompts from seed templates for a given target description
  3. When Judge reports failure, Attacker generates a mutated variant within 3 attempts
  4. Each attack attempt is logged as an `Attack` dataclass with category, prompt, and metadata
  5. Mutation strategy incorporates Judge feedback (why it failed) to guide next mutation
**Plans**: 2 plans

Plans:
- [ ] 02-01-PLAN.md — Seed template catalog (8 categories), template loader, category registry
- [ ] 02-02-PLAN.md — Attacker agent (prompt generation + mutation logic), evolutionary strategy

---

### Phase 3: Target Connector
**Goal**: JailbreakForge can send prompts to any target model API and receive responses
**Depends on**: Phase 1
**Requirements**: TGT-01, TGT-02, TGT-03, TGT-04, TGT-05
**Success Criteria** (what must be TRUE):
  1. OpenAI-compatible endpoint connector works (sends prompt, receives response text)
  2. Anthropic API connector works (handles Messages API format)
  3. Generic HTTP POST connector works with configurable request/response mapping
  4. 429 rate limit responses trigger automatic exponential backoff (max 3 retries)
  5. Target connector is configurable via CLI flags or config file
**Plans**: 2 plans

Plans:
- [ ] 03-01-PLAN.md — Target base class, OpenAI-compatible connector, rate-limit handling
- [ ] 03-02-PLAN.md — Anthropic connector, generic HTTP connector, CLI target configuration

---

### Phase 4: Judge & Storage
**Goal**: JailbreakForge can evaluate target responses with an LLM Judge and persist results in SQLite
**Depends on**: Phase 1
**Requirements**: JDG-01, JDG-02, JDG-03, JDG-04, DB-01, DB-02, DB-03
**Success Criteria** (what must be TRUE):
  1. Judge LLM evaluates a target response and returns structured JSON: `{verdict, category, severity, reasoning}`
  2. Judge correctly classifies a clearly compliant response as "Blocked"
  3. Judge correctly classifies a clearly non-compliant response as "Vulnerable"
  4. Judge detects partial compliance (hedging but still leaking)
  5. SQLite database stores all results for the current run with unique run ID
  6. Results are queryable by category, verdict, and severity
**Plans**: 2 plans

Plans:
- [ ] 04-01-PLAN.md — Judge agent (prompt templates, JSON parsing, verdict classification)
- [ ] 04-02-PLAN.md — SQLite schema, database module, run persistence

---

### Phase 5: Report & Integration
**Goal**: Running one command on a target API produces a full Markdown security report with Security Score
**Depends on**: Phase 2, Phase 3, Phase 4
**Requirements**: CLI-02, CLI-04, RPT-01, RPT-02, RPT-03, RPT-04, RPT-05, RPT-06
**Success Criteria** (what must be TRUE):
  1. Running `jailbreakforge run --target <endpoint>` executes the full attack pipeline (seed → attack → target → judge → store)
  2. A Markdown report is generated with executive summary and Security Score
  3. Report includes per-category attack matrix with success/failure rates
  4. Report includes example prompts and responses for each vulnerability found
  5. Report includes severity classification per vulnerability
  6. Report includes ethical disclaimer and methodology description
  7. Full audit of 8 categories completes in under 5 minutes on a standard machine
**Plans**: 2 plans

Plans:
- [ ] 05-01-PLAN.md — Report generator (Markdown templating, Security Score, attack matrix)
- [ ] 05-02-PLAN.md — Pipeline orchestrator, CLI wiring, E2E validation

---

## Progress

**Execution Order:**
Phases 2 and 3 can execute in parallel after Phase 1.
Phase 4 depends on Phase 1 only.
Phase 5 depends on all previous phases.

```
Phase 1 (Foundation)
    ├──▶ Phase 2 (Attack Engine)  ──┐
    ├──▶ Phase 3 (Target Connector)─┤──▶ Phase 5 (Report & Integration)
    └──▶ Phase 4 (Judge & Storage) ─┘
```

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 2/2 | ✅ Complete | 2026-03-16 |
| 2. Attack Engine | 2/2 | ✅ Complete | 2026-03-16 |
| 3. Target Connector | 2/2 | ✅ Complete | 2026-03-16 |
| 4. Judge & Storage | 2/2 | ✅ Complete | 2026-03-16 |
| 5. Report & Integration | 2/2 | ✅ Complete | 2026-03-16 |
