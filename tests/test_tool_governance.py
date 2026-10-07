from app.idempotency.manager import IdempotencyManager


def test_customer_update_idempotency():
    manager = IdempotencyManager()

    calls = {"count": 0}

    def update_customer():
        calls["count"] += 1
        return {
            "success": True,
            "customer_id": "C001",
            "status": "active",
        }

    first_result = manager.execute(
        "customer-update-test-001",
        update_customer,
    )

    second_result = manager.execute(
        "customer-update-test-001",
        update_customer,
    )

    assert first_result == second_result
    assert calls["count"] == 1


def test_ticket_create_idempotency():
    manager = IdempotencyManager()

    calls = {"count": 0}

    def create_ticket():
        calls["count"] += 1
        return {
            "success": True,
            "ticket_id": "T001",
        }

    first_result = manager.execute(
        "ticket-create-test-001",
        create_ticket,
    )

    second_result = manager.execute(
        "ticket-create-test-001",
        create_ticket,
    )

    assert first_result == second_result
    assert calls["count"] == 1


def test_customer_delete_idempotency():
    manager = IdempotencyManager()

    calls = {"count": 0}

    def delete_customer():
        calls["count"] += 1
        return {
            "success": True,
            "customer_id": "C001",
        }

    first_result = manager.execute(
        "customer-delete-test-001",
        delete_customer,
    )

    second_result = manager.execute(
        "customer-delete-test-001",
        delete_customer,
    )

    assert first_result == second_result
    assert calls["count"] == 1