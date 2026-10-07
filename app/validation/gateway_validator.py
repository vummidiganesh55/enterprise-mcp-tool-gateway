from typing import Any

from pydantic import BaseModel, ValidationError

from app.validation.response_validator import validate_response


class GatewayValidator:
    """Central validation adapter for the MCP gateway."""

    def __init__(self) -> None:
        self.request_schemas: dict[str, type[BaseModel]] = {}
        self.response_schemas: dict[str, type[BaseModel]] = {}

    # ================================================================
    # REQUEST SCHEMAS
    # ================================================================

    def register_request_schema(
        self,
        tool_name: str,
        schema: type[BaseModel],
    ) -> None:
        self.request_schemas[tool_name] = schema

    # ================================================================
    # RESPONSE SCHEMAS
    # ================================================================

    def register_response_schema(
        self,
        tool_name: str,
        schema: type[BaseModel],
    ) -> None:
        self.response_schemas[tool_name] = schema

    # ================================================================
    # REQUEST VALIDATION
    # ================================================================

    def validate_request(
        self,
        *,
        tool_name: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:

        schema = self.request_schemas.get(tool_name)

        # No schema registered.
        if schema is None:
            return {
                "valid": True,
                "data": data,
                "error": None,
            }

        try:
            validated = schema.model_validate(data)

            return {
                "valid": True,
                "data": validated.model_dump(),
                "error": None,
            }

        except ValidationError as exc:
            return {
                "valid": False,
                "data": None,
                "error": exc.errors(),
            }

    # ================================================================
    # RESPONSE VALIDATION
    # ================================================================

    def validate_response(
        self,
        *,
        data: dict[str, Any],
        response_model: type[BaseModel] | None = None,
        tool_name: str | None = None,
    ) -> dict[str, Any]:

        # ------------------------------------------------------------
        # Direct validation using an explicitly supplied model.
        #
        # Preserves the original API used by existing tests.
        # ------------------------------------------------------------

        if response_model is not None:

            return validate_response(
                data,
                response_model,
            )

        # ------------------------------------------------------------
        # Gateway validation using a registered tool schema.
        # ------------------------------------------------------------

        if tool_name is not None:

            schema = self.response_schemas.get(tool_name)

            # No response schema registered.
            if schema is None:
                return {
                    "valid": True,
                    "data": data,
                    "error": None,
                }

            try:

                validated = schema.model_validate(data)

                return {
                    "valid": True,
                    "data": validated.model_dump(),
                    "error": None,
                }

            except ValidationError as exc:

                return {
                    "valid": False,
                    "data": None,
                    "error": exc.errors(),
                }

        # ------------------------------------------------------------
        # No model and no tool schema.
        # Preserve pass-through behavior.
        # ------------------------------------------------------------

        return {
            "valid": True,
            "data": data,
            "error": None,
        }


gateway_validator = GatewayValidator()