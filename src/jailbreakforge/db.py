"""SQLite database persistence layer."""

from __future__ import annotations

import sqlite3
from collections import defaultdict
from pathlib import Path

from jailbreakforge.models import AttackResult, RunConfig, RunSummary


class Database:
    """SQLite persistence layer for JailbreakForge results."""

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS runs (
        id TEXT PRIMARY KEY,
        target_name TEXT NOT NULL,
        target_endpoint TEXT NOT NULL,
        target_model TEXT NOT NULL,
        provider TEXT NOT NULL,
        attacker_model TEXT NOT NULL,
        judge_model TEXT NOT NULL,
        categories TEXT NOT NULL,
        max_mutations INTEGER NOT NULL,
        started_at TEXT NOT NULL,
        completed_at TEXT,
        total_attacks INTEGER DEFAULT 0,
        total_blocked INTEGER DEFAULT 0,
        total_vulnerable INTEGER DEFAULT 0,
        total_partial INTEGER DEFAULT 0,
        security_score REAL
    );

    CREATE TABLE IF NOT EXISTS attacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id TEXT NOT NULL REFERENCES runs(id),
        category TEXT NOT NULL,
        seed_name TEXT NOT NULL,
        seed_prompt TEXT NOT NULL,
        final_prompt TEXT NOT NULL,
        mutation_count INTEGER DEFAULT 0,
        target_response TEXT,
        verdict TEXT CHECK(verdict IN ('BLOCKED', 'VULNERABLE', 'PARTIAL')),
        severity TEXT CHECK(severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')),
        reasoning TEXT,
        confidence REAL,
        created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE INDEX IF NOT EXISTS idx_attacks_run ON attacks(run_id);
    CREATE INDEX IF NOT EXISTS idx_attacks_category ON attacks(category);
    CREATE INDEX IF NOT EXISTS idx_attacks_verdict ON attacks(verdict);
    """

    def __init__(self, db_path: str | Path = "jailbreakforge.db"):
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._init_schema()

    def _init_schema(self):
        """Initialize the database schema if it doesn't exist."""
        with self.conn:
            self.conn.executescript(self.SCHEMA)

    def create_run(self, config: RunConfig) -> str:
        """Insert a new run record. Returns run_id."""
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO runs (
                    id, target_name, target_endpoint, target_model, provider, 
                    attacker_model, judge_model, categories, max_mutations, started_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    config.run_id,
                    config.target_name,
                    config.target_endpoint,
                    config.target_model,
                    config.provider,
                    config.attacker_model,
                    config.judge_model,
                    ",".join(config.categories),
                    config.max_mutations,
                    config.started_at,
                ),
            )
        return config.run_id

    def save_attack(self, run_id: str, result: AttackResult) -> None:
        """Insert an attack result record."""
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO attacks (
                    run_id, category, seed_name, seed_prompt, final_prompt, 
                    mutation_count, target_response, verdict, severity, 
                    reasoning, confidence, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    result.attack.category,
                    result.attack.seed_name,
                    result.attack.seed_prompt,
                    result.attack.final_prompt,
                    result.attack.mutation_count,
                    result.target_response,
                    result.verdict.verdict,
                    result.verdict.severity,
                    result.verdict.reasoning,
                    result.verdict.confidence,
                    result.timestamp,
                ),
            )

    def complete_run(self, run_id: str, summary: RunSummary) -> None:
        """Update run with completion stats and security score."""
        with self.conn:
            self.conn.execute(
                """
                UPDATE runs 
                SET completed_at = ?,
                    total_attacks = ?,
                    total_blocked = ?,
                    total_vulnerable = ?,
                    total_partial = ?,
                    security_score = ?
                WHERE id = ?
                """,
                (
                    summary.completed_at,
                    summary.total_attacks,
                    summary.total_blocked,
                    summary.total_vulnerable,
                    summary.total_partial,
                    summary.security_score,
                    run_id,
                ),
            )

    def get_run_results(self, run_id: str) -> list[dict]:
        """Get all attack results for a run."""
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.execute("SELECT * FROM attacks WHERE run_id = ?", (run_id,))
        return [dict(row) for row in cur.fetchall()]

    def get_category_summary(self, run_id: str) -> dict[str, dict[str, int]]:
        """Get per-category stats: total, blocked, vulnerable, partial."""
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.execute(
            """
            SELECT category, verdict, COUNT(*) as count 
            FROM attacks 
            WHERE run_id = ? 
            GROUP BY category, verdict
            """,
            (run_id,),
        )
        
        # Initialize default nested dict structure
        stats: dict[str, dict[str, int]] = defaultdict(
            lambda: {"TOTAL": 0, "BLOCKED": 0, "VULNERABLE": 0, "PARTIAL": 0}
        )
        
        for row in cur.fetchall():
            cat = row["category"]
            verdict = row["verdict"]
            count = row["count"]
            
            stats[cat][verdict] += count
            stats[cat]["TOTAL"] += count
            
        return dict(stats)

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
