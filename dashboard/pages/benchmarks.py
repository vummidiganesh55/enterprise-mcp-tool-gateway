import streamlit as st

from evaluation.history import evaluation_history
from evaluation.benchmark import BenchmarkRunner


st.title("📈 Benchmark History")

st.caption(
    "Historical evaluation and benchmark runs"
)


runs = evaluation_history.get_runs()


# If no runs exist, create one benchmark run.
if not runs:

    st.info(
        "No benchmark runs found. "
        "Run the benchmark to create the first result."
    )

    if st.button("▶ Run Benchmark"):

        runner = BenchmarkRunner()

        run = runner.run()

        st.success(
            f"Benchmark completed: {run['run_id']}"
        )

        st.rerun()

    st.stop()


# Summary
latest = runs[-1]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Runs",
        len(runs),
    )

with col2:
    st.metric(
        "Latest Accuracy",
        f'{latest["accuracy"]:.1%}',
    )

with col3:
    st.metric(
        "Latest Passed",
        latest["passed"],
    )

with col4:
    st.metric(
        "Latest Failed",
        latest["failed"],
    )


st.divider()

st.subheader("Benchmark Runs")


for index, run in enumerate(
    reversed(runs),
    start=1,
):

    with st.container(border=True):

        st.markdown(
            f"### Run {len(runs) - index + 1}"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write(
                f"**Run ID**  \n`{run['run_id']}`"
            )

        with col2:
            st.write(
                f"**Accuracy**  \n"
                f"{run['accuracy']:.1%}"
            )

        with col3:
            st.write(
                f"**Passed / Failed**  \n"
                f"{run['passed']} / "
                f"{run['failed']}"
            )

        with col4:
            st.write(
                f"**Timestamp**  \n"
                f"{run['timestamp']}"
            )

        metrics = run["metrics"]

        detection_accuracy = metrics.get(
    "detection_accuracy",
    0.0,
    )

risk_accuracy = metrics.get(
    "risk_accuracy",
    0.0,
)

st.write(
    f"Detection Accuracy: "
    f"**{detection_accuracy:.1%}**"
)

st.write(
    f"Risk Accuracy: "
    f"**{risk_accuracy:.1%}**"
)

st.divider()

st.subheader("Run New Benchmark")

if st.button(
    "▶ Run Benchmark",
    type="primary",
):

    runner = BenchmarkRunner()

    run = runner.run()

    st.success(
        f"Benchmark completed successfully: "
        f"{run['run_id']}"
    )

    st.rerun()