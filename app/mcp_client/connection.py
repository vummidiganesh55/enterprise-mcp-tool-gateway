from mcp.client.streamable_http import streamable_http_client


MCP_SERVER_URL = "http://127.0.0.1:8001/mcp"


def create_connection():
    return streamable_http_client(MCP_SERVER_URL)