# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-16)

**Core value:** A security engineer runs one command targeting an AI model's API and gets a detailed security assessment with a scored breakdown of which attack vectors succeeded.
**Current focus:** Phase 1 — Foundation

## Current Position

Phase: 1 of 5 (Foundation)
Plan: 0 of 10 total plans across all phases
Status: Planning Complete — Ready for Execution
Last activity: 2026-03-16 — Project initialized, brainstorm completed, planning structure created.

Progress: [░░░░░░░░░░] 0%

## Performance Metrics

**Velocity:**
- Total plans completed: 0
- Average duration: -
- Total execution time: -

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| (none yet) | - | - | - |

**Recent Trend:**
- Last 5 plans: (none)
- Trend: Starting

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Hybrid evolutionary architecture: Seed templates + LLM mutation (max 3 retries) — balances intelligence with cost control.
- Groq + OpenRouter as LLM providers (reusing pattern from DocGen project).
- SQLite simple: One run → one report. No campaign history in v1.
- Markdown-only reports. No JSON or HTML in v1.
- 8 standard attack categories: Roleplay, Character Hijacking, Base64/Encoding, Logical Injection, System Prompt Extraction, Hypothetical Scenario, Multi-turn Escalation, Language Switching.

### Pending Todos

- [Pre-Phase 1]: Verify Groq and OpenRouter free-tier rate limits and current model names before implementing provider abstraction.

### Blockers/Concerns

- [Pre-Phase 1]: Groq free-tier RPM/TPM limits must be confirmed before retry/backoff logic is implemented.
- [Pre-Phase 3]: OpenAI and Anthropic API formats should be verified at current docs to ensure target connectors are accurate.

## Session Continuity

Last session: 2026-03-16
Stopped at: Planning complete. Ready for Phase 1 execution.
Resume file: .planning/phases/01-foundation/01-01-PLAN.md
