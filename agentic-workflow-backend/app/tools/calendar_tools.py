"""Mock Calendar Tools"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random


def schedule_meeting(
    organizer: str,
    attendees: List[str],
    title: str,
    duration_minutes: int,
    date_time: str,
) -> Dict[str, Any]:
    """Mock calendar meeting scheduling"""
    # Simulate occasional failure
    if random.random() < 0.05:
        return {
            "status": "error",
            "error": "CALENDAR_ERROR",
            "message": "Calendar service unavailable",
        }

    return {
        "status": "success",
        "meeting_id": f"MTG-{random.randint(100000, 999999)}",
        "title": title,
        "organizer": organizer,
        "attendees": attendees,
        "date_time": date_time,
        "duration_minutes": duration_minutes,
        "calendar_link": f"https://calendar.company.com/meeting/{random.randint(10000, 99999)}",
    }


def send_calendar_invite(meeting_id: str, recipient_email: str) -> Dict[str, Any]:
    """Send calendar invite"""
    return {
        "status": "success",
        "invite_sent": True,
        "recipient": recipient_email,
        "sent_at": datetime.utcnow().isoformat(),
    }


def check_availability(email: str, date_time: str) -> Dict[str, Any]:
    """Check if person is available"""
    return {
        "status": "success",
        "email": email,
        "available": random.random() > 0.3,  # 70% available
        "conflicts": [],
    }


def get_calendar(email: str, days_ahead: int = 7) -> Dict[str, Any]:
    """Get calendar for a person"""
    return {
        "status": "success",
        "email": email,
        "busy_slots": [],
        "available_slots": [
            "2024-03-29 14:00-15:00",
            "2024-03-29 15:00-16:00",
            "2024-04-01 10:00-11:00",
        ],
    }
