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


def update_customer(
    customer_id: str,
    name: str | None = None,
    status: str | None = None,
) -> dict[str, Any]:

    customer = CUSTOMERS.get(customer_id)

    if not customer:
        return {
            "success": False,
            "error": "CUSTOMER_NOT_FOUND",
        }

    if name is not None:
        customer["name"] = name

    if status is not None:
        customer["status"] = status

    return {
        "success": True,
        "data": customer,
    }