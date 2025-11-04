"""
Tests for operations module.
"""

import pytest
from app.operations import (
    OperationFactory,
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
    PowerOperation,
    RootOperation,
    ModulusOperation,
    IntDivideOperation,
    PercentOperation,
    AbsDiffOperation,
)
from app.exceptions import OperationError


class TestAddOperation:
    """Tests for addition operation."""
    
    def test_add_positive_numbers(self):
        op = AddOperation()
        assert op.execute(5, 3) == 8
    
    def test_add_negative_numbers(self):
        op = AddOperation()
        assert op.execute(-5, -3) == -8
    
    def test_add_mixed_numbers(self):
        op = AddOperation()
        assert op.execute(-5, 3) == -2


class TestSubtractOperation:
    """Tests for subtraction operation."""
    
    def test_subtract_positive_numbers(self):
        op = SubtractOperation()
        assert op.execute(5, 3) == 2
    
    def test_subtract_negative_numbers(self):
        op = SubtractOperation()
        assert op.execute(-5, -3) == -2


class TestMultiplyOperation:
    """Tests for multiplication operation."""
    
    def test_multiply_positive_numbers(self):
        op = MultiplyOperation()
        assert op.execute(5, 3) == 15
    
    def test_multiply_by_zero(self):
        op = MultiplyOperation()
        assert op.execute(5, 0) == 0


class TestDivideOperation:
    """Tests for division operation."""
    
    def test_divide_positive_numbers(self):
        op = DivideOperation()
        assert op.execute(10, 2) == 5.0
    
    def test_divide_by_zero(self):
        op = DivideOperation()
        with pytest.raises(OperationError, match="Division by zero"):
            op.execute(10, 0)
    
    def test_divide_negative_numbers(self):
        op = DivideOperation()
        assert op.execute(-10, -2) == 5.0


class TestPowerOperation:
    """Tests for power operation."""
    
    def test_power_positive_base_positive_exponent(self):
        op = PowerOperation()
        assert op.execute(2, 3) == 8.0
    
    def test_power_negative_base_positive_exponent(self):
        op = PowerOperation()
        assert op.execute(-2, 3) == -8.0
    
    def test_power_with_zero_exponent(self):
        op = PowerOperation()
        assert op.execute(5, 0) == 1.0
    
    def test_power_with_fractional_exponent(self):
        op = PowerOperation()
        result = op.execute(4, 0.5)
        assert abs(result - 2.0) < 1e-10


class TestRootOperation:
    """Tests for root operation."""
    
    def test_square_root(self):
        op = RootOperation()
        result = op.execute(4, 2)
        assert abs(result - 2.0) < 1e-10
    
    def test_cube_root(self):
        op = RootOperation()
        result = op.execute(8, 3)
        assert abs(result - 2.0) < 1e-10
    
    def test_even_root_of_negative_number(self):
        op = RootOperation()
        with pytest.raises(OperationError, match="even root of negative"):
            op.execute(-4, 2)
    
    def test_root_degree_zero(self):
        op = RootOperation()
        with pytest.raises(OperationError, match="Root degree cannot be zero"):
            op.execute(4, 0)


class TestModulusOperation:
    """Tests for modulus operation."""
    
    def test_modulus_positive_numbers(self):
        op = ModulusOperation()
        assert op.execute(10, 3) == 1.0
    
    def test_modulus_by_zero(self):
        op = ModulusOperation()
        with pytest.raises(OperationError, match="Modulus by zero"):
            op.execute(10, 0)
    
    def test_modulus_negative_numbers(self):
        op = ModulusOperation()
        result = op.execute(-10, 3)
        assert result == 2.0 or result == -1.0  # Python modulus behavior


class TestIntDivideOperation:
    """Tests for integer division operation."""
    
    def test_int_divide_positive_numbers(self):
        op = IntDivideOperation()
        assert op.execute(10, 3) == 3.0
    
    def test_int_divide_by_zero(self):
        op = IntDivideOperation()
        with pytest.raises(OperationError, match="Integer division by zero"):
            op.execute(10, 0)
    
    def test_int_divide_exact_division(self):
        op = IntDivideOperation()
        assert op.execute(10, 2) == 5.0


class TestPercentOperation:
    """Tests for percentage operation."""
    
    def test_percent_calculation(self):
        op = PercentOperation()
        assert op.execute(25, 100) == 25.0
    
    def test_percent_by_zero(self):
        op = PercentOperation()
        with pytest.raises(OperationError, match="divisor cannot be zero"):
            op.execute(25, 0)
    
    def test_percent_partial(self):
        op = PercentOperation()
        assert op.execute(50, 200) == 25.0


class TestAbsDiffOperation:
    """Tests for absolute difference operation."""
    
    def test_abs_diff_positive_numbers(self):
        op = AbsDiffOperation()
        assert op.execute(10, 5) == 5.0
    
    def test_abs_diff_negative_numbers(self):
        op = AbsDiffOperation()
        assert op.execute(-10, -5) == 5.0
    
    def test_abs_diff_mixed_numbers(self):
        op = AbsDiffOperation()
        assert op.execute(-10, 5) == 15.0


class TestOperationFactory:
    """Tests for operation factory."""
    
    @pytest.mark.parametrize("op_name,expected_class", [
        ('add', AddOperation),
        ('subtract', SubtractOperation),
        ('multiply', MultiplyOperation),
        ('divide', DivideOperation),
        ('power', PowerOperation),
        ('root', RootOperation),
        ('modulus', ModulusOperation),
        ('int_divide', IntDivideOperation),
        ('percent', PercentOperation),
        ('abs_diff', AbsDiffOperation),
    ])
    def test_create_operations(self, op_name, expected_class):
        op = OperationFactory.create(op_name)
        assert isinstance(op, expected_class)
    
    def test_create_unknown_operation(self):
        with pytest.raises(OperationError, match="Unknown operation"):
            OperationFactory.create('unknown_op')
    
    def test_create_case_insensitive(self):
        op1 = OperationFactory.create('ADD')
        op2 = OperationFactory.create('add')
        assert isinstance(op1, AddOperation)
        assert isinstance(op2, AddOperation)
    
    def test_get_available_operations(self):
        ops = OperationFactory.get_available_operations()
        assert 'add' in ops
        assert 'power' in ops
        assert 'root' in ops
        assert len(ops) >= 10

