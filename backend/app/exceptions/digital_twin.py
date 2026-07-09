class DigitalTwinAlreadyExistsException(Exception):
    """Raised when a user already has a Digital Twin."""


class DigitalTwinNotFoundException(Exception):
    """Raised when a Digital Twin does not exist."""


class EmptyUpdateException(Exception):
    """Raised when an update request contains no fields."""