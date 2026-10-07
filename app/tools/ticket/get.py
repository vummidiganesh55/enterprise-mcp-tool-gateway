from typing import Any


TICKETS = {
    "T001": {
        "ticket_id": "T001",
        "customer_id": "C001",
        "status": "OPEN",
        "priority": "HIGH",
        "subject": "Payment issue",
    },
    "T002": {
        "ticket_id": "T002",
        "customer_id": "C002",
        "status": "RESOLVED",
        "priority": "MEDIUM",
        "subject": "Refund request",
    },
}


def get_ticket(
    ticket_id: str,
) -> dict[str, Any]:

    ticket = TICKETS.get(ticket_id)

    if not ticket:
        return {
            "success": False,
            "error": "TICKET_NOT_FOUND",
        }

    return {
        "success": True,
        "data": ticket,
    }