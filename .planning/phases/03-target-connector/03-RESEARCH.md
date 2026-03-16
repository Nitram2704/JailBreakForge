# Phase 3: Target Connector — Research Notes

## API Formats

### OpenAI-Compatible (OpenAI, Groq, Together, etc.)
```
POST /v1/chat/completions
{
  "model": "...",
  "messages": [{"role": "user", "content": "..."}]
}
```

### Anthropic Messages API
```
POST /v1/messages
{
  "model": "claude-3-...",
  "max_tokens": 1024,
  "messages": [{"role": "user", "content": "..."}]
}
Headers: x-api-key, anthropic-version
```

### Generic HTTP POST
User-configurable request/response mapping via config.

## Key Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Target API costs accumulate | Unexpected bills | Warn user with token estimate |
| Rate limits vary by provider | Inconsistent timing | Per-target rate limit config |
