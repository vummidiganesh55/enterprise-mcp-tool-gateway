import streamlit as st

from app.mcp_gateway.registry import tool_registry
from app.observability.metrics import (
    metrics_collector,
    measure_tool_execution,
)

from app.mcp_gateway.server import (
    health_check,
    customer_get,
    knowledge_search,
    knowledge_retrieve,
)


st.title("📊 Metrics")

st.caption(
    "MCP tool execution performance and reliability metrics"
)


# Run real tool executions and collect actual measurements
if st.button("▶ Run Metrics Probe", type="primary"):

    measure_tool_execution(
        "health_check",
        health_check,
    )

    measure_tool_execution(
        "customer_get",
        customer_get,
        "C001",
    )

    measure_tool_execution(
    "knowledge_search",
    knowledge_search,
    "customer support",
    )

    measure_tool_execution(
        "knowledge_retrieve",
        knowledge_retrieve,
        "DOC002",
    )

    st.success(
        "Metrics probe completed successfully."
    )


st.divider()

st.subheader("Tool Performance")


tools = tool_registry.list_tools()


for tool in tools:

    metrics = metrics_collector.get_metrics(
        tool.name
    )

    with st.container(border=True):

        st.markdown(
            f"### 🔧 {metrics['tool_name']}"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Requests",
                metrics["total_requests"],
            )

        with col2:
            st.metric(
                "Successful",
                metrics["successful_requests"],
            )

        with col3:
            st.metric(
                "Failed",
                metrics["failed_requests"],
            )

        with col4:
            st.metric(
                "Success Rate",
                f"{metrics['success_rate']:.1%}",
            )

        st.metric(
            "Average Latency",
            f"{metrics['average_latency_seconds']:.6f}s",
        )