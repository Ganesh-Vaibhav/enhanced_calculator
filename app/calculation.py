"""
Calculation data model representing a single calculation.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Calculation:
    """Represents a single calculation with operation, operands, and result."""
    
    operation: str
    operand1: float
    operand2: float
    result: float
    timestamp: datetime = None
    
    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert calculation to dictionary for serialization."""
        return {
            'operation': self.operation,
            'operand1': self.operand1,
            'operand2': self.operand2,
            'result': self.result,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Calculation':
        """Create Calculation from dictionary."""
        timestamp = data.get('timestamp')
        if timestamp and isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        return cls(
            operation=data['operation'],
            operand1=float(data['operand1']),
            operand2=float(data['operand2']),
            result=float(data['result']),
            timestamp=timestamp
        )

