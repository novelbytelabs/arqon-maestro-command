class FailClosedError(RuntimeError):
    """Raised when command flow must fail closed."""


class ContractValidationError(RuntimeError):
    """Raised when payload contract validation fails."""
