from pydantic import BaseModel, ValidationError


def validate_response(
    data: dict,
    response_model: type[BaseModel],
) -> dict:

    try:
        validated = response_model.model_validate(data)

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