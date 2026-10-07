from evaluation.metrics import (
    calculate_evaluation_metrics,
)


def test_evaluation_metrics():

    results = [
        {
            "id": "SEC001",
            "category": "prompt_injection",
            "expected_detected": True,
            "actual_detected": True,
            "expected_risk": "HIGH",
            "actual_risk": "HIGH",
            "passed": True,
        },
        {
            "id": "SEC002",
            "category": "prompt_injection",
            "expected_detected": False,
            "actual_detected": False,
            "expected_risk": "LOW",
            "actual_risk": "LOW",
            "passed": True,
        },
        {
            "id": "SEC003",
            "category": "data_exposure",
            "expected_detected": True,
            "actual_detected": False,
            "expected_risk": "HIGH",
            "actual_risk": "LOW",
            "passed": False,
        },
    ]

    metrics = calculate_evaluation_metrics(
        results
    )

    assert metrics["total_cases"] == 3
    assert metrics["passed_cases"] == 2
    assert metrics["failed_cases"] == 1

    assert metrics["accuracy"] == 2 / 3
    assert metrics["detection_accuracy"] == 2 / 3
    assert metrics["risk_accuracy"] == 2 / 3

    assert (
        metrics["category_accuracy"][
            "prompt_injection"
        ]
        == 1.0
    )

    assert (
        metrics["category_accuracy"][
            "data_exposure"
        ]
        == 0.0
    )


def test_empty_results():

    metrics = calculate_evaluation_metrics([])

    assert metrics["total_cases"] == 0
    assert metrics["accuracy"] == 0.0