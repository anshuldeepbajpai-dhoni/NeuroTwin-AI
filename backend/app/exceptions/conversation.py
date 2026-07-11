class ConversationNotFoundException(Exception):
    """Raised when a Conversation does not exist or is inaccessible."""

    def __init__(
        self,
        message: str = "Conversation not found.",
    ):
        self.message = message

        super().__init__(
            self.message
        )


class EmptyConversationUpdateException(Exception):
    """Raised when no fields are provided for a Conversation update."""

    def __init__(
        self,
        message: str = (
            "No fields provided for update."
        ),
    ):
        self.message = message

        super().__init__(
            self.message
        )