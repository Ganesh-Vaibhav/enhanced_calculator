"""
Extended tests for calculator to improve coverage.
"""

import pytest
import os
import tempfile
from app.calculator import Calculator, LoggingObserver, AutoSaveObserver
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError


class TestCalculatorExtended:
    """Extended tests for Calculator class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        import shutil
        shutil.rmtree(temp_path)
    
    @pytest.fixture
    def config(self, temp_dir):
        """Create test configuration."""
        config = CalculatorConfig()
        config._config['CALCULATOR_LOG_DIR'] = os.path.join(temp_dir, 'logs')
        config._config['CALCULATOR_HISTORY_DIR'] = os.path.join(temp_dir, 'history')
        config._config['CALCULATOR_LOG_FILE'] = os.path.join(temp_dir, 'logs', 'test.log')
        config._config['CALCULATOR_HISTORY_FILE'] = os.path.join(temp_dir, 'history', 'test.csv')
        config._config['CALCULATOR_AUTO_SAVE'] = False
        return config
    
    @pytest.fixture
    def calculator(self, config):
        """Create calculator instance."""
        return Calculator(config)
    
    def test_observer_registration_and_removal(self, calculator):
        """Test observer registration and removal."""
        observer = LoggingObserver()
        calculator.register_observer(observer)
        calculator.calculate('add', 1, 1)
        
        calculator.remove_observer(observer)
        calculator.calculate('add', 1, 1)
        # Should not raise any errors
    
    def test_auto_save_observer(self, temp_dir):
        """Test auto-save observer."""
        config = CalculatorConfig()
        config._config['CALCULATOR_HISTORY_DIR'] = temp_dir
        config._config['CALCULATOR_HISTORY_FILE'] = os.path.join(temp_dir, 'test.csv')
        config._config['CALCULATOR_AUTO_SAVE'] = True
        
        calculator = Calculator(config)
        calculator.calculate('add', 5, 3)
        
        # Check if file was created
        assert os.path.exists(config._config['CALCULATOR_HISTORY_FILE'])
    
    def test_calculate_precision(self, calculator):
        """Test calculation precision."""
        result = calculator.calculate('divide', 1, 3)
        # Should be rounded based on precision
        assert isinstance(result, float)
    
    def test_multiple_undo_redo(self, calculator):
        """Test multiple undo/redo operations."""
        calculator.calculate('add', 1, 1)
        calculator.calculate('add', 2, 2)
        calculator.calculate('add', 3, 3)
        
        assert len(calculator.get_history()) == 3
        
        calculator.undo()
        assert len(calculator.get_history()) == 2
        
        calculator.undo()
        assert len(calculator.get_history()) == 1
        
        calculator.redo()
        assert len(calculator.get_history()) == 2
        
        calculator.redo()
        assert len(calculator.get_history()) == 3
    
    def test_observer_exception_handling(self, calculator):
        """Test that observer exceptions don't break calculator."""
        class FailingObserver:
            def update(self, calculation):
                raise Exception("Observer failed")
        
        observer = FailingObserver()
        calculator.register_observer(observer)
        
        # Should not raise, just log error
        result = calculator.calculate('add', 1, 1)
        assert result == 2.0
    
    def test_load_history_nonexistent_file(self, calculator):
        """Test loading from non-existent file."""
        result = calculator.load_history('/nonexistent/file.csv')
        assert result == []
    
    def test_save_history_with_custom_path(self, calculator, temp_dir):
        """Test saving with custom file path."""
        calculator.calculate('add', 5, 3)
        file_path = os.path.join(temp_dir, 'custom.csv')
        result_path = calculator.save_history(file_path)
        assert os.path.exists(result_path)
    
    def test_precision_rounding(self, calculator):
        """Test that results are rounded to precision."""
        # Set precision to 2
        calculator.config._config['CALCULATOR_PRECISION'] = 2
        result = calculator.calculate('divide', 1, 3)
        # Should be rounded to 2 decimal places
        assert len(str(result).split('.')[-1]) <= 2 or result == round(result, 2)

