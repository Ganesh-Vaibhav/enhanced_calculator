"""
Custom exceptions for the calculator application.
"""


class CalculatorError(Exception):
    """Base exception for calculator-related errors."""
    pass


class OperationError(CalculatorError):
    """Raised when an operation cannot be performed."""
    pass


class ValidationError(CalculatorError):
    """Raised when input validation fails."""
    pass


class HistoryError(CalculatorError):
    """Raised when history operations fail."""
    pass


class ConfigurationError(CalculatorError):
    """Raised when configuration is invalid."""
    pass

