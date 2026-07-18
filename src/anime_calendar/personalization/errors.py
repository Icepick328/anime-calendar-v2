class AuthenticationError(RuntimeError):
    """Raised when an access token cannot be validated."""


class PersistenceError(RuntimeError):
    """Raised when private persistence cannot complete safely."""


class ConfigurationError(RuntimeError):
    """Raised when required backend configuration is missing or invalid."""
