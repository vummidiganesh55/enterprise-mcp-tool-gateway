from typing import Any


ORDERS = {
    "ORD001": {
        "order_id": "ORD001",
        "customer_id": "C001",
        "status": "SHIPPED",
        "amount": 2499,
    },
    "ORD002": {
        "order_id": "ORD002",
        "customer_id": "C002",
        "status": "PROCESSING",
        "amount": 1599,
    },
}


def get_order(
    order_id: str,
) -> dict[str, Any]:

    order = ORDERS.get(order_id)

    if not order:
        return {
            "success": False,
            "error": "ORDER_NOT_FOUND",
        }

    return {
        "success": True,
        "data": order,
    }