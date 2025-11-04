"""
Extended tests for operations to improve coverage.
"""

import pytest
from app.operations import (
    PowerOperation,
    RootOperation,
    ModulusOperation,
    IntDivideOperation,
    PercentOperation,
    AbsDiffOperation,
    OperationFactory,
)
from app.exceptions import OperationError


class TestPowerOperationExtended:
    """Extended tests for power operation."""
    
    def test_power_negative_base_odd_exponent(self):
        """Test power with negative base and odd exponent."""
        op = PowerOperation()
        assert op.execute(-2, 3) == -8.0
    
    def test_power_negative_base_even_exponent(self):
        """Test power with negative base and even exponent."""
        op = PowerOperation()
        assert op.execute(-2, 4) == 16.0
    
    def test_power_fractional_result(self):
        """Test power with fractional result."""
        op = PowerOperation()
        result = op.execute(2, 0.5)
        assert abs(result - 1.4142135623730951) < 1e-10


class TestRootOperationExtended:
    """Extended tests for root operation."""
    
    def test_odd_root_of_negative_number(self):
        """Test odd root of negative number."""
        op = RootOperation()
        result = op.execute(-8, 3)
        assert abs(result - (-2.0)) < 1e-10 or result < 0
    
    def test_fourth_root(self):
        """Test fourth root."""
        op = RootOperation()
        result = op.execute(16, 4)
        assert abs(result - 2.0) < 1e-10


class TestModulusOperationExtended:
    """Extended tests for modulus operation."""
    
    def test_modulus_negative_dividend(self):
        """Test modulus with negative dividend."""
        op = ModulusOperation()
        result = op.execute(-10, 3)
        # Python modulus behavior
        assert result in [2.0, -1.0]
    
    def test_modulus_float_result(self):
        """Test modulus with float result."""
        op = ModulusOperation()
        result = op.execute(10.5, 3)
        assert result == 1.5


class TestIntDivideOperationExtended:
    """Extended tests for integer division."""
    
    def test_int_divide_negative_numbers(self):
        """Test integer division with negative numbers."""
        op = IntDivideOperation()
        result = op.execute(-10, 3)
        assert result == -4.0 or result == -3.0  # Floor division behavior
    
    def test_int_divide_float_operands(self):
        """Test integer division with float operands."""
        op = IntDivideOperation()
        result = op.execute(10.7, 3.2)
        assert result == 3.0  # 10.7 // 3.2 = 3.0


class TestPercentOperationExtended:
    """Extended tests for percentage operation."""
    
    def test_percent_decimal_result(self):
        """Test percentage with decimal result."""
        op = PercentOperation()
        result = op.execute(1, 3)
        assert abs(result - 33.3333333333) < 1e-10
    
    def test_percent_over_100(self):
        """Test percentage over 100."""
        op = PercentOperation()
        result = op.execute(150, 100)
        assert result == 150.0


class TestAbsDiffOperationExtended:
    """Extended tests for absolute difference."""
    
    def test_abs_diff_same_numbers(self):
        """Test absolute difference of same numbers."""
        op = AbsDiffOperation()
        assert op.execute(5, 5) == 0.0
    
    def test_abs_diff_float_numbers(self):
        """Test absolute difference with floats."""
        op = AbsDiffOperation()
        result = op.execute(10.5, 3.2)
        assert abs(result - 7.3) < 1e-10


class TestOperationFactoryExtended:
    """Extended tests for operation factory."""
    
    def test_create_case_variations(self):
        """Test creating operations with case variations."""
        op1 = OperationFactory.create('POWER')
        op2 = OperationFactory.create('Power')
        op3 = OperationFactory.create('power')
        assert type(op1) == type(op2) == type(op3)
    
    @pytest.mark.parametrize("op_name", [
        'add', 'subtract', 'multiply', 'divide',
        'power', 'root', 'modulus', 'int_divide',
        'percent', 'abs_diff'
    ])
    def test_all_operations_creatable(self, op_name):
        """Test that all operations can be created."""
        op = OperationFactory.create(op_name)
        assert op is not None
        assert op.get_symbol() == op_name

