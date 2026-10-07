import asyncio

from mcp import ClientSession

from app.mcp_client.connection import create_connection


async def main():
    async with create_connection() as (
        read_stream,
        write_stream,
    ):
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            # Initialize MCP session
            await session.initialize()

            print("\nConnected to MCP Gateway")

            # Discover tools
            result = await session.list_tools()

            print("\nAvailable MCP Tools:")

            for tool in result.tools:
                print(f"- {tool.name}")

            # Call health_check
            health = await session.call_tool(
                "health_check",
                {},
            )

            print("\nHealth Check:")
            print(health)

            # Call customer_get
            customer = await session.call_tool(
                "customer_get",
                {
                    "customer_id": "C001",
                },
            )

            print("\nCustomer:")
            print(customer)

            # Call knowledge_search
            knowledge_search = await session.call_tool(
                "knowledge_search",
                {
                    "query": "customer support",
                    "limit": 3,
                },
            )

            print("\nKnowledge Search:")
            print(knowledge_search)

            # Call knowledge_retrieve
            knowledge_document = await session.call_tool(
                "knowledge_retrieve",
                {
                    "document_id": "DOC002",
                },
            )

            print("\nKnowledge Retrieve:")
            print(knowledge_document)

            # Call customer_delete
            delete_result = await session.call_tool(
                "customer_delete",
                {
                    "customer_id": "C001",
                    "user_id": "U001",
                    "role": "admin",
                    "request_id": "REQ-MCP-DELETE-001",
                    "idempotency_key": "IDEMP-MCP-DELETE-001",
                },
            )

            print("\nCustomer Delete:")
            print(delete_result)


if __name__ == "__main__":
    asyncio.run(main())