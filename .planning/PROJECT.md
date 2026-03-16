# JailbreakForge

## What This Is

A CLI tool that automates AI security red teaming by acting as an "Attacker". It takes a target model or chatbot (via public API) and fires hundreds of dynamically mutated malicious prompts and jailbreak techniques to discover if the AI leaks sensitive data, ignores its guardrails, or generates toxic content. Results are evaluated by an LLM-as-Judge and compiled into a Markdown security report.

## Core Value

A security engineer (or developer) runs one command targeting an AI model's API and gets a detailed security assessment with a scored breakdown of which attack vectors succeeded — without writing a single jailbreak prompt manually.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] User can run a CLI command targeting a model API and receive a security assessment report
- [ ] Tool generates jailbreak prompts across 8 attack categories using an Attacker LLM
- [ ] Attacker LLM mutates failed prompts (max 3 attempts per seed) for evolutionary attacks
- [ ] Tool sends generated prompts to a configurable Target model API
- [ ] A Judge LLM evaluates each target response and classifies as Blocked/Vulnerable in JSON
- [ ] Results are stored in SQLite (one run → one report)
- [ ] Tool generates a Markdown report with Security Score, attack matrix, and per-category results
- [ ] LLM provider is configurable — supports Groq and OpenRouter
- [ ] API keys are stored securely (env variable, never hardcoded)
- [ ] Tool handles rate limits (429) with automatic retry/backoff

### Out of Scope

- Web UI or dashboard — CLI-first, no frontend in v1
- Local model support (Ollama) — public APIs only in v1
- Multi-turn conversational attacks — single-turn per seed in v1
- Image/multimodal jailbreaks — text-only in v1
- CI/CD integration — standalone tool, no pipeline hooks in v1
- Real-time monitoring — single-run CLI, batch execution

## Context

- **Architecture:** CLI pipeline with modular internals: seed loader → attacker (mutator) → target connector → judge → reporter. SQLite for persistence.
- **Attacker LLM:** Groq (Llama 3 8B default) or OpenRouter — generates and mutates jailbreak prompts. Uses free/cheap tiers.
- **Judge LLM:** Same provider pool — strict evaluator that outputs structured JSON verdicts.
- **Target:** Any model accessible via HTTP API (OpenAI, Anthropic, Gemini, etc.). Configurable endpoint.
- **Attack Strategy:** Hybrid evolutionary — seed templates per category + LLM mutation on failure (max 3 retries).
- **Security Score:** `(Blocked / Total) × 100` with rating bands (Robust/Moderate/Weak/Critical).

## Constraints

- **Execution:** Local CLI — no cloud infrastructure, no Docker required
- **LLM cost:** Free/cheap tier APIs only — Groq (free) + OpenRouter (pay-per-token)
- **Rate limits:** Must handle 429s gracefully with exponential backoff
- **Ethical:** Tool is for authorized security testing only — disclaimer in CLI and report
- **Performance:** Full 8-category audit (64+ prompts with mutations) < 5 minutes

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Hybrid evolutionary architecture | Balances attack intelligence (mutations) with simplicity and cost control | — Pending |
| Groq + OpenRouter as providers | Free tier (Groq) + flexible fallback (OpenRouter), proven in DocGen project | — Pending |
| SQLite simple (one run, one report) | MVP focus — no campaign history needed for portfolio showcase | — Pending |
| LLM-as-Judge with JSON output | Structured, automatable evaluation — industry standard (HarmBench, JAILJUDGE) | — Pending |
| Markdown-only report | Simple, readable, version-controllable — no HTML templating overhead | — Pending |
| 8 attack categories (standard set) | Covers major jailbreak vectors from academic literature (PAIR, TAP, HarmBench) | — Pending |
| Max 3 mutations per seed | Controls token cost while demonstrating evolutionary capability | — Pending |

---
*Last updated: 2026-03-16 after initialization*
