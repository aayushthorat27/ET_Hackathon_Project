"""Action Execution Agent - Schedules meetings and sends emails"""
from typing import Dict, Any
from datetime import datetime, timedelta
from app.tools import calendar_tools, email_tools

# Few-shot examples for action execution
ACTION_EXECUTION_FEWSHOT = [
    {
        "action": "Schedule meetings",
        "input": {"employee": "John", "buddy": "Alice"},
        "meetings": [
            "Day 1 9am: Team Intro",
            "Day 1 2pm: Department Overview",
            "Day 2 10am: 1:1 with Buddy",
        ],
        "output": {"meetings_scheduled": 3, "status": "success"},
    },
    {
        "action": "Send welcome email",
        "input": {"email": "john@company.com", "name": "John"},
        "email": "Welcome email + onboarding schedule + useful links",
        "output": {"email_sent": True, "status": "success"},
    },
    {
        "action": "Email fails, retry",
        "input": {"email": "jane@company.com"},
        "error": "SMTP timeout",
        "retry": "Exponential backoff + eventual success",
        "output": {"email_sent": True, "status": "success", "retry_count": 1},
    },
]


class ActionExecutionAgent:
    """Executes actions like scheduling meetings and sending emails"""

    def __init__(self):
        self.name = "Action Execution Agent"
        self.agent_id = "action-execution"

    def schedule_meetings(
        self, employee_data: Dict[str, Any], buddy_info: Dict[str, Any], retry_count: int = 0
    ) -> Dict[str, Any]:
        """Schedule orientation meetings"""
        try:
            employee_email = employee_data.get("email")
            buddy_email = buddy_info.get("email")
            employee_name = employee_data.get("name")

            meetings = [
                {
                    "title": f"Welcome to {employee_data.get('department')} Team",
                    "attendees": [employee_email, buddy_email],
                    "duration": 30,
                    "date": "2024-03-30 09:00",
                },
                {
                    "title": " Company Overview & Policies",
                    "attendees": [employee_email],
                    "duration": 45,
                    "date": "2024-03-30 14:00",
                },
                {
                    "title": f"Department Resources with {buddy_info.get('name')}",
                    "attendees": [employee_email, buddy_email],
                    "duration": 60,
                    "date": "2024-04-01 10:00",
                },
            ]

            scheduled_meetings = []
            for meeting in meetings:
                result = calendar_tools.schedule_meeting(
                    organizer="hr@company.com",
                    attendees=meeting["attendees"],
                    title=meeting["title"],
                    duration_minutes=meeting["duration"],
                    date_time=meeting["date"],
                )

                if result.get("status") != "success":
                    return {
                        "status": "error",
                        "error": result.get("error"),
                        "message": "Failed to schedule meeting",
                        "retry_viable": True,
                    }

                scheduled_meetings.append(result)

            return {
                "status": "success",
                "reasoning": f"Scheduled {len(scheduled_meetings)} orientation meetings for {employee_name} with buddy {buddy_info.get('name')}",
                "meetings": scheduled_meetings,
                "retry_count": retry_count,
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "retry_viable": True,
            }

    def send_welcome_email(
        self, employee_data: Dict[str, Any], buddy_info: Dict[str, Any], retry_count: int = 0
    ) -> Dict[str, Any]:
        """Send welcome email to new employee"""
        try:
            employee_email = employee_data.get("email")
            employee_name = employee_data.get("name")
            buddy_name = buddy_info.get("name")

            welcome_body = f"""
            Dear {employee_name},

            Welcome to the team! We're excited to have you join us starting {employee_data.get('start_date')}.

            Your buddy, {buddy_name}, will be your go-to person for the first 90 days.
            You'll receive separate calendar invites for orientation meetings.

            Key resources:
            - Employee handbook: https://company.com/handbook
            - Benefits info: https://company.com/benefits
            - IT support: https://support.company.com

            See you soon!
            """

            result = email_tools.send_email(
                recipient=employee_email,
                subject=f"Welcome to the Team, {employee_name}!",
                body=welcome_body,
            )

            if result.get("status") != "success":
                return {
                    "status": "error",
                    "error": result.get("error"),
                    "message": "Failed to send welcome email",
                    "retry_viable": True,
                }

            return {
                "status": "success",
                "reasoning": f"Sent personalized welcome email to {employee_email} with onboarding information",
                "email": result,
                "retry_count": retry_count,
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "retry_viable": True,
            }


def create_action_execution_agent() -> ActionExecutionAgent:
    """Factory to create action execution agent"""
    return ActionExecutionAgent()
