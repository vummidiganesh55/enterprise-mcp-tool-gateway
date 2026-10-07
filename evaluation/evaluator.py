from typing import Any

from evaluation.datasets.security_cases import (
    SECURITY_EVALUATION_CASES,
)

from app.security.scanner.scanner import (
    SecurityScanner,
)


class SecurityEvaluator:

    def __init__(self):
        self.scanner = SecurityScanner()

    def evaluate_case(
        self,
        case: dict[str, Any],
    ) -> dict[str, Any]:

        category = case["category"]

        if category == "prompt_injection":

            result = self.scanner.scan_prompt(
                case["input"]
            )

        elif category == "tool_poisoning":

            result = self.scanner.scan_tool(
                case["tool_metadata"]
            )

            result = result["tool_poisoning"]

        elif category == "authorization_bypass":

            result = self.scanner.scan_authorization(
                role=case["role"],
                tool_name=case["tool_name"],
                authorized=case["authorized"],
                requested_role=case.get(
                    "requested_role"
                ),
            )

        elif category == "data_exposure":

            result = self.scanner.scan_data(
                case["data"]
            )

        elif category == "malicious_tool_definition":

            result = self.scanner.scan_tool(
                case["tool_metadata"]
            )

            result = result["malicious_definition"]

        else:
            raise ValueError(
                f"Unsupported evaluation category: {category}"
            )

        detected_match = (
            result["detected"]
            == case["expected_detected"]
        )

        risk_match = (
            result["risk"]
            == case["expected_risk"]
        )

        return {
            "id": case["id"],
            "category": category,
            "expected_detected": case[
                "expected_detected"
            ],
            "actual_detected": result[
                "detected"
            ],
            "expected_risk": case[
                "expected_risk"
            ],
            "actual_risk": result[
                "risk"
            ],
            "passed": (
                detected_match
                and risk_match
            ),
        }

    def evaluate_all(
        self,
    ) -> list[dict[str, Any]]:

        return [
            self.evaluate_case(case)
            for case in SECURITY_EVALUATION_CASES
        ]


security_evaluator = SecurityEvaluator()