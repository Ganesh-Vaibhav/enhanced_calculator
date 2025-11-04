"""
Input validation utilities.
"""

from typing import Union, Tuple
from app.exceptions import ValidationError
from app.calculator_config import CalculatorConfig


class InputValidator:
    """Validates user inputs for calculator operations."""
    
    def __init__(self, config: CalculatorConfig):
        """Initialize validator with configuration."""
        self.config = config
    
    def validate_number(self, value: Union[str, float, int]) -> float:
        """Validate and convert a value to float."""
        try:
            number = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid number: {value}")
        
        max_value = self.config.get('CALCULATOR_MAX_INPUT_VALUE', float('inf'))
        if abs(number) > max_value:
            raise ValidationError(
                f"Number {number} exceeds maximum allowed value: {max_value}"
            )
        
        return number
    
    def validate_operation(self, operation: str) -> str:
        """Validate operation name."""
        if not isinstance(operation, str) or not operation.strip():
            raise ValidationError("Operation name cannot be empty")
        return operation.strip().lower()
    
    def validate_operands(self, operand1: Union[str, float, int], 
                         operand2: Union[str, float, int]) -> Tuple[float, float]:
        """Validate both operands."""
        return (self.validate_number(operand1), self.validate_number(operand2))

