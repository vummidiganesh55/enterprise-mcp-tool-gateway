import streamlit as st

from evaluation.history import evaluation_history


st.set_page_config(
    page_title="Evaluation",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Evaluation Dashboard")
st.caption("Security evaluation and benchmark history")


# --------------------------------------------------
# Latest Run
# --------------------------------------------------

latest_run = evaluation_history.latest_run()

if latest_run is None:
    st.warning("No benchmark runs available.")
    st.stop()


st.subheader("Latest Benchmark Run")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Cases",
        latest_run.total_cases,
    )

with col2:
    st.metric(
        "Passed",
        latest_run.passed,
    )

with col3:
    st.metric(
        "Failed",
        latest_run.failed,
    )

with col4:
    st.metric(
        "Accuracy",
        f"{latest_run.accuracy * 100:.1f}%",
    )


# --------------------------------------------------
# Evaluation Metrics
# --------------------------------------------------

st.subheader("Evaluation Metrics")

metrics = latest_run.metrics

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

if category_accuracy:
    for category, accuracy in category_accuracy.items():
        st.write(
            f"**{category.replace('_', ' ').title()}**"
        )

        st.progress(
            float(accuracy),
            text=f"{accuracy * 100:.1f}%",
        )
else:
    st.info("No category accuracy data available.")


# --------------------------------------------------
# Benchmark History
# --------------------------------------------------

st.subheader("Benchmark History")

runs = evaluation_history.get_runs()

if runs:

    history_data = []

    for run in runs:
        history_data.append(
            {
                "Run ID": run.run_id,
                "Timestamp": run.timestamp,
                "Total Cases": run.total_cases,
                "Passed": run.passed,
                "Failed": run.failed,
                "Accuracy": f"{run.accuracy * 100:.1f}%",
            }
        )

    st.dataframe(
        history_data,
        use_container_width=True,
    )

else:
    st.info("No benchmark history available.")


# --------------------------------------------------
# Latest Run Details
# --------------------------------------------------

st.subheader("Latest Run Details")

st.write(
    f"**Run ID:** `{latest_run.run_id}`"
)

st.write(
    f"**Timestamp:** `{latest_run.timestamp}`"
)

with st.expander("View Evaluation Results"):

    st.json(
        latest_run.results
    )