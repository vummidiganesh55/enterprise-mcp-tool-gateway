import streamlit as st

from evaluation.evaluator import security_evaluator
from evaluation.metrics import calculate_evaluation_metrics


st.set_page_config(
    page_title="Security",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ Security Evaluation")
st.caption("MCP tool security and threat detection")


# --------------------------------------------------
# Run Security Evaluation
# --------------------------------------------------

if st.button(
    "Run Security Evaluation",
    type="primary",
):

    with st.spinner(
        "Running security evaluation..."
    ):
        results = security_evaluator.evaluate_all()

        metrics = calculate_evaluation_metrics(
            results
        )

    st.session_state[
        "security_results"
    ] = results

    st.session_state[
        "security_metrics"
    ] = metrics

    st.success(
        "Security evaluation completed."
    )


# --------------------------------------------------
# Load Results
# --------------------------------------------------

results = st.session_state.get(
    "security_results"
)

metrics = st.session_state.get(
    "security_metrics"
)


if not results or not metrics:

    st.info(
        "Click **Run Security Evaluation** "
        "to execute the security benchmark."
    )

    st.stop()


# --------------------------------------------------
# Summary
# --------------------------------------------------

st.subheader("Evaluation Summary")

total_cases = metrics.get(
    "total_cases",
    len(results),
)

passed_cases = metrics.get(
    "passed_cases",
    0,
)

failed_cases = metrics.get(
    "failed_cases",
    total_cases - passed_cases,
)

accuracy = metrics.get(
    "accuracy",
    0.0,
)


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Cases",
        total_cases,
    )


with col2:
    st.metric(
        "Passed",
        passed_cases,
    )


with col3:
    st.metric(
        "Failed",
        failed_cases,
    )


with col4:
    st.metric(
        "Accuracy",
        f"{accuracy * 100:.1f}%",
    )


# --------------------------------------------------
# Detection / Risk Accuracy
# --------------------------------------------------

st.subheader("Security Metrics")


col1, col2 = st.columns(2)


with col1:

    detection_accuracy = metrics.get(
        "detection_accuracy",
        0.0,
    )

    st.metric(
        "Detection Accuracy",
        f"{detection_accuracy * 100:.1f}%",
    )


with col2:

    risk_accuracy = metrics.get(
        "risk_accuracy",
        0.0,
    )

    st.metric(
        "Risk Accuracy",
        f"{risk_accuracy * 100:.1f}%",
    )


# --------------------------------------------------
# Category Accuracy
# --------------------------------------------------

st.subheader("Category Accuracy")


category_accuracy = metrics.get(
    "category_accuracy",
    {},
)


for category, value in category_accuracy.items():

    label = category.replace(
        "_",
        " ",
    ).title()

    st.write(
        f"**{label}**"
    )

    st.progress(
        float(value),
        text=f"{value * 100:.1f}%",
    )


# --------------------------------------------------
# Failed Cases
# --------------------------------------------------

st.subheader("Failed Security Cases")


failed_results = [
    result
    for result in results
    if not result.get(
        "passed",
        False,
    )
]


if failed_results:

    st.dataframe(
        failed_results,
        use_container_width=True,
    )

else:

    st.success(
        "No failed security cases."
    )


# --------------------------------------------------
# All Results
# --------------------------------------------------

with st.expander(
    "View All Evaluation Results"
):

    st.dataframe(
        results,
        use_container_width=True,
    )