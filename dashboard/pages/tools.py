import streamlit as st

# Import the MCP server module so that the registered
# ToolMetadata entries are loaded into tool_registry.
import app.mcp_gateway.server  # noqa: F401

from app.mcp_gateway.registry import tool_registry


st.set_page_config(
    page_title="Tool Catalog",
    page_icon="🧰",
    layout="wide",
)

st.title("🧰 MCP Tool Catalog")
st.caption(
    "Registered MCP tools, versions, risk classification and status"
)


# --------------------------------------------------
# Load Tools
# --------------------------------------------------

tools = tool_registry.list_tools()


if not tools:
    st.warning("No tools are registered.")
    st.stop()


# --------------------------------------------------
# Summary
# --------------------------------------------------

total_tools = len(tools)

enabled_tools = sum(
    1
    for tool in tools
    if tool.enabled
)

low_risk = sum(
    1
    for tool in tools
    if tool.risk_level == "LOW"
)

medium_risk = sum(
    1
    for tool in tools
    if tool.risk_level == "MEDIUM"
)

high_risk = sum(
    1
    for tool in tools
    if tool.risk_level == "HIGH"
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Tools",
        total_tools,
    )

with col2:
    st.metric(
        "Enabled",
        enabled_tools,
    )

with col3:
    st.metric(
        "Medium Risk",
        medium_risk,
    )

with col4:
    st.metric(
        "High Risk",
        high_risk,
    )


# --------------------------------------------------
# Risk Distribution
# --------------------------------------------------

st.subheader("Risk Distribution")

risk_data = {
    "Risk Level": [
        "LOW",
        "MEDIUM",
        "HIGH",
    ],
    "Tools": [
        low_risk,
        medium_risk,
        high_risk,
    ],
}

st.dataframe(
    risk_data,
    use_container_width=True,
    hide_index=True,
)


# --------------------------------------------------
# Tool Catalog
# --------------------------------------------------

st.subheader("Registered Tools")

tool_data = []

for tool in tools:

    tool_data.append(
        {
            "Tool": tool.name,
            "Version": tool.version,
            "Risk": tool.risk_level,
            "Status": (
                "ENABLED"
                if tool.enabled
                else "DISABLED"
            ),
            "Description": tool.description,
        }
    )


st.dataframe(
    tool_data,
    use_container_width=True,
    hide_index=True,
)


# --------------------------------------------------
# Tool Details
# --------------------------------------------------

st.subheader("Tool Details")

tool_names = [
    tool.name
    for tool in tools
]

selected_tool = st.selectbox(
    "Select a tool",
    tool_names,
)

selected = tool_registry.get(
    selected_tool
)


col1, col2 = st.columns(2)

with col1:

    st.write(
        f"**Name:** `{selected.name}`"
    )

    st.write(
        f"**Version:** `{selected.version}`"
    )

    st.write(
        f"**Risk Level:** `{selected.risk_level}`"
    )

with col2:

    st.write(
        f"**Enabled:** `{selected.enabled}`"
    )

    st.write(
        f"**Function:** `{selected.function.__name__}`"
    )

    st.write(
        f"**Description:** {selected.description}"
    )


# --------------------------------------------------
# Risk Explanation
# --------------------------------------------------

st.subheader("Risk Classification")

st.markdown(
    """
**LOW**
- Read-only or low-impact operations
- Normally allowed without approval

**MEDIUM**
- Operations that modify business data
- Subject to authorization and policy checks

**HIGH**
- Destructive or sensitive operations
- Requires additional governance such as human approval
"""
)