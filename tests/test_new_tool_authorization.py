from app.security.authorization.rbac import check_permission


# ============================================================
# CUSTOMER
# ============================================================

def test_viewer_cannot_update_customer():
    assert check_permission(
        "viewer",
        "customer_update",
    ) is False


def test_support_can_update_customer():
    assert check_permission(
        "support",
        "customer_update",
    ) is True


def test_admin_can_update_customer():
    assert check_permission(
        "admin",
        "customer_update",
    ) is True


def test_viewer_cannot_delete_customer():
    assert check_permission(
        "viewer",
        "customer_delete",
    ) is False


def test_support_cannot_delete_customer():
    assert check_permission(
        "support",
        "customer_delete",
    ) is False


def test_admin_can_delete_customer():
    assert check_permission(
        "admin",
        "customer_delete",
    ) is True


# ============================================================
# TICKET
# ============================================================

def test_viewer_can_get_ticket():
    assert check_permission(
        "viewer",
        "ticket_get",
    ) is True


def test_support_can_create_ticket():
    assert check_permission(
        "support",
        "ticket_create",
    ) is True


def test_viewer_cannot_create_ticket():
    assert check_permission(
        "viewer",
        "ticket_create",
    ) is False


# ============================================================
# ORDER
# ============================================================

def test_support_can_get_order():
    assert check_permission(
        "support",
        "order_get",
    ) is True


def test_viewer_can_get_order_status():
    assert check_permission(
        "viewer",
        "order_status",
    ) is True


# ============================================================
# AUDIT
# ============================================================

def test_support_cannot_search_audit():
    assert check_permission(
        "support",
        "audit_search",
    ) is False


def test_admin_can_search_audit():
    assert check_permission(
        "admin",
        "audit_search",
    ) is True


# ============================================================
# UNKNOWN ROLE
# ============================================================

def test_unknown_role_is_denied():
    assert check_permission(
        "unknown_role",
        "customer_get",
    ) is False