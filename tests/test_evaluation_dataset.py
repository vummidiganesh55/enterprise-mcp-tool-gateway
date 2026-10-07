from evaluation.datasets.security_cases import (
    SECURITY_EVALUATION_CASES,
)


def test_evaluation_dataset_exists():

    assert len(SECURITY_EVALUATION_CASES) == 100


def test_evaluation_cases_have_required_fields():

    required_fields = {
        "id",
        "category",
        "expected_detected",
        "expected_risk",
    }

    for case in SECURITY_EVALUATION_CASES:
        assert required_fields.issubset(
            case.keys()
        )


def test_all_security_categories_present():

    categories = {
        case["category"]
        for case in SECURITY_EVALUATION_CASES
    }

    expected_categories = {
        "prompt_injection",
        "tool_poisoning",
        "authorization_bypass",
        "data_exposure",
        "malicious_tool_definition",
    }

    assert categories == expected_categories