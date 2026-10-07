from typing import Any


CUSTOMERS = {
    "C001": {
        "customer_id": "C001",
        "name": "John Doe",
        "status": "active",
    },
    "C002": {
        "customer_id": "C002",
        "name": "Jane Smith",
        "status": "active",
    },
}


def delete_customer(
    customer_id: str,
) -> dict[str, Any]:

    customer = CUSTOMERS.get(customer_id)

    if not customer:
        return {
            "success": False,
            "error": "CUSTOMER_NOT_FOUND",
        }

    del CUSTOMERS[customer_id]

    return {
        "success": True,
        "customer_id": customer_id,
        "message": "CUSTOMER_DELETED",
    }