from typing import Any
from uuid import uuid4


TICKETS: dict[str, dict[str, Any]] = {}


def create_ticket(
    customer_id: str,
    subject: str,
    priority: str = "MEDIUM",
) -> dict[str, Any]:

    if not customer_id.strip():
        return {
            "success": False,
            "error": "INVALID_CUSTOMER_ID",
        }

    if not subject.strip():
        return {
            "success": False,
            "error": "INVALID_SUBJECT",
        }

    allowed_priorities = {
        "LOW",
        "MEDIUM",
        "HIGH",
    }

    if priority not in allowed_priorities:
        return {
            "success": False,
            "error": "INVALID_PRIORITY",
        }

    ticket_id = f"T{uuid4().hex[:6].upper()}"

    ticket = {
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "status": "OPEN",
        "priority": priority,
        "subject": subject,
    }

    TICKETS[ticket_id] = ticket

    return {
        "success": True,
        "data": ticket,
    }