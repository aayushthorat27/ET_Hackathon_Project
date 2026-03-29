from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    ERROR = "error"
    RETRYING = "retrying"
    COMPLETED = "completed"
    ESCALATED = "escalated"


class StepStatus(str, Enum):
    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    ESCALATED = "escalated"


@dataclass
class EmployeeData:
    name: str
    email: str
    department: str
    start_date: str


@dataclass
class StepLog:
    timestamp: str
    step_id: int
    step_name: str
    agent_id: str
    agent_name: str
    message: str
    type: str  # info, success, warning, error
    reasoning: Optional[str] = None
    retry_count: int = 0


@dataclass
class WorkflowState:
    """LangGraph workflow state"""
    employee_data: EmployeeData
    workflow_id: str
    current_step: int = 0
    status: WorkflowStatus = WorkflowStatus.PENDING
    step_statuses: Dict[int, StepStatus] = field(default_factory=dict)
    logs: List[StepLog] = field(default_factory=list)
    errors: Dict[int, str] = field(default_factory=dict)
    feedback: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    token_usage: Dict[str, int] = field(default_factory=dict)
    step_results: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    retry_counts: Dict[int, int] = field(default_factory=dict)
    max_retries: int = 2
    active_agent: Optional[str] = None

    def add_log(self, log: StepLog) -> None:
        """Add a log entry to the workflow"""
        self.logs.append(log)

    def get_current_retry_count(self, step_id: int) -> int:
        """Get current retry count for a step"""
        return self.retry_counts.get(step_id, 0)

    def increment_retry(self, step_id: int) -> int:
        """Increment and return retry count for a step"""
        self.retry_counts[step_id] = self.get_current_retry_count(step_id) + 1
        return self.retry_counts[step_id]
