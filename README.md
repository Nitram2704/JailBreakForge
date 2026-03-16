# JailbreakForge

🔒 **AI Security Red Teaming Framework** — Automated jailbreak testing for AI models.

## What is JailbreakForge?

JailbreakForge is a Python CLI tool that automates AI security red teaming. It attacks target AI models using dynamically mutated prompts and jailbreak techniques, evaluates responses with an LLM-as-Judge, and generates a scored Markdown security report.

**One command. Full security audit. Scored report.**

## Key Features

- 🧠 **Intelligent Attacks** — LLM-generated prompts that evolve based on feedback
- 🎯 **8 Attack Categories** — Roleplay, Encoding, Logic Injection, and more
- ⚖️ **LLM-as-Judge** — Automated evaluation with structured verdicts
- 📊 **Security Score** — 0-100 score with per-category breakdown
- 📄 **Markdown Reports** — Professional audit reports with evidence

## Architecture

```
Seed Templates → Attacker LLM → Target API → Judge LLM → SQLite → Report
                     ↑                            │
                     └──── mutation feedback ──────┘
```

## Status

🚧 **In Development** — Planning phase complete. Implementation starting with Phase 1 (Foundation).

## License

MIT
