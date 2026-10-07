from pathlib import Path
from typing import Any

import yaml


class PolicyLoader:
    def __init__(self, policy_file: str | None = None):
        if policy_file is None:
            policy_file = str(
                Path(__file__).parent / "policies.yaml"
            )

        self.policy_file = Path(policy_file)

    def load(self) -> list[dict[str, Any]]:
        if not self.policy_file.exists():
            raise FileNotFoundError(
                f"Policy file not found: {self.policy_file}"
            )

        with self.policy_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = yaml.safe_load(file) or {}

        policies = data.get("policies", [])

        if not isinstance(policies, list):
            raise ValueError(
                "'policies' must be a list"
            )

        return policies


policy_loader = PolicyLoader()