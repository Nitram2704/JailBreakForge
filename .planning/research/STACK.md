# Stack: JailbreakForge

## Core

| Technology | Purpose | Why This One |
|-----------|---------|-------------|
| **Python 3.10+** | Primary language | AI/ML ecosystem, rapid prototyping, portfolio alignment |
| **Typer** | CLI framework | Clean API, auto-help, used in DocGen (consistency) |
| **Rich** | Terminal UI | Progress bars, spinners, styled output |
| **httpx** | HTTP client | Async support, modern, replaces requests |
| **SQLite (stdlib)** | Result storage | Zero dependencies, portable, built into Python |

## LLM Providers

| Technology | Purpose | Why This One |
|-----------|---------|-------------|
| **Groq API** | Attacker + Judge LLM | Free tier, fastest inference (~100ms), Llama 3 |
| **OpenRouter API** | Fallback provider | Multi-model access, pay-per-token, flexible |

## Dev & Quality

| Technology | Purpose | Why This One |
|-----------|---------|-------------|
| **uv** | Package manager | Fast, modern, used in DocGen (consistency) |
| **python-dotenv** | Env loading | Standard .env support |
| **Jinja2** | Report templating | Markdown report generation |
| **pytest** | Testing | Standard Python testing |

## Project Structure

```
jailbreakforge/
├── pyproject.toml
├── .env.example
├── .gitignore
├── .planning/               # Planning docs (this directory)
├── src/
│   └── jailbreakforge/
│       ├── __init__.py
│       ├── cli.py           # Typer CLI entrypoint
│       ├── config.py        # Config + API key loading
│       ├── models.py        # Dataclasses: Attack, Result, Campaign
│       ├── providers/       # LLM provider abstraction
│       │   ├── __init__.py
│       │   ├── base.py      # Base ABC
│       │   ├── groq.py      # Groq client
│       │   ├── openrouter.py # OpenRouter client
│       │   └── factory.py   # Provider factory
│       ├── targets/         # Target model connectors
│       │   ├── __init__.py
│       │   ├── base.py      # Base ABC
│       │   ├── openai.py    # OpenAI-compatible
│       │   ├── anthropic.py # Anthropic Messages API
│       │   └── generic.py   # Generic HTTP POST
│       ├── attacks/         # Attack engine
│       │   ├── __init__.py
│       │   ├── seeds/       # YAML seed templates
│       │   │   ├── roleplay.yaml
│       │   │   ├── encoding.yaml
│       │   │   ├── logical_injection.yaml
│       │   │   ├── character_hijacking.yaml
│       │   │   ├── system_prompt_extraction.yaml
│       │   │   ├── hypothetical_scenario.yaml
│       │   │   ├── multiturn_escalation.yaml
│       │   │   └── language_switching.yaml
│       │   ├── loader.py    # Seed template loader
│       │   └── attacker.py  # Attacker agent (generate + mutate)
│       ├── judge.py         # LLM-as-Judge evaluator
│       ├── db.py            # SQLite persistence
│       └── reporter.py      # Markdown report generator
├── tests/
│   ├── test_config.py
│   ├── test_attacker.py
│   ├── test_judge.py
│   ├── test_db.py
│   └── test_reporter.py
└── docs/
    └── reports/             # Generated reports go here
```

## Dependency Decisions

| Decision | Rationale |
|----------|-----------|
| httpx over requests | Native async, modern API, better for concurrent API calls |
| SQLite stdlib over SQLAlchemy | Simple schema, no ORM overhead for single-table queries |
| Jinja2 for reports | Markdown templating is cleaner than string concatenation |
| Typer over Click | Higher-level API, auto-completion, used in DocGen |
| uv over pip | 10x faster installs, consistent with DocGen project |
