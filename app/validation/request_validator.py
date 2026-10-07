from pydantic import ValidationError

from app.validation.schemas import CustomerRequest


def validate_customer_request(data: dict) -> dict:
    try:
        request = CustomerRequest(**data)

        return {
            "valid": True,
            "data": request.model_dump(),
            "error": None,
        }

    except ValidationError as exc:
        return {
            "valid": False,
            "data": None,
            "error": exc.errors(),
        }