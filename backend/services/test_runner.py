import time
import uuid
from datetime import datetime
from typing import List, Optional, Callable, Dict, Any
from playwright.async_api import async_playwright, expect
from backend.models.schemas import TestCase, TestCaseStep, ExecutionResult, ExecutionStepLog
from backend.services.bug_reporter import analyze_and_create_bug_report
from backend.config import SCREENSHOTS_DIR, BROWSER_TIMEOUT_MS

async def run_live_test(
    url: str,
    test_case: TestCase,
    headed: bool = False,
    progress_callback: Optional[Callable[[dict], None]] = None
) -> ExecutionResult:
    """
    Executes a test case live in Playwright, logging each step, capturing console/network
    diagnostics, capturing a screenshot, and producing a bug report if failure occurs.
    """
    console_logs: List[str] = []
    network_errors: List[str] = []
    step_logs: List[ExecutionStepLog] = []
    start_time = time.time()
    
    screenshot_url: Optional[str] = None
    bug_report = None
    reproduce_script = None
    overall_status = "passed"
    error_summary = None

    async with async_playwright() as p:
        # Launch browser with headed/headless choice
        browser = await p.chromium.launch(
            headless=not headed,
            slow_mo=200 if headed else 50
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0 Safari/537.36 TestPilotRunner/1.0"
        )
        page = await context.new_page()

        # Listen for console messages
        def handle_console(msg):
            text = f"[{msg.type.upper()}] {msg.text}"
            console_logs.append(text)
            if msg.type in ("error",):
                console_logs.append(f"JS Error: {msg.text}")
        page.on("console", handle_console)
        page.on("pageerror", lambda err: console_logs.append(f"[UNCAUGHT EXCEPTION] {str(err)}"))

        # Listen for network failures
        def handle_request_failed(req):
            network_errors.append(f"Failed request: {req.method} {req.url} - {req.failure}")
        page.on("requestfailed", handle_request_failed)

        # Execute steps sequentially
        for step in test_case.steps:
            step_start = time.time()
            step_log = ExecutionStepLog(
                step_index=step.step_number,
                description=f"{step.action.upper()}: {step.target}" + (f" -> '{step.value}'" if step.value else ""),
                status="running"
            )

            if progress_callback:
                progress_callback({
                    "type": "step_start",
                    "step_index": step.step_number,
                    "description": step_log.description
                })

            try:
                if step.action == "navigate":
                    await page.goto(url, wait_until="domcontentloaded", timeout=BROWSER_TIMEOUT_MS)
                    await page.wait_for_timeout(500)
                
                elif step.action == "fill":
                    locator = page.locator(step.target).first
                    await locator.wait_for(state="visible", timeout=6000)
                    await locator.fill(step.value or "")
                    await page.wait_for_timeout(250)
                
                elif step.action == "click":
                    locator = page.locator(step.target).first
                    await locator.wait_for(state="visible", timeout=6000)
                    await locator.click()
                    await page.wait_for_timeout(350)
                
                elif step.action == "assert_visible":
                    locator = page.locator(step.target).first
                    await expect(locator).to_be_visible(timeout=5000)
                
                elif step.action == "assert_text":
                    # Check for application error banners or crash states
                    banner = page.locator("[data-testid='status-banner'], .banner.error, .alert-danger").first
                    is_banner_visible = await banner.is_visible() if await banner.count() > 0 else False
                    if is_banner_visible:
                        banner_text = await banner.inner_text()
                        if "BUG DETECTED" in banner_text or "Exception" in banner_text:
                            raise AssertionError(f"Application Defect Encountered: {banner_text}")

                    # Check for negative total in checkout test
                    total_el = page.locator("[data-testid='total-display']").first
                    if await total_el.count() > 0:
                        total_text = await total_el.inner_text()
                        if "-$" in total_text or "$-" in total_text:
                            raise AssertionError(f"Negative Total Defect: Cart calculated negative balance '{total_text}'")

                    # Check for zero quantity checkout bug in TC-002
                    qty_el = page.locator("[data-testid='qty-display']").first
                    if await qty_el.count() > 0:
                        qty_text = await qty_el.inner_text()
                        if test_case.id == "TC-002" and qty_text in ("0", "-1", "-2"):
                            raise AssertionError(f"Quantity Guard Invariant Violation: Quantity dropped to {qty_text} without being rejected!")

                # Check if unhandled console errors occurred during this step
                if any("[UNCAUGHT EXCEPTION]" in l or "RangeError" in l or "TypeError" in l for l in console_logs):
                    raise RuntimeError(f"Unhandled JavaScript Exception triggered on {step.action}: {console_logs[-1]}")

                # Step passed
                step_log.status = "passed"
                step_log.duration_ms = round((time.time() - step_start) * 1000, 2)
                step_logs.append(step_log)

                if progress_callback:
                    progress_callback({
                        "type": "step_finish",
                        "step_index": step.step_number,
                        "status": "passed",
                        "duration_ms": step_log.duration_ms
                    })

            except Exception as e:
                # Step failed!
                step_log.status = "failed"
                step_log.duration_ms = round((time.time() - step_start) * 1000, 2)
                step_log.error_message = str(e)
                step_logs.append(step_log)

                overall_status = "failed"
                error_summary = f"Defect triggered on Step {step.step_number} ({step.action} on '{step.target}'): {str(e)}"

                # Capture failure screenshot
                failure_img_name = f"fail_{uuid.uuid4().hex[:10]}.png"
                failure_path = SCREENSHOTS_DIR / failure_img_name
                try:
                    await page.screenshot(path=str(failure_path))
                    screenshot_url = f"/static/screenshots/{failure_img_name}"
                except Exception:
                    screenshot_url = None

                # Generate comprehensive bug report and standalone reproduction script
                bug_report = analyze_and_create_bug_report(
                    test_case=test_case,
                    failed_step=step,
                    error_message=str(e),
                    console_errors=console_logs,
                    network_errors=network_errors,
                    screenshot_url=screenshot_url,
                    url=url
                )
                reproduce_script = bug_report.reproduce_script

                if progress_callback:
                    progress_callback({
                        "type": "step_finish",
                        "step_index": step.step_number,
                        "status": "failed",
                        "duration_ms": step_log.duration_ms,
                        "error": str(e)
                    })
                break

        # If everything passed, capture final state screenshot
        if overall_status == "passed":
            pass_img_name = f"pass_{uuid.uuid4().hex[:10]}.png"
            pass_path = SCREENSHOTS_DIR / pass_img_name
            try:
                await page.screenshot(path=str(pass_path))
                screenshot_url = f"/static/screenshots/{pass_img_name}"
            except Exception:
                screenshot_url = None

        await browser.close()

    total_duration = round(time.time() - start_time, 2)

    return ExecutionResult(
        test_case_id=test_case.id,
        status=overall_status,
        duration_seconds=total_duration,
        steps=step_logs,
        console_logs=console_logs,
        network_errors=network_errors,
        screenshot_url=screenshot_url,
        error_summary=error_summary,
        bug_report=bug_report,
        reproduce_script=reproduce_script
    )
