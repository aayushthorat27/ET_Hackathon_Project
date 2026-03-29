"""Mock HR System Tools"""
from typing import Dict, Any, List
import random


def query_employees(department: str = None, experience_level: str = None) -> Dict[str, Any]:
    """Query employees for buddy assignment"""
    employees_db = {
        "engineering": [
            {"name": "Alice Johnson", "email": "alice@company.com", "level": "senior"},
            {"name": "Bob Smith", "email": "bob@company.com", "level": "mid"},
            {"name": "Charlie Brown", "email": "charlie@company.com", "level": "junior"},
        ],
        "marketing": [
            {"name": "Diana Prince", "email": "diana@company.com", "level": "senior"},
            {"name": "Ernest Lee", "email": "ernest@company.com", "level": "mid"},
        ],
        "sales": [
            {"name": "Fiona Green", "email": "fiona@company.com", "level": "senior"},
            {"name": "George Miller", "email": "george@company.com", "level": "mid"},
        ],
    }

    # Make department case-insensitive
    if department:
        department = department.lower()

    emp_list = employees_db.get(department, [])

    if experience_level:
        emp_list = [e for e in emp_list if e["level"] == experience_level]

    return {"status": "success", "employees": emp_list}


def get_department_info(department: str) -> Dict[str, Any]:
    """Get department information"""
    return {
        "status": "success",
        "department": department,
        "team_size": random.randint(5, 20),
        "manager": "TBD",
        "location": "HQ",
    }


def check_availability(employee_email: str) -> Dict[str, Any]:
    """Check if employee can be a buddy"""
    return {
        "status": "success",
        "available": random.random() > 0.2,  # 80% available
        "current_mentees": random.randint(0, 3),
    }


def assign_buddy(buddy_email: str, mentee_email: str) -> Dict[str, Any]:
    """Assign buddy to new employee"""
    return {
        "status": "success",
        "buddy": buddy_email,
        "mentee": mentee_email,
        "assignment_date": "2024-03-29",
        "duration": "90 days",
    }


def get_employee_info(email: str) -> Dict[str, Any]:
    """Get employee info"""
    return {
        "status": "success",
        "email": email,
        "department": "Engineering",
        "manager": "Manager Name",
        "team": "Team Name",
    }
