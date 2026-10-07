import streamlit as st

from app.security.policy.policy_engine import (
    PolicyContext,
    policy_engine,
)
from app.security.policy.policy_loader import (
    policy_loader,
)


st.set_page_config(
    page_title="Governance",
    page_icon="🔐",
    layout="wide",
)

st.title("🔐 Governance & Policy")
st.caption(
    "RBAC, Policy-as-Code and risk-based governance"
)


# ============================================================
# POLICY CATALOG
# ============================================================

st.subheader("Policy Catalog")

policies = policy_loader.load()

if not policies:
    st.warning("No policies configured.")
else:

    policy_rows = []

    for policy in policies:
        policy_rows.append(
            {
                "Policy": policy.get("name", ""),
                "Role": policy.get("role", ""),
                "Tool": policy.get("tool", "ALL"),
                "Risk": policy.get("risk", "ALL"),
                "Action": policy.get("action", ""),
            }
        )

    st.dataframe(
        policy_rows,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# POLICY SUMMARY
# ============================================================

st.subheader("Policy Summary")

total_policies = len(policies)

allow_policies = sum(
    1
    for policy in policies
    if policy.get("action") == "ALLOW"
)

approval_policies = sum(
    1
    for policy in policies
    if policy.get("action") == "REQUIRE_APPROVAL"
)

deny_policies = sum(
    1
    for policy in policies
    if policy.get("action") == "DENY"
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Policies",
        total_policies,
    )

with col2:
    st.metric(
        "ALLOW",
        allow_policies,
    )

with col3:
    st.metric(
        "REQUIRE APPROVAL",
        approval_policies,
    )

with col4:
    st.metric(
        "DENY",
        deny_policies,
    )


# ============================================================
# POLICY EVALUATOR
# ============================================================

st.subheader("Policy Evaluation")

st.write(
    "Test a policy decision using the active Policy Engine."
)


user_id = st.text_input(
    "User ID",
    value="U001",
)

role = st.selectbox(
    "Role",
    [
        "admin",
        "support",
        "viewer",
    ],
)

tool_names = sorted(
    {
        policy.get("tool")
        for policy in policies
        if policy.get("tool")
    }
)

tool_names = [
    tool
    for tool in tool_names
    if tool
]

if not tool_names:
    tool_names = [
        "health_check",
        "customer_get",
    ]

tool_name = st.selectbox(
    "Tool",
    tool_names,
)

risk_level = st.selectbox(
    "Risk Level",
    [
        "LOW",
        "MEDIUM",
        "HIGH",
    ],
)

customer_id = st.text_input(
    "Customer ID (optional)",
    value="",
)


if st.button(
    "Evaluate Policy",
    type="primary",
):

    context = PolicyContext(
        user_id=user_id,
        role=role,
        tool_name=tool_name,
        risk_level=risk_level,
        customer_id=(
            customer_id
            if customer_id
            else None
        ),
    )

    decision = policy_engine.evaluate(
        context
    )

    st.session_state[
        "policy_decision"
    ] = decision


# ============================================================
# POLICY DECISION
# ============================================================

decision = st.session_state.get(
    "policy_decision"
)

if decision is not None:

    st.subheader("Policy Decision")

    col1, col2 = st.columns(2)

    with col1:

        if decision.allowed:
            st.success("ALLOWED")
        else:
            st.error("DENIED")

    with col2:

        st.info(
            f"Reason: {decision.reason}"
        )


# ============================================================
# GOVERNANCE FLOW
# ============================================================

st.subheader("Governance Flow")

st.code(
    """
MCP Tool Request
       |
       v
Authentication
       |
       v
RBAC Authorization
       |
       v
Risk Classification
       |
       v
Policy Engine
       |
       +------ ALLOW ------------> Tool Execution
       |
       +------ DENY -------------> Request Rejected
       |
       +------ HIGH RISK --------> Approval Required
    """,
    language="text",
)


# ============================================================
# POLICY EXPLANATION
# ============================================================

st.subheader("Active Governance Rules")

st.markdown(
    """
- **Admin:** LOW and MEDIUM risk operations are allowed by the Policy Engine.
- **Admin + HIGH risk:** requires approval.
- **Support:** `customer_get` with LOW risk is allowed.
- **Viewer:** `health_check` with LOW risk is allowed.
- Other combinations are denied by the Policy Engine.
"""
)