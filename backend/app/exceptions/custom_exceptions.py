class UserAlreadyExistsException(Exception):
    def __init__(self, message: str):
        self.message = message


class InvalidCredentialsException(Exception):
    def __init__(self, message: str):
        self.message = message


class ForbiddenException(Exception):
    def __init__(self, message: str):
        self.message = message


class NotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message

class MemoryNotFoundException(Exception):
    """Raised when the requested memory does not exist."""

    pass


class EmptyMemoryUpdateException(Exception):
    """Raised when no fields are provided for a memory update."""

    pass