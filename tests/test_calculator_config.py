"""
Tests for calculator configuration.
"""

import pytest
import os
import tempfile
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


class TestCalculatorConfig:
    """Tests for CalculatorConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = CalculatorConfig()
        assert config.get('CALCULATOR_LOG_DIR') is not None
        assert config.get('CALCULATOR_HISTORY_DIR') is not None
        assert config.get('CALCULATOR_MAX_HISTORY_SIZE') == 100
        assert config.get('CALCULATOR_PRECISION') == 10
    
    def test_get_config_value(self):
        """Test getting configuration value."""
        config = CalculatorConfig()
        value = config.get('CALCULATOR_PRECISION')
        assert isinstance(value, int)
    
    def test_get_config_with_default(self):
        """Test getting config value with default."""
        config = CalculatorConfig()
        value = config.get('NONEXISTENT_KEY', 'default')
        assert value == 'default'
    
    def test_getitem_config(self):
        """Test getting config using bracket notation."""
        config = CalculatorConfig()
        value = config['CALCULATOR_PRECISION']
        assert isinstance(value, int)
    
    def test_getitem_nonexistent(self):
        """Test getting nonexistent config key."""
        config = CalculatorConfig()
        with pytest.raises(ConfigurationError):
            _ = config['NONEXISTENT_KEY']
    
    def test_directory_creation(self, tmp_path):
        """Test that directories are created."""
        log_dir = str(tmp_path / 'logs')
        history_dir = str(tmp_path / 'history')
        
        # Manually set directories
        config = CalculatorConfig()
        config._config['CALCULATOR_LOG_DIR'] = log_dir
        config._config['CALCULATOR_HISTORY_DIR'] = history_dir
        config._ensure_directories()
        
        assert os.path.exists(log_dir)
        assert os.path.exists(history_dir)

