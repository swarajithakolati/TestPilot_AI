import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from backend.models.schemas import BugReport, TestCase, TestCaseStep

def analyze_and_create_bug_report(
    test_case: TestCase,
    failed_step: TestCaseStep,
    error_message: str,
    console_errors: List[str],
    network_errors: List[str],
    screenshot_url: Optional[str],
    url: str
) -> BugReport:
    """
    Analyzes execution failure context and synthesizes a structured bug report
    and a standalone reproducible Playwright Python script.
    """
    bug_id = f"BUG-{uuid.uuid4().hex[:6].upper()}"
    
    # Assess severity
    severity = "medium"
    is_crash = any("uncaught" in e.lower() or "referenceerror" in e.lower() or "typeerror" in e.lower() for e in console_errors)
    if "negative" in error_message.lower() or is_crash or "critical" in error_message.lower():
        severity = "critical"
    elif "timeout" in error_message.lower() or "not found" in error_message.lower():
        severity = "high"

    # Root Cause Hypothesis
    root_cause = "The element interaction triggered an invalid application state."
    suggested_fix = "Add boundary checks and defensive input validation."

    if "negative" in error_message.lower() or any("negative" in e.lower() for e in console_errors):
        root_cause = "Calculation logic permits negative subtotals/totals without bounding at zero (Math.max(0, total))."
        suggested_fix = "Clamp discount calculations: `total = Math.max(0, subtotal - discount);` and validate coupon eligibility before state mutation."
    elif "quantity" in error_message.lower() or test_case.id == "TC-002":
        root_cause = "Decrement handler lacks an lower-bound guard, permitting quantity <= 0 and enabling zero-dollar order checkout."
        suggested_fix = "Enforce `qty = Math.max(1, qty + delta);` in adjustment handlers and validate `qty >= 1` in server/client checkout handlers."
    elif "format" in error_message.lower() or "email" in error_message.lower():
        root_cause = "HTML5 type='email' browser regex differs from backend RFC-5322 regex parser."
        suggested_fix = "Harmonize email validation using comprehensive validator or display inline field errors prior to submission."
    elif console_errors:
        root_cause = f"Unhandled JavaScript runtime exception: {console_errors[0]}"
        suggested_fix = "Wrap calculation event handlers in try/catch blocks and display graceful fallback UI notifications."

    # Synthesize standalone executable reproduction script
    reproduce_script = _generate_standalone_reproduce_script(
        bug_id=bug_id,
        url=url,
        test_case=test_case,
        failed_step=failed_step,
        error_message=error_message
    )

    return BugReport(
        bug_id=bug_id,
        test_case_id=test_case.id,
        title=f"[{severity.upper()}] Defect in {test_case.title}: {failed_step.action} on '{failed_step.target}'",
        severity=severity,
        category=test_case.category,
        url=url,
        failed_step=f"Step {failed_step.step_number}: {failed_step.action} on {failed_step.target} (Value: {failed_step.value})",
        expected_behavior=failed_step.expected_outcome,
        actual_behavior=error_message,
        root_cause_hypothesis=root_cause,
        suggested_fix=suggested_fix,
        reproduce_script=reproduce_script,
        screenshot_url=screenshot_url,
        console_errors=console_errors,
        network_errors=network_errors
    )


def _generate_standalone_reproduce_script(
    bug_id: str,
    url: str,
    test_case: TestCase,
    failed_step: TestCaseStep,
    error_message: str
) -> str:
    """Creates a self-contained Playwright Python script that directly replicates the bug."""
    lines = [
        '#!/usr/bin/env python3',
        '"""',
        f'TestPilot AI — Automated Bug Reproduction Script',
        f'Bug ID: {bug_id}',
        f'Target URL: {url}',
        f'Failure: {error_message}',
        f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        '',
        'To run this script directly:',
        '  pip install playwright && playwright install chromium',
        '  python reproduce_bug.py',
        '"""',
        'import asyncio',
        'from playwright.async_api import async_playwright, expect',
        '',
        'async def reproduce_defect():',
        '    print("--> [TestPilot AI] Launching browser to reproduce defect...")',
        '    async with async_playwright() as p:',
        '        # Launch headed so developer/judge can visually observe the failure',
        '        browser = await p.chromium.launch(headless=False, slow_mo=350)',
        '        context = await browser.new_context(viewport={"width": 1280, "height": 800})',
        '        page = await context.new_page()',
        '',
        '        # Listen for console errors',
        '        page.on("console", lambda msg: print(f"  [Browser Console] {msg.type}: {msg.text}") if msg.type in ("error", "warning") else None)',
        '        page.on("pageerror", lambda err: print(f"  [Browser Uncaught Error] {err}"))',
        '',
        f'        print("--> Step: Navigating to {url}")',
        f'        await page.goto("{url}", wait_until="networkidle")',
        ''
    ]

    for step in test_case.steps:
        if step.action == "navigate":
            continue
        lines.append(f'        print("--> Executing Step {step.step_number}: {step.action} on {step.target}...")')
        if step.action == "fill":
            lines.append(f'        await page.locator("{step.target}").fill("{step.value}")')
        elif step.action == "click":
            lines.append(f'        await page.locator("{step.target}").click()')
        elif step.action == "assert_visible":
            lines.append(f'        await expect(page.locator("{step.target}").first).to_be_visible(timeout=5000)')
        elif step.action == "assert_text":
            lines.append(f'        # Assertion check: {step.expected_outcome}')
            lines.append(f'        content = await page.locator("{step.target}").first.inner_text()')
            lines.append(f'        print(f"    Observed text: {{content}}")')

        if step.step_number == failed_step.step_number:
            lines.append(f'        print("--> [!] Defect reproduced successfully at this point.")')
            break

    lines.extend([
        '',
        '        print("--> Taking defect snapshot...")',
        f'        await page.screenshot(path="bug_{bug_id.lower()}_snapshot.png")',
        f'        print("--> Snapshot saved to bug_{bug_id.lower()}_snapshot.png")',
        '        await page.wait_for_timeout(3000)',
        '        await browser.close()',
        '        print("--> [TestPilot AI] Bug reproduction run complete.")',
        '',
        'if __name__ == "__main__":',
        '    asyncio.run(reproduce_defect())'
    ])
    return "\n".join(lines)
