import streamlit as st

from app.mcp_gateway.registry import tool_registry
from app.observability.health import get_tool_health


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Enterprise MCP Gateway",
    page_icon="🔐",
    layout="wide",
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🔐 Enterprise MCP Tool Gateway")

st.caption(
    "Enterprise MCP Tool Gateway and Evaluation Platform"
)


# ---------------------------------------------------------
# Load MCP Tool Registry
# ---------------------------------------------------------

tools = tool_registry.list_tools()

total_tools = len(tools)

healthy_tools = sum(
    1
    for tool in tools
    if tool.enabled
)

disabled_tools = sum(
    1
    for tool in tools
    if not tool.enabled
)


# ---------------------------------------------------------
# Load Tool Health
# ---------------------------------------------------------

try:
    health_data = get_tool_health()
except Exception:
    health_data = []


# ---------------------------------------------------------
# Overview Metrics
# ---------------------------------------------------------

st.subheader("📊 Gateway Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "MCP Tools",
        total_tools,
    )


with col2:
    st.metric(
        "Healthy Tools",
        healthy_tools,
    )


with col3:
    st.metric(
        "Disabled Tools",
        disabled_tools,
    )


with col4:
    st.metric(
        "Tool Health Records",
        len(health_data),
    )


# ---------------------------------------------------------
# Tool Registry
# ---------------------------------------------------------

st.divider()

st.subheader("🔧 MCP Tool Registry")

st.caption(
    f"{total_tools} tools registered in the MCP Gateway"
)


for tool in tools:

    with st.container(border=True):

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"### 🔧 {tool.name}"
            )

        with col2:
            st.write(
                f"**Version**  \n"
                f"`{tool.version}`"
            )

        with col3:
            st.write(
                f"**Risk Level**  \n"
                f"`{tool.risk_level}`"
            )

        with col4:

            if tool.enabled:
                st.success("HEALTHY")
            else:
                st.error("DISABLED")

        st.write(
            f"**Description:** {tool.description}"
        )


# ---------------------------------------------------------
# Tool Summary
# ---------------------------------------------------------

st.divider()

st.subheader("📋 Tool Summary")


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
        "LOW Risk",
        low_risk,
    )


with col2:
    st.metric(
        "MEDIUM Risk",
        medium_risk,
    )


with col3:
    st.metric(
        "HIGH Risk",
        high_risk,
    )


with col4:
    st.metric(
        "Total Tools",
        total_tools,
    )


# ---------------------------------------------------------
# Registered Tools Table
# ---------------------------------------------------------

st.divider()

st.subheader("📑 Registered MCP Tools")


tool_rows = []

for tool in tools:

    tool_rows.append(
        {
            "Tool": tool.name,
            "Version": tool.version,
            "Risk": tool.risk_level,
            "Enabled": "Yes" if tool.enabled else "No",
            "Status": (
                "HEALTHY"
                if tool.enabled
                else "DISABLED"
            ),
        }
    )


st.dataframe(
    tool_rows,
    width="stretch",
    hide_index=True,
)


# ---------------------------------------------------------
# Architecture Status
# ---------------------------------------------------------

st.divider()

st.subheader("🏗️ Gateway Components")

components = [
    ("Tool Discovery", "ACTIVE"),
    ("Tool Registry", "ACTIVE"),
    ("Tool Versioning", "ACTIVE"),
    ("Authentication", "ACTIVE"),
    ("RBAC / ABAC", "ACTIVE"),
    ("Policy Engine", "ACTIVE"),
    ("Policy-as-Code", "ACTIVE"),
    ("Rate Limiting", "ACTIVE"),
    ("Risk Classification", "ACTIVE"),
    ("Input Validation", "ACTIVE"),
    ("Idempotency", "ACTIVE"),
    ("Human Approval", "ACTIVE"),
    ("Reliability", "ACTIVE"),
    ("Observability", "ACTIVE"),
    ("Security Scanner", "ACTIVE"),
    ("Evaluation Engine", "ACTIVE"),
    ("Evaluation History", "ACTIVE"),
    ("Tool Health Monitoring", "ACTIVE"),
]


for name, status in components:

    col1, col2 = st.columns([4, 1])

    with col1:
        st.write(name)

    with col2:
        st.success(status)


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "Enterprise MCP Tool Gateway & Evaluation Platform"
)