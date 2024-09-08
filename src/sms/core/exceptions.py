class EntityNotFound(Exception):
    """Raises when an entity is not found in the database."""


class UniqueViolation(Exception):
    """Raises when unique violation is detected."""


class DeletionError(Exception):
    """Raises when error occurs during entity deletion from database."""


class EntityAlreadyExist(Exception):
    """Raises when saving already existing entity."""


class InvalidCredential(Exception):
    """Raises when invalid credentials are provided."""
