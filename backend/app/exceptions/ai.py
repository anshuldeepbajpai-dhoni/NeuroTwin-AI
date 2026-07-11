class AIConfigurationException(Exception):
    """
    Raised when the AI provider
    is not configured correctly.
    """

    def __init__(
        self,
        message: str = (
            "AI service is not configured."
        ),
    ):
        self.message = message

        super().__init__(
            self.message
        )


class AIAuthenticationException(Exception):
    """
    Raised when the AI provider
    rejects the configured API key.
    """

    def __init__(
        self,
        message: str = (
            "AI provider authentication failed."
        ),
    ):
        self.message = message

        super().__init__(
            self.message
        )


class AIQuotaExceededException(Exception):
    """
    Raised when AI API credits or
    quota are unavailable.
    """

    def __init__(
        self,
        message: str = (
            "AI service quota has been exceeded."
        ),
    ):
        self.message = message

        super().__init__(
            self.message
        )


class AIRateLimitException(Exception):
    """
    Raised when too many requests
    are sent to the AI provider.
    """

    def __init__(
        self,
        message: str = (
            "AI service rate limit exceeded. "
            "Please try again later."
        ),
    ):
        self.message = message

        super().__init__(
            self.message
        )


class AITimeoutException(Exception):
    """
    Raised when the AI provider
    does not respond within the timeout.
    """

    def __init__(
        self,
        message: str = (
            "AI service request timed out."
        ),
    ):
        self.message = message

        super().__init__(
            self.message
        )


class AIConnectionException(Exception):
    """
    Raised when the application cannot
    connect to the AI provider.
    """

    def __init__(
        self,
        message: str = (
            "Unable to connect to the "
            "AI service."
        ),
    ):
        self.message = message

        super().__init__(
            self.message
        )


class AIResponseException(Exception):
    """
    Raised when the AI provider returns
    an invalid or empty response.
    """

    def __init__(
        self,
        message: str = (
            "AI service returned an "
            "invalid response."
        ),
    ):
        self.message = message

        super().__init__(
            self.message
        )