import streamlit as st

from app.reliability.circuit_breaker import CircuitBreaker
from app.reliability.executor import ReliabilityExecutor


st.set_page_config(
    page_title="Reliability",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ Reliability")
st.caption(
    "Retry, timeout, fallback and circuit-breaker controls"
)


# --------------------------------------------------
# Reliability Configuration
# --------------------------------------------------

st.subheader("Reliability Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Max Retry Attempts",
        3,
    )

with col2:
    st.metric(
        "Timeout",
        "5 seconds",
    )

with col3:
    st.metric(
        "Circuit Threshold",
        3,
    )


# --------------------------------------------------
# Reliability Components
# --------------------------------------------------

st.subheader("Reliability Components")

components = [
    {
        "Component": "Retry",
        "Status": "ACTIVE",
        "Description": "Retries failed tool executions",
    },
    {
        "Component": "Timeout",
        "Status": "ACTIVE",
        "Description": "Limits tool execution time",
    },
    {
        "Component": "Fallback",
        "Status": "ACTIVE",
        "Description": "Executes fallback when primary fails",
    },
    {
        "Component": "Circuit Breaker",
        "Status": "ACTIVE",
        "Description": "Prevents repeated calls to failing tools",
    },
]

st.dataframe(
    components,
    use_container_width=True,
    hide_index=True,
)


# --------------------------------------------------
# Circuit Breaker State
# --------------------------------------------------

st.subheader("Circuit Breaker")

circuit_breaker = CircuitBreaker()

state = circuit_breaker.state

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "State",
        state.state,
    )

with col2:
    st.metric(
        "Failure Count",
        state.failure_count,
    )

with col3:
    st.metric(
        "Failure Threshold",
        circuit_breaker.failure_threshold,
    )


# --------------------------------------------------
# Reliability Flow
# --------------------------------------------------

st.subheader("Execution Flow")

st.code(
    """
Tool Request
     |
     v
Circuit Breaker
     |
     v
Retry
     |
     v
Timeout
     |
     +------ Success ------> Result
     |
     +------ Failure
              |
              v
          Fallback
              |
              v
            Result
    """,
    language="text",
)


# --------------------------------------------------
# Reliability Notes
# --------------------------------------------------

st.subheader("Reliability Policies")

st.markdown(
    """
- **Retry:** Re-executes failed operations up to the configured limit.
- **Timeout:** Prevents indefinitely running tool executions.
- **Fallback:** Provides an alternate execution path when the primary fails.
- **Circuit Breaker:** Opens after repeated failures and prevents additional calls.
"""
)