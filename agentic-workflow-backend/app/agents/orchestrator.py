"""Orchestrator Agent - Routes workflow and coordinates other agents"""
from typing import Dict, Any
from app.utils import format_timestamp, EventLogger

# Few-shot examples for orchestrator routing
ORCHESTRATOR_FEWSHOT = [
    {
        "scenario": "New employee onboarding starting",
        "decision": "Delegate to Data Retrieval Agent to create accounts",
        "reasoning": "First step is to establish system access",
    },
    {
        "scenario": "Accounts created, now need to assign mentor",
        "decision": "Delegate to Decision-Making Agent to find buddy",
        "reasoning": "Need intelligent matching based on department and experience",
    },
    {
        "scenario": "Step failed with retry needed",
        "decision": "Retry with adjusted parameters, then escalate if fails again",
        "reasoning": "Follow fault tolerance pattern",
    },
]


class OrchestratorAgent:
    """Main orchestrator that routes workflow to specialized agents"""

    def __init__(self):
        self.name = "Orchestrator Agent"
        self.agent_id = "orchestrator"
        self.logger = EventLogger()

    def decide_next_step(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Decide which agent should execute next"""
        current_step = state.get("current_step", 0)
        total_steps = 5

        # Workflow orchestration logic
        if current_step == 0:
            next_agent = "data-retrieval"
            reasoning = "Starting workflow: Time to create user accounts in all systems"
        elif current_step == 1:
            next_agent = "decision-making"
            reasoning = "Accounts created: Need to intelligently assign buddy/mentor"
        elif current_step == 2:
            next_agent = "action-execution"
            reasoning = "Buddy assigned: Ready to schedule orientation meetings"
        elif current_step == 3:
            next_agent = "action-execution"
            reasoning = "Meetings scheduled: Now send welcome email and materials"
        elif current_step == 4:
            next_agent = "verification"
            reasoning = "All actions completed: Time to verify and audit everything"
        else:
            next_agent = None
            reasoning = "Workflow complete"

        return {
            "status": "success",
            "next_agent": next_agent,
            "reasoning": reasoning,
            "current_step": current_step,
            "total_steps": total_steps,
        }

    def handle_error(self, state: Dict[str, Any], error: str) -> Dict[str, Any]:
        """Handle errors and decide on retry/escalation"""
        retry_count = state.get("retry_counts", {}).get(state.get("current_step"), 0)
        max_retries = state.get("max_retries", 2)

        if retry_count < max_retries:
            return {
                "status": "retry",
                "action": "retry_step",
                "retry_count": retry_count + 1,
                "reasoning": f"Failed step, attempting retry {retry_count + 1}/{max_retries}",
            }
        else:
            return {
                "status": "escalate",
                "action": "escalate_to_admin",
                "retry_count": retry_count,
                "reasoning": f"Max retries ({max_retries}) exceeded. Escalating to human intervention",
            }

    def synchronize_agents(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronize state between agents"""
        return {
            "status": "synchronized",
            "shared_context": {
                "employee_data": state.get("employee_data"),
                "current_step": state.get("current_step"),
                "previous_results": state.get("step_results"),
                "logs": state.get("logs"),
            },
        }


def create_orchestrator() -> OrchestratorAgent:
    """Factory to create orchestrator agent"""
    return OrchestratorAgent()
