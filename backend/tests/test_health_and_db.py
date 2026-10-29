"""
Automated Stage 2 Verification Tests:
Tests health endpoint, database schema initialization, and repository functions.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.database.db import check_db_health, init_db
from backend.database.repository import (
    save_project,
    save_test_case,
    save_execution_run,
    save_execution_result,
    get_recent_runs,
    get_run_results
)


@pytest.mark.asyncio
async def test_database_initialization_and_health():
    """Verify SQLite database initializes and passes health check."""
    await init_db()
    health_ok = await check_db_health()
    assert health_ok is True, "Database should be reachable and healthy"


@pytest.mark.asyncio
async def test_health_api_endpoint():
    """Verify /api/health returns 200 with database status."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "connected" in data["database"]
        assert data["playwright"] == "ready (chromium)"


@pytest.mark.asyncio
async def test_repository_save_and_retrieve():
    """Verify execution run and execution result persistence."""
    # 1. Create Project
    project_id = await save_project(name="Unit Test Project", url="http://localhost:8000/demo/shop", project_id="test_proj")
    assert project_id == "test_proj"

    # 2. Create Test Case
    test_id = await save_test_case(
        test_id="TC-001",
        project_id=project_id,
        title="Sample Test Case",
        category="smoke",
        priority="high",
        steps=[{"step_number": 1, "action": "navigate", "target": "url", "expected_outcome": "page loads"}],
        expected_result="Page loaded successfully"
    )
    assert test_id == "TC-001"

    # 3. Create Execution Run
    run_id = await save_execution_run(
        project_id=project_id,
        run_name="Unit Test Verification Run",
        total_tests=1,
        passed_tests=1,
        failed_tests=0,
        skipped_tests=0,
        duration_seconds=0.45,
        status="completed"
    )
    assert run_id.startswith("run_")

    # 4. Create Execution Result
    result_id = await save_execution_result(
        run_id=run_id,
        test_case_id=test_id,
        status="passed",
        duration_seconds=0.45,
        steps=[{"step_index": 1, "description": "Sample step", "status": "passed"}],
        error_summary=None
    )
    assert result_id.startswith("res_")

    runs = await get_recent_runs(limit=5)
    assert any(r["id"] == run_id for r in runs), "Saved run should appear in recent runs"

    results = await get_run_results(run_id)
    assert len(results) == 1
    assert results[0]["test_case_id"] == "TC-001"
    assert results[0]["status"] == "passed"
