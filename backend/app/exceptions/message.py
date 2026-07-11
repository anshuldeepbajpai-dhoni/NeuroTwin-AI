class MessageNotFoundException(Exception):
    """
    Raised when a Message does not exist
    or does not belong to the authenticated user.
    """

    def __init__(
        self,
        message: str = "Message not found.",
    ):
        self.message = message

        super().__init__(
            self.message
        )


class InvalidMessageRoleException(Exception):
    """
    Raised when a normal user attempts to create
    an assistant or system Message.
    """

    def __init__(
        self,
        message: str = (
            "Users can create only user messages."
        ),
    ):
        self.message = message

        super().__init__(
            self.message
        )