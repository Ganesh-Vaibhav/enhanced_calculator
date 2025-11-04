"""
Tests for input validators.
"""

import pytest
from app.input_validators import InputValidator
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


class TestInputValidator:
    """Tests for InputValidator class."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        config = CalculatorConfig()
        config._config['CALCULATOR_MAX_INPUT_VALUE'] = 1000.0
        return config
    
    @pytest.fixture
    def validator(self, config):
        """Create validator instance."""
        return InputValidator(config)
    
    def test_validate_number_valid(self, validator):
        """Test validating valid numbers."""
        assert validator.validate_number('5') == 5.0
        assert validator.validate_number(5) == 5.0
        assert validator.validate_number(5.5) == 5.5
    
    def test_validate_number_invalid(self, validator):
        """Test validating invalid numbers."""
        with pytest.raises(ValidationError):
            validator.validate_number('not_a_number')
    
    def test_validate_number_exceeds_max(self, validator):
        """Test validating number that exceeds max."""
        with pytest.raises(ValidationError):
            validator.validate_number(2000)
    
    def test_validate_operation_valid(self, validator):
        """Test validating valid operation."""
        assert validator.validate_operation('add') == 'add'
        assert validator.validate_operation('  ADD  ') == 'add'
    
    def test_validate_operation_invalid(self, validator):
        """Test validating invalid operation."""
        with pytest.raises(ValidationError):
            validator.validate_operation('')
    
    def test_validate_operands(self, validator):
        """Test validating operands."""
        op1, op2 = validator.validate_operands('5', '3')
        assert op1 == 5.0
        assert op2 == 3.0

