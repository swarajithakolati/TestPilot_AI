"""
Database Repository Helper Functions.
Provides simple, safe CRUD operations for TestPilot AI sessions, runs, and findings.
"""

import json
import uuid
from typing import List, Dict, Any, Optional
from backend.database.db import get_db


async def save_project(name: str, url: str, project_id: Optional[str] = None) -> str:
    """Creates or updates a target project/session."""
    p_id = project_id or f"proj_{uuid.uuid4().hex[:8]}"
    async with get_db() as conn:
        await conn.execute(
            """
            INSERT OR REPLACE INTO projects (id, name, url, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (p_id, name, url)
        )
        await conn.commit()
    return p_id


async def save_test_case(
    test_id: str,
    title: str,
    category: str,
    priority: str,
    steps: List[Dict[str, Any]],
    expected_result: str,
    project_id: Optional[str] = None,
    description: Optional[str] = None,
    gherkin: Optional[str] = None
) -> str:
    """Saves a structured test case."""
    async with get_db() as conn:
        await conn.execute(
            """
            INSERT OR REPLACE INTO test_cases (
                id, project_id, title, description, category, priority,
                steps_json, expected_result, gherkin
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                test_id, project_id, title, description or "", category,
                priority, json.dumps(steps), expected_result, gherkin
            )
        )
        await conn.commit()
    return test_id


async def save_execution_run(
    project_id: Optional[str],
    run_name: str,
    total_tests: int,
    passed_tests: int,
    failed_tests: int,
    skipped_tests: int,
    duration_seconds: float,
    status: str = "completed"
) -> str:
    """Saves a test execution session and returns the run_id."""
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    async with get_db() as conn:
        await conn.execute(
            """
            INSERT INTO execution_runs (
                id, project_id, run_name, total_tests, passed_tests, 
                failed_tests, skipped_tests, duration_seconds, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (run_id, project_id, run_name, total_tests, passed_tests, failed_tests, skipped_tests, duration_seconds, status)
        )
        await conn.commit()
    return run_id


async def save_execution_result(
    run_id: str,
    test_case_id: str,
    status: str,
    duration_seconds: float,
    steps: List[Dict[str, Any]],
    screenshot_url: Optional[str] = None,
    error_summary: Optional[str] = None,
    bug_report: Optional[Dict[str, Any]] = None
) -> str:
    """Saves an individual test result associated with a run."""
    result_id = f"res_{uuid.uuid4().hex[:8]}"
    async with get_db() as conn:
        await conn.execute(
            """
            INSERT INTO execution_results (
                id, run_id, test_case_id, status, duration_seconds,
                steps_json, screenshot_url, error_summary, bug_report_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result_id, run_id, test_case_id, status, duration_seconds,
                json.dumps(steps), screenshot_url, error_summary,
                json.dumps(bug_report) if bug_report else None
            )
        )
        await conn.commit()
    return result_id


async def get_recent_runs(limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieves recent test execution runs."""
    async with get_db() as conn:
        async with conn.execute(
            "SELECT * FROM execution_runs ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_run_results(run_id: str) -> List[Dict[str, Any]]:
    """Retrieves all test results belonging to a specific execution run."""
    async with get_db() as conn:
        async with conn.execute(
            "SELECT * FROM execution_results WHERE run_id = ? ORDER BY created_at ASC",
            (run_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                if item.get("steps_json"):
                    item["steps"] = json.loads(item["steps_json"])
                if item.get("bug_report_json"):
                    item["bug_report"] = json.loads(item["bug_report_json"])
                results.append(item)
            return results
