"""Mock Email Tools"""
from typing import Dict, Any
import random


def send_email(
    recipient: str, subject: str, body: str, sender: str = "noreply@company.com"
) -> Dict[str, Any]:
    """Mock email sending"""
    # Simulate failure on "welcome email" step to demo retry logic
    # This will fail first time but succeed on retry
    if random.random() < 0.3:  # 30% failure simulating real-world issues
        return {
            "status": "error",
            "error": "SMTP_TIMEOUT",
            "message": "Email service connection timeout",
        }

    return {
        "status": "success",
        "email_id": f"EMAIL-{random.randint(100000, 999999)}",
        "recipient": recipient,
        "subject": subject,
        "sent_at": "2024-03-29T10:05:00Z",
        "delivery_status": "sent",
    }


def send_bulk_email(recipients: list, subject: str, body: str) -> Dict[str, Any]:
    """Send email to multiple recipients"""
    return {
        "status": "success",
        "recipients": recipients,
        "subject": subject,
        "sent_at": "2024-03-29T10:05:00Z",
        "delivery_status": "sent to all",
    }


def get_email_template(template_name: str) -> Dict[str, Any]:
    """Get email template"""
    templates = {
        "welcome": {
            "subject": "Welcome to Company!",
            "body": "We're excited to have you join our team...",
        },
        "onboarding_schedule": {
            "subject": "Your Onboarding Schedule",
            "body": "Here's your schedule for the first week...",
        },
    }
    return templates.get(template_name, {})
