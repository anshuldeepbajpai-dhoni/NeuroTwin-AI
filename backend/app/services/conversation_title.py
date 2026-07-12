class ConversationTitleService:
    """
    Generate a short Conversation title
    from the user's first message.
    """

    MAX_TITLE_LENGTH = 80

    @classmethod
    def generate_title(
        cls,
        message: str,
    ) -> str:
        """
        Clean the message and convert it
        into a Conversation title.
        """

        clean_message = " ".join(
            message.strip().split()
        )

        if not clean_message:
            return "New Conversation"

        if (
            len(clean_message)
            <= cls.MAX_TITLE_LENGTH
        ):
            return clean_message

        shortened_title = (
            clean_message[
                :cls.MAX_TITLE_LENGTH
            ]
            .rstrip(
                " ,.;:-"
            )
        )

        return (
            f"{shortened_title}..."
        )


conversation_title_service = (
    ConversationTitleService()
)