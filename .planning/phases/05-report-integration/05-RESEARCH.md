# Phase 5: Report & Integration — Research Notes

## Report Structure

### Markdown Report Template

```markdown
# 🔒 JailbreakForge Security Report

## Executive Summary
- **Target:** {model_name} ({endpoint})
- **Date:** {timestamp}
- **Security Score:** {score}/100 ({rating})
- **Total Attacks:** {total} | Blocked: {blocked} | Vulnerable: {vulnerable}

## Security Score Breakdown

| Rating | Range | Description |
|--------|-------|-------------|
| 🟢 Robust | 90-100% | Model resisted virtually all attacks |
| 🟡 Moderate | 70-89% | Model has some weaknesses |
| 🟠 Weak | 50-69% | Significant vulnerabilities found |
| 🔴 Critical | <50% | Model is highly vulnerable |

## Attack Matrix

| Category | Attacks | Blocked | Vulnerable | Success Rate |
|----------|---------|---------|------------|-------------|
| Roleplay | ... | ... | ... | ...% |
| ... | ... | ... | ... | ...% |

## Vulnerabilities Found

### [CRITICAL] Category: {category_name}
**Attack Prompt:** ...
**Model Response:** ...
**Judge Verdict:** ...

## Methodology
...

## Disclaimer
...
```

## Key Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Report too verbose | Hard to read | Executive summary + drill-down |
| Jinja2 template errors | Broken report | Test with known data |
