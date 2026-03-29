"""Data Retrieval Agent - Creates accounts and retrieves system access"""
from typing import Dict, Any
from app.tools import ad_tools, hr_tools

# Few-shot examples for account creation
DATA_RETRIEVAL_FEWSHOT = [
    {
        "input": {"name": "John Doe", "dept": "Engineering", "email": "john@company.com"},
        "process": "Create AD account → Create Email account → Create HR record",
        "output": {"accounts_created": 3, "status": "success"},
    },
    {
        "input": {"name": "Jane Smith", "dept": "Marketing", "email": "jane@company.com"},
        "process": "Retry failed AD creation → Create Email account → Verify all accounts",
        "output": {"accounts_created": 3, "status": "success", "retry_count": 1},
    },
    {
        "input": {"name": "Bob Wilson", "dept": "Sales", "email": "bob@company.com"},
        "process": "Create AD → Handle email timeout → Queue for retry",
        "output": {"accounts_created": 1, "status": "partial", "pending": ["email"]},
    },
]


class DataRetrievalAgent:
    """Creates accounts across systems (AD, Email, HR)"""

    def __init__(self):
        self.name = "Data Retrieval Agent"
        self.agent_id = "data-retrieval"

    def execute(self, employee_data: Dict[str, Any], retry_count: int = 0) -> Dict[str, Any]:
        """Execute account creation workflow"""
        try:
            # Step 1: Create AD account
            ad_result = ad_tools.create_ad_account(
                employee_data.get("name"), employee_data.get("department")
            )

            if ad_result.get("status") == "error":
                return {
                    "status": "error",
                    "error": ad_result.get("error"),
                    "message": "Failed to create AD account",
                    "retry_viable": True,
                }

            # Step 2: Create Email account
            email_result = ad_tools.create_email_account(
                ad_result.get("username"),
                employee_data.get("name"),
                employee_data.get("department"),
            )

            if email_result.get("status") == "error":
                return {
                    "status": "partial",
                    "ad_account": ad_result,
                    "email_error": email_result.get("error"),
                    "message": "AD created, but Email account creation failed",
                    "retry_viable": True,
                }

            # Step 3: Create HR record
            hr_result = ad_tools.create_hr_record(
                employee_data.get("name"),
                ad_result.get("username") + "@company.com",
                employee_data.get("department"),
                employee_data.get("start_date"),
            )

            return {
                "status": "success",
                "reasoning": f"Successfully created accounts in all 3 systems for {employee_data.get('name')}",
                "accounts": {"ad": ad_result, "email": email_result, "hr": hr_result},
                "retry_count": retry_count,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "retry_viable": True,
            }


def create_data_retrieval_agent() -> DataRetrievalAgent:
    """Factory to create data retrieval agent"""
    return DataRetrievalAgent()
