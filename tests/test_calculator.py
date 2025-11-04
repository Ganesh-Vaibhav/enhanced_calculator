"""
Tests for calculator class.
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from app.calculator import Calculator, LoggingObserver, AutoSaveObserver
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation
from app.exceptions import OperationError, ValidationError


class TestCalculator:
    """Tests for Calculator class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path)
    
    @pytest.fixture
    def config(self, temp_dir):
        """Create test configuration."""
        config = CalculatorConfig()
        config._config['CALCULATOR_LOG_DIR'] = os.path.join(temp_dir, 'logs')
        config._config['CALCULATOR_HISTORY_DIR'] = os.path.join(temp_dir, 'history')
        config._config['CALCULATOR_LOG_FILE'] = os.path.join(temp_dir, 'logs', 'test.log')
        config._config['CALCULATOR_HISTORY_FILE'] = os.path.join(temp_dir, 'history', 'test.csv')
        config._config['CALCULATOR_AUTO_SAVE'] = False  # Disable auto-save for tests
        return config
    
    @pytest.fixture
    def calculator(self, config):
        """Create calculator instance."""
        return Calculator(config)
    
    def test_calculate_addition(self, calculator):
        """Test basic addition."""
        result = calculator.calculate('add', 5, 3)
        assert result == 8.0
    
    def test_calculate_subtraction(self, calculator):
        """Test subtraction."""
        result = calculator.calculate('subtract', 10, 3)
        assert result == 7.0
    
    def test_calculate_division_by_zero(self, calculator):
        """Test division by zero error."""
        with pytest.raises(OperationError):
            calculator.calculate('divide', 10, 0)
    
    def test_calculate_power(self, calculator):
        """Test power operation."""
        result = calculator.calculate('power', 2, 8)
        assert result == 256.0
    
    def test_calculate_root(self, calculator):
        """Test root operation."""
        result = calculator.calculate('root', 16, 2)
        assert abs(result - 4.0) < 1e-10
    
    def test_calculate_modulus(self, calculator):
        """Test modulus operation."""
        result = calculator.calculate('modulus', 10, 3)
        assert result == 1.0
    
    def test_calculate_int_divide(self, calculator):
        """Test integer division."""
        result = calculator.calculate('int_divide', 10, 3)
        assert result == 3.0
    
    def test_calculate_percent(self, calculator):
        """Test percentage calculation."""
        result = calculator.calculate('percent', 25, 100)
        assert result == 25.0
    
    def test_calculate_abs_diff(self, calculator):
        """Test absolute difference."""
        result = calculator.calculate('abs_diff', 10, 5)
        assert result == 5.0
    
    def test_history_after_calculation(self, calculator):
        """Test that calculation is added to history."""
        calculator.calculate('add', 5, 3)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].result == 8.0
    
    def test_clear_history(self, calculator):
        """Test clearing history."""
        calculator.calculate('add', 5, 3)
        calculator.clear_history()
        assert len(calculator.get_history()) == 0
    
    def test_undo(self, calculator):
        """Test undo functionality."""
        calculator.calculate('add', 5, 3)
        calculator.calculate('multiply', 2, 4)
        assert len(calculator.get_history()) == 2
        
        calculator.undo()
        assert len(calculator.get_history()) == 1
        assert calculator.get_history()[0].operation == 'add'
    
    def test_undo_empty_history(self, calculator):
        """Test undo with empty history."""
        assert not calculator.undo()
    
    def test_redo(self, calculator):
        """Test redo functionality."""
        calculator.calculate('add', 5, 3)
        calculator.undo()
        assert len(calculator.get_history()) == 0
        
        calculator.redo()
        assert len(calculator.get_history()) == 1
    
    def test_redo_empty(self, calculator):
        """Test redo with nothing to redo."""
        assert not calculator.redo()
    
    def test_save_history(self, calculator, temp_dir):
        """Test saving history to CSV."""
        calculator.calculate('add', 5, 3)
        calculator.calculate('multiply', 2, 4)
        
        file_path = os.path.join(temp_dir, 'test_history.csv')
        result_path = calculator.save_history(file_path)
        assert os.path.exists(result_path)
    
    def test_load_history(self, calculator, temp_dir):
        """Test loading history from CSV."""
        calculator.calculate('add', 5, 3)
        calculator.calculate('multiply', 2, 4)
        
        file_path = os.path.join(temp_dir, 'test_history.csv')
        calculator.save_history(file_path)
        
        # Clear and reload
        calculator.clear_history()
        calculator.load_history(file_path)
        
        history = calculator.get_history()
        assert len(history) == 2
    
    def test_observer_registration(self, calculator):
        """Test observer registration."""
        observer = LoggingObserver()
        calculator.register_observer(observer)
        # Should not raise any error
        calculator.calculate('add', 1, 1)
    
    def test_invalid_operation(self, calculator):
        """Test invalid operation name."""
        with pytest.raises(OperationError):
            calculator.calculate('invalid_op', 1, 1)
    
    def test_invalid_input(self, calculator):
        """Test invalid input validation."""
        with pytest.raises(ValidationError):
            calculator.calculate('add', 'not_a_number', 1)

