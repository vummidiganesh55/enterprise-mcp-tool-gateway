from sqlalchemy.orm import Session

from app.database.models import Customer


def get_customer(
    db: Session,
    customer_id: str,
):
    return (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )


def create_customer(
    db: Session,
    customer_id: str,
    name: str,
    status: str,
):
    customer = Customer(
        customer_id=customer_id,
        name=name,
        status=status,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer