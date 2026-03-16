"""Core data contracts for the JailbreakForge pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Attack:
    """Represents a single attack attempt sent to a target model."""

    category: str
    seed_name: str
    seed_prompt: str
    final_prompt: str
    mutation_count: int
    target_description: str


@dataclass
class JudgeVerdict:
    """Structured evaluation verdict from the LLM-as-Judge."""

    verdict: str       # BLOCKED | VULNERABLE | PARTIAL
    severity: str      # CRITICAL | HIGH | MEDIUM | LOW
    reasoning: str
    confidence: float  # 0.0 - 1.0
    raw_response: str


@dataclass
class AttackResult:
    """Combined attack attempt + target response + judge evaluation."""

    attack: Attack
    target_response: str
    verdict: JudgeVerdict
    timestamp: str     # ISO 8601


@dataclass
class RunConfig:
    """Configuration for a single audit run."""

    run_id: str
    target_name: str
    target_endpoint: str
    target_model: str
    categories: list[str]
    max_mutations: int
    provider: str
    attacker_model: str
    judge_model: str
    started_at: str    # ISO 8601


@dataclass
class RunSummary:
    """Aggregated results for a completed audit run."""

    config: RunConfig
    results: list[AttackResult] = field(default_factory=list)
    total_attacks: int = 0
    total_blocked: int = 0
    total_vulnerable: int = 0
    total_partial: int = 0
    security_score: float = 100.0
    completed_at: str = ""
