class EntityNotFound(Exception):
    """Raises when an entity is not found in the database."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.code = 1000


class UniqueViolation(Exception):
    """Raises when unique violation is detected."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.code = 1001


class DeletionError(Exception):
    """Raises when error occurs during entity deletion from database."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.code = 1002


class EntityAlreadyExist(Exception):
    """Raises when saving already existing entity."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.code = 1003
