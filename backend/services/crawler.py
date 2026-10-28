import uuid
import time
from datetime import datetime
from typing import Dict, Any, List
from playwright.async_api import async_playwright
from backend.models.schemas import InteractiveElement, PageInspectionResult
from backend.config import SCREENSHOTS_DIR, BROWSER_TIMEOUT_MS

async def inspect_page(url: str, wait_time_ms: int = 2000) -> PageInspectionResult:
    """
    Launches Playwright headless Chromium, navigates to the target URL,
    extracts interactive elements, DOM structure, and captures a screenshot.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 TestPilotAI/1.0"
        )
        page = await context.new_page()

        try:
            # Navigate
            await page.goto(url, wait_until="networkidle", timeout=BROWSER_TIMEOUT_MS)
        except Exception:
            # Fallback to domcontentloaded if networkidle times out
            await page.goto(url, wait_until="domcontentloaded", timeout=BROWSER_TIMEOUT_MS)

        if wait_time_ms > 0:
            await page.wait_for_timeout(wait_time_ms)

        title = await page.title()

        # Capture screenshot
        screenshot_filename = f"inspect_{uuid.uuid4().hex[:10]}.png"
        screenshot_path = SCREENSHOTS_DIR / screenshot_filename
        await page.screenshot(path=str(screenshot_path), full_page=False)
        screenshot_url = f"/static/screenshots/{screenshot_filename}"

        # Extract interactive elements via browser JS evaluation
        raw_elements = await page.evaluate("""
            () => {
                const results = [];
                const selectorCandidate = (el) => {
                    if (el.getAttribute('data-testid')) return `[data-testid="${el.getAttribute('data-testid')}"]`;
                    if (el.id) return `#${el.id}`;
                    if (el.name) return `${el.tagName.toLowerCase()}[name="${el.name}"]`;
                    if (el.getAttribute('aria-label')) return `[aria-label="${el.getAttribute('aria-label')}"]`;
                    if (el.innerText && el.innerText.length < 30) {
                        return `${el.tagName.toLowerCase()}:has-text("${el.innerText.trim()}")`;
                    }
                    return null;
                };

                const nodes = document.querySelectorAll('button, input, select, textarea, a, form, [role="button"]');
                nodes.forEach((el, index) => {
                    const rect = el.getBoundingClientRect();
                    const isVisible = rect.width > 0 && rect.height > 0 && window.getComputedStyle(el).display !== 'none';
                    if (!isVisible && el.type === 'hidden') return;

                    let sel = selectorCandidate(el);
                    if (!sel) {
                        sel = `${el.tagName.toLowerCase()}:nth-of-type(${index + 1})`;
                    }

                    results.push({
                        tag: el.tagName.toLowerCase(),
                        element_id: el.id || null,
                        name: el.name || null,
                        type: el.type || null,
                        role: el.getAttribute('role') || null,
                        placeholder: el.placeholder || null,
                        text: (el.innerText || el.value || '').trim().slice(0, 80),
                        selector: sel,
                        is_visible: isVisible,
                        required: el.required || false,
                        test_id: el.getAttribute('data-testid') || null,
                        value: el.value || null
                    });
                });
                return results;
            }
        """)

        await browser.close()

        # Parse into typed models
        interactive_elements: List[InteractiveElement] = []
        buttons_count = 0
        inputs_count = 0
        links_count = 0
        forms_count = 0

        for r in raw_elements:
            elem = InteractiveElement(**r)
            interactive_elements.append(elem)
            if elem.tag == "button" or elem.role == "button":
                buttons_count += 1
            elif elem.tag in ("input", "textarea", "select"):
                inputs_count += 1
            elif elem.tag == "a":
                links_count += 1
            elif elem.tag == "form":
                forms_count += 1

        return PageInspectionResult(
            url=url,
            title=title or "Untitled Web Page",
            elements_count=len(interactive_elements),
            elements=interactive_elements,
            screenshot_url=screenshot_url,
            forms_count=forms_count,
            inputs_count=inputs_count,
            buttons_count=buttons_count,
            links_count=links_count,
            timestamp=datetime.now().isoformat()
        )
