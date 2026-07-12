from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    model_validator,
)


MemoryCategory = Literal[
    "goal",
    "preference",
    "interest",
    "skill",
    "education",
    "career",
    "project",
    "personal",
]


class MemoryExtractionResult(BaseModel):
    """
    Validate structured memory data
    extracted by an AI provider.
    """

    should_save: bool

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    content: str | None = Field(
        default=None,
        min_length=1,
    )

    category: MemoryCategory | None = None

    importance: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )

    @model_validator(
        mode="after"
    )
    def validate_memory_data(
        self,
    ):
        """
        Require complete memory information
        only when should_save is true.
        """

        if self.should_save:

            required_fields = [
                self.title,
                self.content,
                self.category,
                self.importance,
            ]

            if any(
                value is None
                for value in required_fields
            ):
                raise ValueError(
                    "Memory title, content, "
                    "category, and importance "
                    "are required when "
                    "should_save is true."
                )

        else:

            self.title = None
            self.content = None
            self.category = None
            self.importance = None

        return self