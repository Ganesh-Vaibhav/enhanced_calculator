"""
Tests for calculation data model.
"""

from datetime import datetime
from app.calculation import Calculation


class TestCalculation:
    """Tests for Calculation class."""
    
    def test_calculation_creation(self):
        calc = Calculation(
            operation='add',
            operand1=5.0,
            operand2=3.0,
            result=8.0
        )
        assert calc.operation == 'add'
        assert calc.operand1 == 5.0
        assert calc.operand2 == 3.0
        assert calc.result == 8.0
        assert isinstance(calc.timestamp, datetime)
    
    def test_calculation_with_timestamp(self):
        timestamp = datetime(2023, 1, 1, 12, 0, 0)
        calc = Calculation(
            operation='multiply',
            operand1=2.0,
            operand2=3.0,
            result=6.0,
            timestamp=timestamp
        )
        assert calc.timestamp == timestamp
    
    def test_to_dict(self):
        calc = Calculation(
            operation='divide',
            operand1=10.0,
            operand2=2.0,
            result=5.0
        )
        data = calc.to_dict()
        assert data['operation'] == 'divide'
        assert data['operand1'] == 10.0
        assert data['operand2'] == 2.0
        assert data['result'] == 5.0
        assert 'timestamp' in data
    
    def test_from_dict(self):
        timestamp = datetime(2023, 1, 1, 12, 0, 0)
        data = {
            'operation': 'subtract',
            'operand1': '10.0',
            'operand2': '3.0',
            'result': '7.0',
            'timestamp': timestamp.isoformat()
        }
        calc = Calculation.from_dict(data)
        assert calc.operation == 'subtract'
        assert calc.operand1 == 10.0
        assert calc.operand2 == 3.0
        assert calc.result == 7.0
        assert isinstance(calc.timestamp, datetime)

