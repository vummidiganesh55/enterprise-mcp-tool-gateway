from sqlalchemy.orm import Session

from app.repositories.customer_repository import (
    create_customer,
    get_customer,
)


def get_customer_service(
    db: Session,
    customer_id: str,
) -> dict:

    customer = get_customer(
        db,
        customer_id,
    )

    if customer is None:
        return {
            "success": False,
            "error": "CUSTOMER_NOT_FOUND",
        }

    return {
        "success": True,
        "data": {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "status": customer.status,
        },
    }


def create_customer_service(
    db: Session,
    customer_id: str,
    name: str,
    status: str = "active",
) -> dict:

    existing = get_customer(
        db,
        customer_id,
    )

    if existing:
        return {
            "success": False,
            "error": "CUSTOMER_ALREADY_EXISTS",
        }

    customer = create_customer(
        db,
        customer_id,
        name,
        status,
    )

    return {
        "success": True,
        "data": {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "status": customer.status,
        },
    }