import os
import sys
from pathlib import Path

# Ensure project root is in sys.path so modules can be imported as `backend.*`
# regardless of whether uvicorn is launched from the root or from inside backend/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.config import PORT, HOST, STATIC_DIR, GEMINI_API_KEY, OPENAI_API_KEY, DB_PATH
from backend.database.db import init_db, check_db_health
from backend.models.schemas import (
    InspectRequest,
    PageInspectionResult,
    GenerateRequest,
    TestSuite,
    ExecuteTestRequest,
    ExecutionResult
)
from backend.services.crawler import inspect_page
from backend.services.ai_generator import generate_test_suite
from backend.services.test_runner import run_live_test
from backend.services.sample_apps import get_demo_shop_html


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite schema on startup
    await init_db()
    yield


app = FastAPI(
    title="TestPilot AI — API Engine",
    description="Autonomous Web Test Case & Bug Script Generation Platform (PS-03)",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for screenshots and reports
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# In-memory storage for active sessions
cached_inspections: Dict[str, PageInspectionResult] = {}
cached_suites: Dict[str, TestSuite] = {}

@app.get("/")
async def root():
    return {
        "app": "TestPilot AI API",
        "status": "online",
        "version": "1.0.0",
        "docs_url": "/docs",
        "demo_shop_url": f"http://localhost:{PORT}/demo/shop"
    }

@app.get("/api/health")
async def health():
    db_ok = await check_db_health()
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected (sqlite)" if db_ok else "disconnected",
        "db_path": str(DB_PATH),
        "has_gemini_key": bool(GEMINI_API_KEY),
        "has_openai_key": bool(OPENAI_API_KEY),
        "fallback_engine": "active (AST Heuristic)",
        "playwright": "ready (chromium)",
        "static_dir": str(STATIC_DIR)
    }

@app.get("/demo/shop", response_class=HTMLResponse)
async def demo_shop():
    """Serves the built-in target e-commerce store with intentional edge-case bugs."""
    return HTMLResponse(content=get_demo_shop_html(base_url=f"http://localhost:{PORT}"))

@app.get("/api/presets")
async def get_presets():
    """Returns ready-to-test preset scenarios for instant live demonstrations."""
    return [
        {
            "id": "preset-local-shop",
            "name": "AeroMart Pro Store (Built-in Testbed)",
            "url": f"http://localhost:{PORT}/demo/shop",
            "description": "Interactive tech store with real cart, quantity stepper, coupon codes, and intentional edge-case bugs (Zero quantity checkout, negative promo crash).",
            "category": "E-Commerce / FinTech",
            "recommended": True
        },
        {
            "id": "preset-saucedemo",
            "name": "SauceDemo Swag Labs (Public)",
            "url": "https://www.saucedemo.com",
            "description": "Standard industry benchmark web application with login credentials (standard_user, locked_out_user).",
            "category": "Authentication",
            "recommended": False
        },
        {
            "id": "preset-the-internet",
            "name": "The Internet Herokuapp (Public)",
            "url": "https://the-internet.herokuapp.com/login",
            "description": "Form authentication benchmark testing valid/invalid credential handling and flash banners.",
            "category": "Forms / Auth",
            "recommended": False
        }
    ]

@app.post("/api/inspect", response_model=PageInspectionResult)
async def api_inspect(payload: InspectRequest):
    """Inspects a target web URL using Playwright, harvesting DOM elements and capturing a screenshot."""
    try:
        url = payload.url.strip()
        if not url:
            raise HTTPException(status_code=400, detail="Target URL cannot be empty")
        
        # Rewrite localhost if needed
        if "localhost" in url and f":{PORT}" not in url and "http://" in url:
            pass

        result = await inspect_page(url=url, wait_time_ms=payload.wait_time_ms or 2000)
        cached_inspections[url] = result
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to inspect URL: {str(e)}")

@app.post("/api/generate", response_model=TestSuite)
async def api_generate(payload: GenerateRequest):
    """Generates structured test cases and executable Playwright scripts from inspection data."""
    try:
        url = payload.url.strip()
        inspection = payload.inspection or cached_inspections.get(url)
        
        # If no inspection data passed or cached, perform quick inspection
        if not inspection:
            inspection = await inspect_page(url=url)
            cached_inspections[url] = inspection

        suite = await generate_test_suite(
            url=url,
            inspection=inspection,
            custom_instructions=payload.custom_instructions,
            gemini_key=payload.gemini_api_key,
            openai_key=payload.openai_api_key,
            provider=payload.provider
        )
        cached_suites[url] = suite
        return suite
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate test suite: {str(e)}")

@app.post("/api/execute", response_model=ExecutionResult)
async def api_execute(payload: ExecuteTestRequest):
    """Executes a test case live in Playwright and captures failure diagnosis and bug reproduction."""
    try:
        url = payload.url.strip()
        test_case = payload.test_case
        
        if not test_case:
            suite = cached_suites.get(url)
            if suite:
                test_case = next((tc for tc in suite.test_cases if tc.id == payload.test_case_id), None)
        
        if not test_case:
            raise HTTPException(status_code=404, detail=f"Test case '{payload.test_case_id}' not found")

        result = await run_live_test(
            url=url,
            test_case=test_case,
            headed=payload.headed
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")

@app.websocket("/ws/execute")
async def websocket_execute(websocket: WebSocket):
    """WebSocket endpoint for real-time live execution progress and step telemetry."""
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        req_json = json.loads(data)
        url = req_json.get("url")
        test_case_dict = req_json.get("test_case")
        headed = req_json.get("headed", False)

        if not test_case_dict:
            await websocket.send_json({"type": "error", "message": "Missing test_case payload"})
            await websocket.close()
            return

        from backend.models.schemas import TestCase
        test_case = TestCase(**test_case_dict)

        def progress_cb(evt):
            asyncio.create_task(websocket.send_json(evt))

        result = await run_live_test(
            url=url,
            test_case=test_case,
            headed=headed,
            progress_callback=progress_cb
        )

        await websocket.send_json({
            "type": "completed",
            "result": result.model_dump()
        })
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
    finally:
        try:
            await websocket.close()
        except Exception:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
