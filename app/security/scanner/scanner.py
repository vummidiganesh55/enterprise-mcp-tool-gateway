from typing import Any

from app.security.scanner.prompt_injection import (
    detect_prompt_injection,
)
from app.security.scanner.tool_poisoning import (
    detect_tool_poisoning,
)
from app.security.scanner.authorization_bypass import (
    detect_authorization_bypass,
)
from app.security.scanner.data_exposure import (
    detect_data_exposure,
)
from app.security.scanner.malicious_tool_definition import (
    detect_malicious_tool_definition,
)


class SecurityScanner:

    # ---------------------------------------------------------
    # Individual scanner APIs
    # Used by the existing SecurityEvaluator
    # ---------------------------------------------------------

    def scan_prompt(
        self,
        text: str,
    ) -> dict[str, Any]:
        return detect_prompt_injection(text)

    def scan_tool(
        self,
        tool_metadata: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "tool_poisoning": detect_tool_poisoning(
                tool_metadata
            ),
            "malicious_definition": (
                detect_malicious_tool_definition(
                    tool_metadata
                )
            ),
        }

    def scan_authorization(
        self,
        *,
        role: str,
        tool_name: str,
        authorized: bool,
        requested_role: str | None = None,
    ) -> dict[str, Any]:
        return detect_authorization_bypass(
            role=role,
            tool_name=tool_name,
            authorized=authorized,
            requested_role=requested_role,
        )

    def scan_data(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        return detect_data_exposure(data)

    def scan_tool_definition(
        self,
        tool_metadata: dict[str, Any],
    ) -> dict[str, Any]:
        return detect_malicious_tool_definition(
            tool_metadata
        )

    # ---------------------------------------------------------
    # Unified Security Scanner
    # Used by dashboard / future gateway integration
    # ---------------------------------------------------------

    def scan(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:

        # -----------------------------
        # Extract common payload fields
        # -----------------------------

        text = str(
            payload.get(
                "query",
                payload.get("text", ""),
            )
        )

        role = str(
            payload.get(
                "role",
                "",
            )
        )

        tool_name = str(
            payload.get(
                "tool_name",
                "",
            )
        )

        authorized = bool(
            payload.get(
                "authorized",
                True,
            )
        )

        requested_role = payload.get(
            "requested_role"
        )

        # -----------------------------
        # Tool metadata
        # -----------------------------

        tool_metadata = payload.get(
            "tool_metadata",
            {
                "name": tool_name,
                "description": payload.get(
                    "description",
                    "",
                ),
            },
        )

        # -----------------------------
        # Data to scan
        # -----------------------------

        data = payload.get(
            "data",
            payload,
        )

        # -----------------------------
        # Run all security scanners
        # -----------------------------

        results = {
            "prompt_injection": detect_prompt_injection(
                text
            ),

            "tool_poisoning": detect_tool_poisoning(
                tool_metadata
            ),

            "authorization_bypass": (
                detect_authorization_bypass(
                    role=role,
                    tool_name=tool_name,
                    authorized=authorized,
                    requested_role=requested_role,
                )
            ),

            "data_exposure": detect_data_exposure(
                data
            ),

            "malicious_tool_definition": (
                detect_malicious_tool_definition(
                    tool_metadata
                )
            ),
        }

        # -----------------------------
        # Determine detected threats
        # -----------------------------

        detected_threats = [
            name
            for name, result in results.items()
            if result.get(
                "detected",
                False,
            )
        ]

        # -----------------------------
        # Unified result
        # -----------------------------

        return {
            "safe": len(detected_threats) == 0,
            "detected_count": len(
                detected_threats
            ),
            "detected_threats": detected_threats,
            "results": results,
        }


# Global scanner instance

security_scanner = SecurityScanner()