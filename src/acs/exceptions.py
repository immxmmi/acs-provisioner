"""ACS-specific exceptions."""


class AcsError(Exception):
    """Base exception for ACS operations."""
    pass


class AcsAuthError(AcsError):
    """Authentication error with ACS API."""
    pass


class AcsNotFoundError(AcsError):
    """Resource not found in ACS."""
    pass


class AcsConflictError(AcsError):
    """Resource already exists in ACS."""
    pass


class AcsValidationError(AcsError):
    """Validation error for ACS resources."""
    pass
