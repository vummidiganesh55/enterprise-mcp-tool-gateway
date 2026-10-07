from mcp.server.mcpserver import MCPServer
import asyncio
from app.tools.customer.get import get_customer
from app.tools.customer.update import update_customer
from app.tools.customer.delete import delete_customer

from app.tools.knowledge.search import search_knowledge
from app.tools.knowledge.retrieve import retrieve_document

from app.tools.ticket.get import get_ticket
from app.tools.ticket.create import create_ticket

from app.tools.order.get import get_order
from app.tools.order.status import get_order_status

from app.tools.governance.audit_search import search_audit_events

from app.mcp_gateway.registry import ToolMetadata, tool_registry

from app.security.governance.executor import governance_executor


# ============================================================
# MCP SERVER
# ============================================================

mcp = MCPServer("enterprise-mcp-gateway")


# ============================================================
# HEALTH CHECK
# ============================================================

@mcp.tool()
def health_check() -> dict:
    return {
        "status": "healthy",
        "service": "enterprise-mcp-gateway",
    }


# ============================================================
# CUSTOMER GET
# ============================================================

@mcp.tool()
def customer_get(customer_id: str) -> dict:
    return get_customer(customer_id)


# ============================================================
# CUSTOMER UPDATE
# ============================================================

@mcp.tool()
def customer_update(
    customer_id: str,
    name: str | None = None,
    status: str | None = None,
) -> dict:
    return update_customer(
        customer_id=customer_id,
        name=name,
        status=status,
    )


# ============================================================
# CUSTOMER DELETE — GOVERNED HIGH-RISK TOOL
# ============================================================

@mcp.tool()
def customer_delete(
    customer_id: str,
    user_id: str = "anonymous",
    role: str = "viewer",
    request_id: str = "REQ-DEFAULT",
    idempotency_key: str = "IDEMP-DEFAULT",
) -> dict:
    """
    Delete a customer through the governance layer.

    Governance:
    - RBAC authorization
    - HIGH risk classification
    - Human approval
    - Idempotency
    - Audit logging
    """

    return governance_executor.execute(
        user_id=user_id,
        role=role,
        tool_name="customer_delete",
        risk_level="HIGH",
        request_id=request_id,
        idempotency_key=idempotency_key,
        function=delete_customer,
        kwargs={
            "customer_id": customer_id,
        },
    )


# ============================================================
# KNOWLEDGE SEARCH
# ============================================================

@mcp.tool()
def knowledge_search(query: str) -> dict:
    return search_knowledge(query)


# ============================================================
# KNOWLEDGE RETRIEVE
# ============================================================

@mcp.tool()
def knowledge_retrieve(document_id: str) -> dict:
    return retrieve_document(document_id)


# ============================================================
# TICKET GET
# ============================================================

@mcp.tool()
def ticket_get(ticket_id: str) -> dict:
    return get_ticket(ticket_id)


# ============================================================
# TICKET CREATE
# ============================================================

@mcp.tool()
def ticket_create(
    customer_id: str,
    subject: str,
    priority: str,
) -> dict:
    return create_ticket(
        customer_id=customer_id,
        subject=subject,
        priority=priority,
    )


# ============================================================
# ORDER GET
# ============================================================

@mcp.tool()
def order_get(order_id: str) -> dict:
    return get_order(order_id)


# ============================================================
# ORDER STATUS
# ============================================================

@mcp.tool()
def order_status(order_id: str) -> dict:
    return get_order_status(order_id)


# ============================================================
# AUDIT SEARCH
# ============================================================

@mcp.tool()
def audit_search(
    tool_name: str | None = None,
    user_id: str | None = None,
    success: bool | None = None,
) -> dict:
    return search_audit_events(
        tool_name=tool_name,
        user_id=user_id,
        success=success,
    )


# ============================================================
# TOOL REGISTRY
# ============================================================

tool_registry.register(
    ToolMetadata(
        name="health_check",
        version="1.0.0",
        description="Check MCP gateway health",
        function=health_check,
        risk_level="LOW",
    )
)

tool_registry.register(
    ToolMetadata(
        name="customer_get",
        version="1.0.0",
        description="Retrieve customer information",
        function=customer_get,
        risk_level="LOW",
    )
)

tool_registry.register(
    ToolMetadata(
        name="customer_update",
        version="1.0.0",
        description="Update customer information",
        function=customer_update,
        risk_level="MEDIUM",
    )
)

tool_registry.register(
    ToolMetadata(
        name="customer_delete",
        version="1.0.0",
        description="Delete a customer",
        function=customer_delete,
        risk_level="HIGH",
    )
)

tool_registry.register(
    ToolMetadata(
        name="knowledge_search",
        version="1.0.0",
        description="Search enterprise knowledge",
        function=knowledge_search,
        risk_level="LOW",
    )
)

tool_registry.register(
    ToolMetadata(
        name="knowledge_retrieve",
        version="1.0.0",
        description="Retrieve an enterprise document",
        function=knowledge_retrieve,
        risk_level="LOW",
    )
)

tool_registry.register(
    ToolMetadata(
        name="ticket_get",
        version="1.0.0",
        description="Retrieve support ticket information",
        function=ticket_get,
        risk_level="LOW",
    )
)

tool_registry.register(
    ToolMetadata(
        name="ticket_create",
        version="1.0.0",
        description="Create a support ticket",
        function=ticket_create,
        risk_level="MEDIUM",
    )
)

tool_registry.register(
    ToolMetadata(
        name="order_get",
        version="1.0.0",
        description="Retrieve order information",
        function=order_get,
        risk_level="LOW",
    )
)

tool_registry.register(
    ToolMetadata(
        name="order_status",
        version="1.0.0",
        description="Retrieve order status",
        function=order_status,
        risk_level="LOW",
    )
)

tool_registry.register(
    ToolMetadata(
        name="audit_search",
        version="1.0.0",
        description="Search audit events",
        function=audit_search,
        risk_level="MEDIUM",
    )
)


# ============================================================
# STARTUP
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Enterprise MCP Tool Gateway")
    print("=" * 60)

    print("\nRegistered MCP Tools:")

    for tool in tool_registry.list_tools():
        print(
            f"- {tool.name} "
            f"| v{tool.version} "
            f"| risk={tool.risk_level}"
        )

    print(f"\nTotal tools: {len(tool_registry.list_tools())}")

    print("\nMCP endpoint:")
    print("http://127.0.0.1:8001/mcp")

    print("=" * 60)

    import asyncio

    asyncio.run(
        mcp.run_streamable_http_async(
            host="127.0.0.1",
            port=8001,
            streamable_http_path="/mcp",
        )
    )