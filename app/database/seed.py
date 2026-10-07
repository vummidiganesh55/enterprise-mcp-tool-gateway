from app.database.connection import SessionLocal
from app.database.init_db import init_db
from app.services.customer_service import create_customer_service


def seed():
    init_db()

    db = SessionLocal()

    try:
        customers = [
            ("C001", "John Doe", "active"),
            ("C002", "Jane Smith", "active"),
        ]

        for customer_id, name, status in customers:
            result = create_customer_service(
                db,
                customer_id,
                name,
                status,
            )

            print(result)

    finally:
        db.close()


if __name__ == "__main__":
    seed()