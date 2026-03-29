from datetime import datetime
import json


class EventLogger:
    """Centralized event logging for workflow execution"""

    def __init__(self):
        self.events = []

    def log_event(
        self,
        event_type: str,
        step_id: int,
        step_name: str,
        agent_id: str,
        agent_name: str,
        message: str,
        reasoning: str = None,
        retry_count: int = 0,
    ) -> dict:
        """Log an event and return the event object"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type,
            "step_id": step_id,
            "step_name": step_name,
            "agent_id": agent_id,
            "agent_name": agent_name,
            "message": message,
            "reasoning": reasoning,
            "retry_count": retry_count,
        }
        self.events.append(event)
        return event

    def get_events(self) -> list:
        """Get all events"""
        return self.events

    def clear_events(self) -> None:
        """Clear all events"""
        self.events = []
