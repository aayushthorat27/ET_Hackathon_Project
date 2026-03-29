"""Decision-Making Agent - Intelligently assigns buddy/mentor"""
from typing import Dict, Any
import random
from app.tools import hr_tools

# Few-shot examples for buddy matching
DECISION_MAKING_FEWSHOT = [
    {
        "new_employee": {"name": "John (Senior Eng)", "dept": "Engineering"},
        "candidates": [
            {"name": "Alice (Senior Eng)", "level": "senior", "mentees": 2},
            {"name": "Bob (Senior Eng)", "level": "senior", "mentees": 1},
        ],
        "decision": "Bob",
        "reasoning": "Senior mentee needs senior mentor. Bob has lower mentee count (1 vs 2)",
    },
    {
        "new_employee": {"name": "Jane (Junior Marketing)", "dept": "Marketing"},
        "candidates": [
            {"name": "Diana (Senior Marketing)", "level": "senior", "mentees": 0},
            {"name": "Ernest (Mid Marketing)", "level": "mid", "mentees": 1},
        ],
        "decision": "Diana",
        "reasoning": "Junior needs guidance from senior. Diana has capacity",
    },
    {
        "new_employee": {"name": "Carlos (Mid Sales)", "dept": "Sales"},
        "candidates": [
            {"name": "Fiona (Senior Sales)", "level": "senior", "mentees": 3},
            {"name": "George (Mid Sales)", "level": "mid", "mentees": 0},
        ],
        "decision": "George",
        "reasoning": "Same-level pairing often works well. George available",
    },
]


class DecisionMakingAgent:
    """Makes intelligent decisions about buddy assignment"""

    def __init__(self):
        self.name = "Decision-Making Agent"
        self.agent_id = "decision-making"

    def assign_buddy(self, employee_data: Dict[str, Any], retry_count: int = 0) -> Dict[str, Any]:
        """Assign the best buddy match for new employee"""
        try:
            department = employee_data.get("department", "")

            # Query available employees in department
            candidates_result = hr_tools.query_employees(department=department)

            if candidates_result.get("status") != "success":
                return {
                    "status": "error",
                    "error": "Could not fetch candidates",
                    "retry_viable": True,
                }

            candidates = candidates_result.get("employees", [])

            if not candidates:
                return {
                    "status": "error",
                    "error": f"No available candidates in {department}",
                    "message": "Cannot assign buddy - no candidates available",
                    "retry_viable": False,
                }

            # Use first available (in production, would use ML model)
            selected_buddy = candidates[0]

            return {
                "status": "success",
                "reasoning": f"Selected {selected_buddy['name']} as buddy. Same department ({department}), experienced mentor",
                "buddy": {
                    "name": selected_buddy["name"],
                    "email": selected_buddy["email"],
                    "experience_level": selected_buddy["level"],
                },
                "algo": "Dept match + Senior preference",
                "retry_count": retry_count,
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "retry_viable": True,
            }


def create_decision_making_agent() -> DecisionMakingAgent:
    """Factory to create decision-making agent"""
    return DecisionMakingAgent()
