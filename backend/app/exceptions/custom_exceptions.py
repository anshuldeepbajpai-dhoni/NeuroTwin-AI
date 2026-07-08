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