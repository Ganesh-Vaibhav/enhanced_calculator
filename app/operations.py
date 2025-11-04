"""
Arithmetic operations with Factory Design Pattern.
"""

from abc import ABC, abstractmethod
from typing import Dict, Type
from app.exceptions import OperationError


class Operation(ABC):
    """Abstract base class for all operations."""
    
    @abstractmethod
    def execute(self, operand1: float, operand2: float) -> float:
        """Execute the operation on two operands."""
        pass
    
    @abstractmethod
    def get_symbol(self) -> str:
        """Get the symbol/name of the operation."""
        pass


class AddOperation(Operation):
    """Addition operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        return operand1 + operand2
    
    def get_symbol(self) -> str:
        return "add"


class SubtractOperation(Operation):
    """Subtraction operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        return operand1 - operand2
    
    def get_symbol(self) -> str:
        return "subtract"


class MultiplyOperation(Operation):
    """Multiplication operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        return operand1 * operand2
    
    def get_symbol(self) -> str:
        return "multiply"


class DivideOperation(Operation):
    """Division operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        if operand2 == 0:
            raise OperationError("Division by zero is not allowed")
        return operand1 / operand2
    
    def get_symbol(self) -> str:
        return "divide"


class PowerOperation(Operation):
    """Power operation (raise to power)."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        try:
            result = operand1 ** operand2
            if not isinstance(result, (int, float)) or (isinstance(result, complex) and result.imag != 0):
                raise OperationError(f"Cannot compute {operand1} to the power of {operand2}")
            return float(result)
        except (ValueError, OverflowError) as e:
            raise OperationError(f"Power operation failed: {str(e)}")
    
    def get_symbol(self) -> str:
        return "power"


class RootOperation(Operation):
    """Root operation (nth root)."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        if operand1 < 0 and operand2 % 2 == 0:
            raise OperationError("Cannot compute even root of negative number")
        if operand2 == 0:
            raise OperationError("Root degree cannot be zero")
        try:
            # For odd roots of negative numbers, use sign-aware calculation
            if operand1 < 0 and operand2 % 2 == 1:
                # Odd root of negative number: result is negative
                result = -((-operand1) ** (1.0 / operand2))
            else:
                result = operand1 ** (1.0 / operand2)
            
            # Check if result is complex (shouldn't happen with our logic, but just in case)
            if isinstance(result, complex):
                raise OperationError(f"Cannot compute {operand2}th root of {operand1}")
            return float(result)
        except (ValueError, OverflowError, ZeroDivisionError) as e:
            raise OperationError(f"Root operation failed: {str(e)}")
    
    def get_symbol(self) -> str:
        return "root"


class ModulusOperation(Operation):
    """Modulus operation (remainder)."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        if operand2 == 0:
            raise OperationError("Modulus by zero is not allowed")
        return operand1 % operand2
    
    def get_symbol(self) -> str:
        return "modulus"


class IntDivideOperation(Operation):
    """Integer division operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        if operand2 == 0:
            raise OperationError("Integer division by zero is not allowed")
        return float(operand1 // operand2)
    
    def get_symbol(self) -> str:
        return "int_divide"


class PercentOperation(Operation):
    """Percentage calculation (a / b * 100)."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        if operand2 == 0:
            raise OperationError("Percentage calculation: divisor cannot be zero")
        return (operand1 / operand2) * 100.0
    
    def get_symbol(self) -> str:
        return "percent"


class AbsDiffOperation(Operation):
    """Absolute difference operation."""
    
    def execute(self, operand1: float, operand2: float) -> float:
        return abs(operand1 - operand2)
    
    def get_symbol(self) -> str:
        return "abs_diff"


class OperationFactory:
    """Factory for creating operation instances."""
    
    _operations: Dict[str, Type[Operation]] = {
        'add': AddOperation,
        'subtract': SubtractOperation,
        'multiply': MultiplyOperation,
        'divide': DivideOperation,
        'power': PowerOperation,
        'root': RootOperation,
        'modulus': ModulusOperation,
        'int_divide': IntDivideOperation,
        'percent': PercentOperation,
        'abs_diff': AbsDiffOperation,
    }
    
    @classmethod
    def create(cls, operation_name: str) -> Operation:
        """Create an operation instance by name."""
        operation_name = operation_name.lower()
        if operation_name not in cls._operations:
            raise OperationError(f"Unknown operation: {operation_name}")
        return cls._operations[operation_name]()
    
    @classmethod
    def get_available_operations(cls) -> list:
        """Get list of available operation names."""
        return list(cls._operations.keys())

