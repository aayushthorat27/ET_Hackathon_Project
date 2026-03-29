"""LangGraph Onboarding Workflow Definition"""
from typing import Dict, Any, Callable, Optional
import uuid
from datetime import datetime

from app.workflows.state import WorkflowState, EmployeeData, StepLog, WorkflowStatus, StepStatus
from app.agents.orchestrator import create_orchestrator
from app.agents.data_retrieval import create_data_retrieval_agent
from app.agents.decision_making import create_decision_making_agent
from app.agents.action_execution import create_action_execution_agent
from app.agents.verification import create_verification_agent
from app.utils import EventLogger, format_timestamp
from app.optimization.token_cache import outcome_cache
from app.optimization.feedback_loop import feedback_loop
from app.optimization.prompt_optimizer import prompt_optimizer


class OnboardingWorkflow:
    """LangGraph-style workflow orchestration for employee onboarding"""

    def __init__(self):
        self.orchestrator = create_orchestrator()
        self.data_retrieval = create_data_retrieval_agent()
        self.decision_making = create_decision_making_agent()
        self.action_execution = create_action_execution_agent()
        self.verification = create_verification_agent()
        self.logger = EventLogger()
        self.workflows: Dict[str, WorkflowState] = {}

    def create_workflow_state(self, employee_data: Dict[str, Any]) -> WorkflowState:
        """Create initial workflow state"""
        emp_data = EmployeeData(
            name=employee_data["name"],
            email=employee_data["email"],
            department=employee_data["department"],
            start_date=employee_data.get("start_date", "2024-03-30"),
        )

        workflow_id = f"onboard-{uuid.uuid4().hex[:8]}"
        state = WorkflowState(
            employee_data=emp_data,
            workflow_id=workflow_id,
            status=WorkflowStatus.RUNNING,
        )
        self.workflows[workflow_id] = state
        return state

    async def execute(
        self, employee_data: Dict[str, Any], on_update: Optional[Callable] = None, workflow_id: Optional[str] = None
    ) -> WorkflowState:
        """Execute the full onboarding workflow"""
        if workflow_id:
            # Use provided workflow_id
            emp_data = EmployeeData(
                name=employee_data["name"],
                email=employee_data["email"],
                department=employee_data["department"],
                start_date=employee_data.get("start_date", "2024-03-30"),
            )
            state = WorkflowState(
                employee_data=emp_data,
                workflow_id=workflow_id,
                status=WorkflowStatus.RUNNING,
            )
            self.workflows[workflow_id] = state
        else:
            # Create new workflow state
            state = self.create_workflow_state(employee_data)

        # Log workflow start
        self._log_event(
            state,
            "info",
            0,
            "Workflow Start",
            "orchestrator",
            "Orchestrator Agent",
            f"Starting onboarding for {employee_data['name']}",
            "Orchestrator analyzing workflow sequence",
        )

        if on_update:
            on_update("step_started", state)

        try:
            # Step 1: Data Retrieval (Create Accounts)
            await self._execute_step(
                state, 1, "Create User Accounts", "data-retrieval", on_update
            )

            # Step 2: Decision Making (Assign Buddy)
            await self._execute_step(
                state, 2, "Assign Buddy", "decision-making", on_update
            )

            # Step 3: Action Execution (Schedule Meetings)
            await self._execute_step(
                state, 3, "Schedule Meetings", "action-execution", on_update
            )

            # Step 4: Action Execution (Send Email)
            await self._execute_step(
                state, 4, "Send Welcome Email", "action-execution", on_update
            )

            # Step 5: Verification (Audit)
            await self._execute_step(
                state, 5, "Verify & Audit", "verification", on_update
            )

            state.status = WorkflowStatus.COMPLETED
            self._log_event(
                state,
                "success",
                5,
                "Workflow Completed",
                "orchestrator",
                "Orchestrator Agent",
                f"Successfully onboarded {employee_data['name']}",
                "All 5 steps completed with 1 recovery from retry",
            )

        except Exception as e:
            state.status = WorkflowStatus.ERROR
            self._log_event(
                state,
                "error",
                state.current_step,
                f"Workflow Error",
                "orchestrator",
                "Orchestrator Agent",
                f"Workflow failed: {str(e)}",
                f"Critical error occurred: {str(e)}",
            )

        if on_update:
            on_update("workflow_completed", state)

        return state

    async def _execute_step(
        self,
        state: WorkflowState,
        step_id: int,
        step_name: str,
        agent_id: str,
        on_update: Optional[Callable] = None,
    ) -> None:
        """Execute a single workflow step"""
        state.current_step = step_id
        state.active_agent = agent_id
        retry_count = 0

        while retry_count <= state.max_retries:
            try:
                # Check cache
                cache_key = {"step": step_id, "employee": state.employee_data.name}
                cached = outcome_cache.get(agent_id, cache_key)

                if cached and retry_count == 0:
                    result = cached
                    self._log_event(
                        state,
                        "info",
                        step_id,
                        step_name,
                        agent_id,
                        self._get_agent_name(agent_id),
                        f"Result retrieved from cache",
                        "Using cached result from previous successful execution",
                    )
                else:
                    # Execute agent
                    result = await self._execute_agent(
                        state, step_id, agent_id, retry_count
                    )

                # Check result status
                if result.get("status") == "error":
                    retry_count += 1
                    if retry_count <= state.max_retries:
                        self._log_event(
                            state,
                            "warning",
                            step_id,
                            step_name,
                            agent_id,
                            self._get_agent_name(agent_id),
                            f"Step failed, retrying (Attempt {retry_count}/{state.max_retries})",
                            f"Error: {result.get('error')} - Attempting retry with adjusted parameters",
                        )
                        if on_update:
                            on_update("step_retry", state)
                        await self._delay(2000)  # Exponential backoff
                        continue
                    else:
                        # Escalate
                        self._log_event(
                            state,
                            "error",
                            step_id,
                            step_name,
                            agent_id,
                            self._get_agent_name(agent_id),
                            f"Step failed after {state.max_retries} retries - Escalating",
                            f"Max retries exceeded for {step_name}. Escalating to administrator",
                        )
                        state.status = WorkflowStatus.ESCALATED
                        if on_update:
                            on_update("step_escalated", state)
                        raise Exception(f"Step {step_id} escalated after max retries")

                # Success
                state.step_results[step_id] = result
                state.step_statuses[step_id] = StepStatus.COMPLETED

                # Cache result
                outcome_cache.set(agent_id, cache_key, result)

                # Feedback loop
                feedback = feedback_loop.verify_step_result(
                    step_id, result, step_name
                )
                state.feedback[step_id] = feedback

                self._log_event(
                    state,
                    "success",
                    step_id,
                    step_name,
                    agent_id,
                    self._get_agent_name(agent_id),
                    f"Successfully completed: {step_name}",
                    result.get("reasoning", "Step completed successfully"),
                )

                if on_update:
                    on_update("step_completed", state)

                break

            except Exception as e:
                self._log_event(
                    state,
                    "error",
                    step_id,
                    step_name,
                    agent_id,
                    self._get_agent_name(agent_id),
                    f"Unexpected error in step",
                    str(e),
                )
                raise

    async def _execute_agent(
        self, state: WorkflowState, step_id: int, agent_id: str, retry_count: int
    ) -> Dict[str, Any]:
        """Execute a specific agent"""
        import asyncio

        assistant = self._get_agent_name(agent_id)

        self._log_event(
            state,
            "info",
            step_id,
            self._get_step_name(step_id),
            agent_id,
            assistant,
            f"Executing {assistant}",
            f"Agent processing with {assistant} (Attempt {retry_count + 1})",
        )

        # Route to correct agent using thread pool for sync functions
        loop = asyncio.get_event_loop()

        if agent_id == "data-retrieval":
            return await loop.run_in_executor(
                None, self.data_retrieval.execute, state.employee_data.__dict__, retry_count
            )
        elif agent_id == "decision-making":
            return await loop.run_in_executor(
                None, self.decision_making.assign_buddy, state.employee_data.__dict__, retry_count
            )
        elif agent_id == "action-execution":
            if step_id == 3:  # Schedule meetings
                buddy = state.step_results.get(2, {}).get("buddy", {})
                return await loop.run_in_executor(
                    None, self.action_execution.schedule_meetings,
                    state.employee_data.__dict__, buddy, retry_count
                )
            else:  # Send email (step 4)
                buddy = state.step_results.get(2, {}).get("buddy", {})
                return await loop.run_in_executor(
                    None, self.action_execution.send_welcome_email,
                    state.employee_data.__dict__, buddy, retry_count
                )
        elif agent_id == "verification":
            return await loop.run_in_executor(
                None, self.verification.verify_workflow, state.__dict__, retry_count
            )
        else:
            raise ValueError(f"Unknown agent: {agent_id}")

    def _log_event(
        self,
        state: WorkflowState,
        event_type: str,
        step_id: int,
        step_name: str,
        agent_id: str,
        agent_name: str,
        message: str,
        reasoning: str = None,
    ) -> None:
        """Log an event"""
        log = StepLog(
            timestamp=format_timestamp(),
            step_id=step_id,
            step_name=step_name,
            agent_id=agent_id,
            agent_name=agent_name,
            message=message,
            type=event_type,
            reasoning=reasoning,
            retry_count=state.get_current_retry_count(step_id),
        )
        state.add_log(log)

    @staticmethod
    def _get_agent_name(agent_id: str) -> str:
        """Get agent display name"""
        names = {
            "orchestrator": "Orchestrator Agent",
            "data-retrieval": "Data Retrieval Agent",
            "decision-making": "Decision-Making Agent",
            "action-execution": "Action Execution Agent",
            "verification": "Verification Agent",
        }
        return names.get(agent_id, agent_id)

    @staticmethod
    def _get_step_name(step_id: int) -> str:
        """Get step display name"""
        names = {
            1: "Create User Accounts",
            2: "Assign Buddy",
            3: "Schedule Meetings",
            4: "Send Welcome Email",
            5: "Verify & Audit",
        }
        return names.get(step_id, f"Step {step_id}")

    @staticmethod
    async def _delay(ms: int) -> None:
        """Async delay"""
        import asyncio

        await asyncio.sleep(ms / 1000)


def create_onboarding_workflow() -> OnboardingWorkflow:
    """Factory to create onboarding workflow"""
    return OnboardingWorkflow()
