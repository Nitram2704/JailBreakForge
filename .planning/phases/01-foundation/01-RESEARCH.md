# Phase 1: Foundation — Research Notes

## Pre-Implementation Verification

### Groq Free Tier Limits (MUST verify before implementation)
- Current model names for Llama 3 (verify at docs.groq.com)
- RPM/TPM limits for free tier
- Rate limit response format (headers, 429 body)

### OpenRouter API (MUST verify before implementation)
- Authentication method (Bearer token)
- Request/response format for chat completions
- Available Llama 3 models and pricing

### Typer + Rich Integration
- Typer callback pattern for global options
- Rich progress bar integration with Typer
- Tested in DocGen project — reuse patterns

## Key Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Groq rate limit too restrictive | Attacks slow | Queue + backoff + OpenRouter fallback |
| Provider API changes | Broken clients | Verify docs before coding |
