"""
Tests for history management.
"""

import pytest
import os
import tempfile
import shutil
from app.history import HistoryManager
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig


class TestHistoryManager:
    """Tests for HistoryManager class."""
    
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
        config._config['CALCULATOR_HISTORY_DIR'] = temp_dir
        config._config['CALCULATOR_HISTORY_FILE'] = os.path.join(temp_dir, 'test_history.csv')
        config._config['CALCULATOR_MAX_HISTORY_SIZE'] = 5
        return config
    
    @pytest.fixture
    def history_manager(self, config):
        """Create history manager instance."""
        return HistoryManager(config)
    
    def test_add_calculation(self, history_manager):
        """Test adding calculation to history."""
        calc = Calculation('add', 5, 3, 8)
        history_manager.add(calc)
        assert len(history_manager.get_all()) == 1
    
    def test_max_size_limit(self, history_manager):
        """Test that history respects max size."""
        for i in range(10):
            calc = Calculation('add', i, i, i * 2)
            history_manager.add(calc)
        
        assert len(history_manager.get_all()) == 5
    
    def test_clear_history(self, history_manager):
        """Test clearing history."""
        calc = Calculation('add', 5, 3, 8)
        history_manager.add(calc)
        history_manager.clear()
        assert len(history_manager.get_all()) == 0
    
    def test_save_to_csv(self, history_manager, temp_dir):
        """Test saving history to CSV."""
        calc1 = Calculation('add', 5, 3, 8)
        calc2 = Calculation('multiply', 2, 4, 8)
        history_manager.add(calc1)
        history_manager.add(calc2)
        
        file_path = os.path.join(temp_dir, 'test.csv')
        result_path = history_manager.save_to_csv(file_path)
        assert os.path.exists(result_path)
    
    def test_load_from_csv(self, history_manager, temp_dir):
        """Test loading history from CSV."""
        calc1 = Calculation('add', 5, 3, 8)
        calc2 = Calculation('multiply', 2, 4, 8)
        history_manager.add(calc1)
        history_manager.add(calc2)
        
        file_path = os.path.join(temp_dir, 'test.csv')
        history_manager.save_to_csv(file_path)
        
        # Clear and reload
        history_manager.clear()
        history_manager.load_from_csv(file_path)
        
        history = history_manager.get_all()
        assert len(history) == 2
    
    def test_load_from_nonexistent_file(self, history_manager):
        """Test loading from non-existent file."""
        result = history_manager.load_from_csv('/nonexistent/file.csv')
        assert result == []

