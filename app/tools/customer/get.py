def get_customer(customer_id: str) -> dict:
    customers = {
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

    customer = customers.get(customer_id)

    if not customer:
        return {
            "success": False,
            "error": "CUSTOMER_NOT_FOUND",
        }

    return {
        "success": True,
        "data": customer,
    }