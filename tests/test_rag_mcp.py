import asyncio

from app.mcp_client.client import MCPClient


async def main():
    client = MCPClient()

    await client.connect()

    result = await client.call_tool(
        "knowledge_retrieve",
        {"document_id": "DOC002"},
    )

    print("\n=== KNOWLEDGE RETRIEVE ===")
    print(result)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())