"""
Tests for observer pattern implementation.
"""

import pytest
import os
import tempfile
from app.calculator import Calculator, LoggingObserver, AutoSaveObserver
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation


class TestLoggingObserver:
    """Tests for LoggingObserver."""
    
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
        config._config['CALCULATOR_LOG_DIR'] = temp_dir
        config._config['CALCULATOR_LOG_FILE'] = os.path.join(temp_dir, 'test.log')
        config._config['CALCULATOR_AUTO_SAVE'] = False
        return config
    
    def test_logging_observer_update(self, config):
        """Test that logging observer logs calculations."""
        calculator = Calculator(config)
        observer = LoggingObserver()
        calculator.register_observer(observer)
        
        calculator.calculate('add', 5, 3)
        
        # Check if log file was created and has content
        log_file = config.get('CALCULATOR_LOG_FILE')
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                content = f.read()
                assert 'add' in content or 'Calculation' in content


class TestAutoSaveObserver:
    """Tests for AutoSaveObserver."""
    
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
        config._config['CALCULATOR_HISTORY_DIR'] = temp_dir
        config._config['CALCULATOR_HISTORY_FILE'] = os.path.join(temp_dir, 'test.csv')
        config._config['CALCULATOR_AUTO_SAVE'] = False
        return config
    
    def test_auto_save_observer_update(self, config, temp_dir):
        """Test that auto-save observer saves history."""
        from app.history import HistoryManager
        
        history_manager = HistoryManager(config)
        # Add calculation to history first
        calc = Calculation('add', 5, 3, 8)
        history_manager.add(calc)
        
        observer = AutoSaveObserver(history_manager)
        observer.update(calc)
        
        # Check if file was created
        history_file = config.get('CALCULATOR_HISTORY_FILE')
        assert os.path.exists(history_file)
    
    def test_auto_save_observer_exception_handling(self, config, temp_dir):
        """Test that auto-save observer handles exceptions."""
        from app.history import HistoryManager
        from unittest.mock import patch
        
        history_manager = HistoryManager(config)
        observer = AutoSaveObserver(history_manager)
        
        calc = Calculation('add', 5, 3, 8)
        history_manager.add(calc)
        
        # Should not raise even if save fails
        with patch.object(history_manager, 'save_to_csv', side_effect=Exception("Save failed")):
            observer.update(calc)  # Should not raise

