import streamlit as st

from app.mcp_gateway import server
from app.observability.health import get_tool_health


st.title("❤️ Tool Health")

st.caption(
    "Real-time health status of registered MCP tools"
)

health = get_tool_health()

if not health:
    st.warning("No tools are currently registered.")
    st.stop()

healthy = sum(
    1
    for tool in health
    if tool["status"] == "HEALTHY"
)

disabled = len(health) - healthy

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Tools",
        len(health),
    )

with col2:
    st.metric(
        "Healthy",
        healthy,
    )

with col3:
    st.metric(
        "Disabled",
        disabled,
    )

st.divider()

for tool in health:

    status = tool["status"]

    if status == "HEALTHY":
        indicator = "🟢"
    else:
        indicator = "🔴"

    with st.container(border=True):

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write(
                f"{indicator} **{tool['tool_name']}**"
            )

        with col2:
            st.write(
                f"Version: `{tool['version']}`"
            )

        with col3:
            st.write(
                f"Risk: `{tool['risk_level']}`"
            )

        with col4:
            st.write(
                f"Status: `{status}`"
            )