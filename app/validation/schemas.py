from pydantic import BaseModel, Field


class CustomerRequest(BaseModel):
    customer_id: str = Field(
        min_length=1,
        max_length=50
    )


class ToolRequest(BaseModel):
    tool_name: str = Field(
        min_length=1,
        max_length=100
    )
    arguments: dict = Field(
        default_factory=dict
    )