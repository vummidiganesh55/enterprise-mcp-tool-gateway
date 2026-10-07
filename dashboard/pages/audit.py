import streamlit as st

from app.security.audit.audit_logger import AUDIT_EVENTS


st.set_page_config(
    page_title="Audit Logs",
    page_icon="📋",
    layout="wide",
)

st.title("📋 Audit Logs")
st.caption(
    "MCP gateway security, governance and tool execution audit trail"
)


# ============================================================
# SUMMARY
# ============================================================

st.subheader("Audit Summary")

total_events = len(AUDIT_EVENTS)

successful_events = sum(
    1
    for event in AUDIT_EVENTS
    if event.get("success") is True
)

failed_events = sum(
    1
    for event in AUDIT_EVENTS
    if event.get("success") is False
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Events",
        total_events,
    )

with col2:
    st.metric(
        "Successful",
        successful_events,
    )

with col3:
    st.metric(
        "Failed",
        failed_events,
    )


# ============================================================
# FILTERS
# ============================================================

st.subheader("Audit Filters")

tool_options = sorted(
    {
        event.get("tool_name", "")
        for event in AUDIT_EVENTS
        if event.get("tool_name")
    }
)

role_options = sorted(
    {
        event.get("role", "")
        for event in AUDIT_EVENTS
        if event.get("role")
    }
)

action_options = sorted(
    {
        event.get("action", "")
        for event in AUDIT_EVENTS
        if event.get("action")
    }
)


col1, col2, col3 = st.columns(3)

with col1:
    selected_tool = st.selectbox(
        "Tool",
        ["ALL"] + tool_options,
    )

with col2:
    selected_role = st.selectbox(
        "Role",
        ["ALL"] + role_options,
    )

with col3:
    selected_action = st.selectbox(
        "Action",
        ["ALL"] + action_options,
    )


success_filter = st.selectbox(
    "Result",
    [
        "ALL",
        "SUCCESS",
        "FAILED",
    ],
)


# ============================================================
# FILTER EVENTS
# ============================================================

filtered_events = []

for event in AUDIT_EVENTS:

    if (
        selected_tool != "ALL"
        and event.get("tool_name") != selected_tool
    ):
        continue

    if (
        selected_role != "ALL"
        and event.get("role") != selected_role
    ):
        continue

    if (
        selected_action != "ALL"
        and event.get("action") != selected_action
    ):
        continue

    if (
        success_filter == "SUCCESS"
        and event.get("success") is not True
    ):
        continue

    if (
        success_filter == "FAILED"
        and event.get("success") is not False
    ):
        continue

    filtered_events.append(event)


# ============================================================
# AUDIT TABLE
# ============================================================

st.subheader("Audit Events")

if not filtered_events:

    st.info(
        "No audit events match the selected filters."
    )

else:

    table_data = []

    for event in filtered_events:

        table_data.append(
            {
                "Timestamp": event.get(
                    "timestamp",
                    "",
                ),
                "User": event.get(
                    "user_id",
                    "",
                ),
                "Role": event.get(
                    "role",
                    "",
                ),
                "Tool": event.get(
                    "tool_name",
                    "",
                ),
                "Action": event.get(
                    "action",
                    "",
                ),
                "Success": event.get(
                    "success",
                    False,
                ),
                "Request ID": event.get(
                    "request_id",
                    "",
                ),
            }
        )

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# EVENT DETAILS
# ============================================================

st.subheader("Event Details")

if filtered_events:

    event_indices = list(
        range(len(filtered_events))
    )

    selected_index = st.selectbox(
        "Select Event",
        event_indices,
        format_func=lambda index: (
            f"{filtered_events[index].get('timestamp', '')} | "
            f"{filtered_events[index].get('tool_name', '')} | "
            f"{filtered_events[index].get('action', '')}"
        ),
    )

    selected_event = filtered_events[
        selected_index
    ]

    st.json(selected_event)


# ============================================================
# AUDIT FLOW
# ============================================================

st.subheader("Audit Flow")

st.code(
    """
MCP Tool Request
       |
       v
Authentication
       |
       v
Authorization / Policy
       |
       v
Risk / Approval
       |
       v
Tool Execution
       |
       v
Audit Event
       |
       +---- SUCCESS
       |
       +---- FAILURE
    """,
    language="text",
)