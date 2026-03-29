"""Mock Active Directory Tools"""
from typing import Dict, Any
import random
import string


def generate_username(first_name: str, last_name: str) -> str:
    """Generate a username from name"""
    return f"{first_name.lower()}.{last_name.lower()}"


def generate_password(length: int = 12) -> str:
    """Generate a random password"""
    chars = string.ascii_letters + string.digits + "!@#$%"
    return "".join(random.choices(chars, k=length))


def create_ad_account(full_name: str, department: str) -> Dict[str, Any]:
    """
    Mock AD account creation
    Returns: {username, password, status}
    """
    parts = full_name.split()
    username = generate_username(parts[0], parts[-1])
    password = generate_password()

    # Simulate occasional failure
    if random.random() < 0.1:  # 10% failure rate
        return {
            "status": "error",
            "error": "AD_CONNECTION_TIMEOUT",
            "message": "Active Directory connection timed out",
        }

    return {
        "status": "success",
        "username": username,
        "password": password,
        "user_id": f"AD-{random.randint(100000, 999999)}",
        "created_at": "2024-03-29T10:00:00Z",
    }


def create_email_account(username: str, full_name: str, department: str) -> Dict[str, Any]:
    """Mock Email account creation"""
    if random.random() < 0.05:
        return {
            "status": "error",
            "error": "SMTP_ERROR",
            "message": "Email service temporarily unavailable",
        }

    return {
        "status": "success",
        "email": f"{username}@company.com",
        "mailbox_size": "50GB",
        "created_at": "2024-03-29T10:00:30Z",
    }


def create_hr_record(employee_name: str, email: str, department: str, start_date: str) -> Dict[str, Any]:
    """Mock HR system record creation"""
    return {
        "status": "success",
        "employee_id": f"EMP-{random.randint(10000, 99999)}",
        "record_created": True,
        "details": {
            "name": employee_name,
            "email": email,
            "department": department,
            "start_date": start_date,
        },
    }
