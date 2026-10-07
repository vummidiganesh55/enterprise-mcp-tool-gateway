from collections import defaultdict
from typing import Any


def calculate_evaluation_metrics(
    results: list[dict[str, Any]],
) -> dict[str, Any]:

    total = len(results)

    if total == 0:
        return {
            "total_cases": 0,
            "passed_cases": 0,
            "failed_cases": 0,
            "accuracy": 0.0,
            "detection_accuracy": 0.0,
            "risk_accuracy": 0.0,
            "category_accuracy": {},
        }

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    detection_correct = sum(
        1
        for result in results
        if (
            result["expected_detected"]
            == result["actual_detected"]
        )
    )

    risk_correct = sum(
        1
        for result in results
        if (
            result["expected_risk"]
            == result["actual_risk"]
        )
    )

    category_results = defaultdict(list)

    for result in results:
        category_results[
            result["category"]
        ].append(result)

    category_accuracy = {}

    for category, cases in category_results.items():

        category_passed = sum(
            1
            for case in cases
            if case["passed"]
        )

        category_accuracy[category] = (
            category_passed / len(cases)
        )

    return {
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": total - passed,
        "accuracy": passed / total,
        "detection_accuracy": (
            detection_correct / total
        ),
        "risk_accuracy": (
            risk_correct / total
        ),
        "category_accuracy": category_accuracy,
    }