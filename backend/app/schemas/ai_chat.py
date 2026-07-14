from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from app.schemas.message import (
    MessageResponse,
)


class AIChatRequest(BaseModel):
    """
    Request schema for sending a message
    to the user's Digital Twin.
    """

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description=(
            "Message sent by the user "
            "to the Digital Twin."
        ),
        json_schema_extra={
            "example": (
                "Create a practical roadmap "
                "for learning machine learning."
            )
        },
    )

    @field_validator(
        "message"
    )
    @classmethod
    def validate_message(
        cls,
        value: str,
    ) -> str:
        """
        Remove surrounding whitespace and
        reject whitespace-only messages.
        """

        clean_value = value.strip()

        if not clean_value:
            raise ValueError(
                "Message cannot contain "
                "only whitespace."
            )

        return clean_value


class AIChatResponse(BaseModel):
    """
    Response containing the saved user
    and assistant messages.
    """

    user_message: MessageResponse

    assistant_message: MessageResponse

    model_config = ConfigDict(
        from_attributes=True
    )