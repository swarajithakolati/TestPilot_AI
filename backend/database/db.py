"""
Async SQLite Database Initializer and Connection Management.
Provides structured tables for persistent test cases, execution runs,
bug reports, visual baselines, and historical regression telemetry.
"""

import logging
from typing import AsyncGenerator
import aiosqlite
from backend.config import DB_PATH

logger = logging.getLogger("testpilot.database")

SCHEMA_SQL = """
-- Projects / Target Sessions
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Static Code Analysis Findings
CREATE TABLE IF NOT EXISTS analysis_findings (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    file_name TEXT,
    component_name TEXT,
    severity TEXT NOT NULL,          -- critical, high, medium, low
    finding_type TEXT NOT NULL,      -- validation, security, accessibility, quality
    rule_id TEXT NOT NULL,
    evidence TEXT,
    explanation TEXT,
    suggested_fix TEXT,
    finding_label TEXT NOT NULL,     -- 'Static analysis (rule-based)', 'AI prediction (unconfirmed)', 'Confirmed by execution'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES projects(id)
);

-- Stored Test Cases
CREATE TABLE IF NOT EXISTS test_cases (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL,          -- smoke, edge_case, negative, security, accessibility, regression
    priority TEXT NOT NULL,          -- high, medium, low
    preconditions_json TEXT,
    steps_json TEXT NOT NULL,
    expected_result TEXT NOT NULL,
    gherkin TEXT,
    finding_label TEXT DEFAULT 'Static analysis (rule-based)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES projects(id)
);

-- Test Execution Sessions
CREATE TABLE IF NOT EXISTS execution_runs (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    run_name TEXT NOT NULL,
    total_tests INTEGER DEFAULT 0,
    passed_tests INTEGER DEFAULT 0,
    failed_tests INTEGER DEFAULT 0,
    skipped_tests INTEGER DEFAULT 0,
    duration_seconds REAL DEFAULT 0.0,
    status TEXT DEFAULT 'completed', -- completed, failed, cancelled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id) REFERENCES projects(id)
);

-- Individual Test Results inside a Run
CREATE TABLE IF NOT EXISTS execution_results (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    test_case_id TEXT NOT NULL,
    status TEXT NOT NULL,            -- passed, failed, error, skipped
    duration_seconds REAL DEFAULT 0.0,
    steps_json TEXT,
    screenshot_url TEXT,
    error_summary TEXT,
    bug_report_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(run_id) REFERENCES execution_runs(id),
    FOREIGN KEY(test_case_id) REFERENCES test_cases(id)
);

-- Visual Regression Baselines
CREATE TABLE IF NOT EXISTS visual_baselines (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    viewport_width INTEGER DEFAULT 1280,
    viewport_height INTEGER DEFAULT 800,
    image_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Generated Reports
CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    run_id TEXT,
    title TEXT NOT NULL,
    html_path TEXT,
    summary_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(run_id) REFERENCES execution_runs(id)
);

-- Key-Value System Settings
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


from contextlib import asynccontextmanager


@asynccontextmanager
async def get_db():
    """Context manager for managing an async SQLite database connection."""
    conn = await aiosqlite.connect(DB_PATH)
    conn.row_factory = aiosqlite.Row
    await conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        await conn.close()


async def init_db() -> None:
    """Initializes the database schema if tables do not exist."""
    logger.info(f"Initializing SQLite database at: {DB_PATH}")
    async with get_db() as conn:
        await conn.executescript(SCHEMA_SQL)
        await conn.commit()
    logger.info("SQLite database schema initialized successfully.")


async def check_db_health() -> bool:
    """Verifies that the SQLite database is reachable and operational."""
    try:
        async with get_db() as conn:
            async with conn.execute("SELECT 1;") as cursor:
                row = await cursor.fetchone()
                return bool(row and row[0] == 1)
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
