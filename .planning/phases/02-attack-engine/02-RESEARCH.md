# Phase 2: Attack Engine — Research Notes

## Seed Template Design

### Template Format (YAML)
Each seed template should contain:
- `category`: Attack category identifier
- `name`: Human-readable technique name
- `description`: How the technique works
- `base_prompt`: The seed prompt template with `{target_description}` placeholder
- `mutation_hints`: Guidance for the Attacker LLM on how to mutate this type

### Mutation Strategy
Inspired by PAIR (Prompt Automatic Iterative Refinement):
1. Attacker receives: seed prompt + Judge feedback (why it failed)
2. Attacker generates mutated variant
3. Mutation types: rephrase, add context, change persona, encode differently
4. Max 3 mutations per seed (cost control)

## Key Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Attacker generates weak mutations | Low success rate | Include mutation hints in seeds |
| Attacker ignores Judge feedback | Wasted tokens | Structured feedback in mutation prompt |
