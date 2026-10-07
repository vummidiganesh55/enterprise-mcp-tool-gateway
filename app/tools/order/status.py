from typing import Any


ORDER_STATUS = {
    "ORD001": "SHIPPED",
    "ORD002": "PROCESSING",
}


def get_order_status(
    order_id: str,
) -> dict[str, Any]:

    status = ORDER_STATUS.get(order_id)

    if status is None:
        return {
            "success": False,
            "error": "ORDER_NOT_FOUND",
        }

    return {
        "success": True,
        "order_id": order_id,
        "status": status,
    }