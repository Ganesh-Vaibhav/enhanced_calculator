"""
Tests for logger module.
"""

import pytest
import logging
import os
import tempfile
from app.logger import CalculatorLogger
from app.calculator_config import CalculatorConfig


class TestCalculatorLogger:
    """Tests for CalculatorLogger class."""
    
    def test_setup(self, tmp_path):
        """Test logger setup."""
        config = CalculatorConfig()
        config._config['CALCULATOR_LOG_DIR'] = str(tmp_path)
        config._config['CALCULATOR_LOG_FILE'] = str(tmp_path / 'test.log')
        
        # Reset logger
        CalculatorLogger._logger = None
        
        logger = CalculatorLogger.setup(config)
        assert logger is not None
        assert isinstance(logger, logging.Logger)
    
    def test_get_logger_without_setup(self, tmp_path):
        """Test getting logger without setup."""
        # First setup to ensure we can test the failure case
        config = CalculatorConfig()
        config._config['CALCULATOR_LOG_DIR'] = str(tmp_path)
        config._config['CALCULATOR_LOG_FILE'] = str(tmp_path / 'test.log')
        CalculatorLogger.setup(config)
        
        # Now test the failure case by temporarily removing the logger
        original_logger = CalculatorLogger._logger
        CalculatorLogger._logger = None
        try:
            with pytest.raises(RuntimeError, match="Logger not initialized"):
                CalculatorLogger.get_logger()
        finally:
            CalculatorLogger._logger = original_logger
    
    def test_get_logger_after_setup(self, tmp_path):
        """Test getting logger after setup."""
        config = CalculatorConfig()
        config._config['CALCULATOR_LOG_DIR'] = str(tmp_path)
        config._config['CALCULATOR_LOG_FILE'] = str(tmp_path / 'test.log')
        
        # Reset logger
        CalculatorLogger._logger = None
        
        # Setup logger
        CalculatorLogger.setup(config)
        
        # Now get logger should work
        logger = CalculatorLogger.get_logger()
        assert logger is not None

