import streamlit as st

from app.security.approval.manager import approval_manager


st.set_page_config(
    page_title="Approvals",
    page_icon="✅",
    layout="wide",
)

st.title("✅ Approval Management")
st.caption(
    "Human approval workflow for high-risk MCP tool operations"
)


# ============================================================
# CREATE TEST APPROVAL
# ============================================================

st.subheader("Create Approval Request")

col1, col2 = st.columns(2)

with col1:
    request_id = st.text_input(
        "Request ID",
        value="REQ-DASHBOARD-001",
    )

    user_id = st.text_input(
        "User ID",
        value="U001",
    )

with col2:
    tool_name = st.text_input(
        "Tool Name",
        value="customer_delete",
    )

    reason = st.text_input(
        "Reason",
        value="High-risk customer deletion",
    )


if st.button(
    "Create Approval Request",
    type="primary",
):

    approval = approval_manager.create_request(
        request_id=request_id,
        user_id=user_id,
        tool_name=tool_name,
        reason=reason,
    )

    st.success(
        f"Approval request `{approval.request_id}` created."
    )


# ============================================================
# PENDING / APPROVAL REQUESTS
# ============================================================

st.subheader("Approval Requests")

requests = list(
    approval_manager._requests.values()
)


if not requests:

    st.info(
        "No approval requests available."
    )

else:

    request_rows = []

    for request in requests:

        created_at = (
            request.created_at.isoformat()
            if request.created_at
            else ""
        )

        request_rows.append(
            {
                "Request ID": request.request_id,
                "User ID": request.user_id,
                "Tool": request.tool_name,
                "Reason": request.reason,
                "Status": request.status,
                "Created At": created_at,
            }
        )

    st.dataframe(
        request_rows,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# SUMMARY
# ============================================================

st.subheader("Approval Summary")

pending_count = sum(
    1
    for request in requests
    if request.status == "PENDING"
)

approved_count = sum(
    1
    for request in requests
    if request.status == "APPROVED"
)

denied_count = sum(
    1
    for request in requests
    if request.status == "DENIED"
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Pending",
        pending_count,
    )

with col2:
    st.metric(
        "Approved",
        approved_count,
    )

with col3:
    st.metric(
        "Denied",
        denied_count,
    )


# ============================================================
# APPROVE / DENY
# ============================================================

st.subheader("Process Approval")

if requests:

    request_ids = [
        request.request_id
        for request in requests
    ]

    selected_request_id = st.selectbox(
        "Select Request",
        request_ids,
    )

    selected_request = approval_manager.get(
        selected_request_id
    )

    st.write(
        f"**Tool:** `{selected_request.tool_name}`"
    )

    st.write(
        f"**User:** `{selected_request.user_id}`"
    )

    st.write(
        f"**Reason:** {selected_request.reason}"
    )

    st.write(
        f"**Current Status:** `{selected_request.status}`"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Approve",
            type="primary",
        ):

            approval_manager.approve(
                selected_request_id
            )

            st.success(
                f"`{selected_request_id}` approved."
            )

            st.rerun()

    with col2:

        if st.button("Deny"):

            approval_manager.deny(
                selected_request_id
            )

            st.warning(
                f"`{selected_request_id}` denied."
            )

            st.rerun()


# ============================================================
# GOVERNANCE FLOW
# ============================================================

st.subheader("High-Risk Approval Flow")

st.code(
    """
MCP Tool Request
       |
       v
Risk Classification
       |
       v
HIGH RISK
       |
       v
Approval Manager
       |
       +---- PENDING ----> Human Review
       |                       |
       |                       v
       |                 APPROVE / DENY
       |
       +---- APPROVED ----> Tool Execution
       |
       +---- DENIED ------> Request Rejected
    """,
    language="text",
)