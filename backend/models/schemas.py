from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class InteractiveElement(BaseModel):
    tag: str
    element_id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    role: Optional[str] = None
    placeholder: Optional[str] = None
    text: Optional[str] = None
    selector: str
    is_visible: bool = True
    required: bool = False
    test_id: Optional[str] = None
    value: Optional[str] = None

class PageInspectionResult(BaseModel):
    url: str
    title: str
    elements_count: int
    elements: List[InteractiveElement]
    screenshot_url: Optional[str] = None
    forms_count: int = 0
    inputs_count: int = 0
    buttons_count: int = 0
    links_count: int = 0
    timestamp: str

class TestCaseStep(BaseModel):
    step_number: int
    action: str  # "navigate", "click", "fill", "select", "assert_visible", "assert_text", "assert_url"
    target: str  # selector or element description
    value: Optional[str] = None
    expected_outcome: str

class TestCase(BaseModel):
    id: str
    title: str
    description: str
    category: str  # "smoke", "regression", "edge_case", "security", "accessibility"
    priority: str  # "high", "medium", "low"
    preconditions: List[str] = Field(default_factory=list)
    steps: List[TestCaseStep] = Field(default_factory=list)
    expected_result: str
    gherkin: Optional[str] = None

class TestSuite(BaseModel):
    url: str
    generated_at: str
    model_used: str
    summary: str
    test_cases: List[TestCase]
    playwright_python_code: str
    playwright_ts_code: str

class InspectRequest(BaseModel):
    url: str
    wait_time_ms: Optional[int] = 2000

class GenerateRequest(BaseModel):
    url: str
    inspection: Optional[PageInspectionResult] = None
    custom_instructions: Optional[str] = None
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    provider: Optional[str] = "hybrid"

class ExecuteTestRequest(BaseModel):
    url: str
    test_case_id: str
    test_case: Optional[TestCase] = None
    custom_script: Optional[str] = None
    headed: bool = False

class ExecutionStepLog(BaseModel):
    step_index: int
    description: str
    status: str  # "pending", "running", "passed", "failed", "skipped"
    duration_ms: float = 0.0
    error_message: Optional[str] = None

class BugReport(BaseModel):
    bug_id: str
    test_case_id: str
    title: str
    severity: str  # "critical", "high", "medium", "low"
    category: str
    url: str
    failed_step: str
    expected_behavior: str
    actual_behavior: str
    root_cause_hypothesis: str
    suggested_fix: str
    reproduce_script: str
    screenshot_url: Optional[str] = None
    console_errors: List[str] = Field(default_factory=list)
    network_errors: List[str] = Field(default_factory=list)

class ExecutionResult(BaseModel):
    test_case_id: str
    status: str  # "passed", "failed", "error"
    duration_seconds: float
    steps: List[ExecutionStepLog]
    console_logs: List[str] = Field(default_factory=list)
    network_errors: List[str] = Field(default_factory=list)
    screenshot_url: Optional[str] = None
    error_summary: Optional[str] = None
    bug_report: Optional[BugReport] = None
    reproduce_script: Optional[str] = None
