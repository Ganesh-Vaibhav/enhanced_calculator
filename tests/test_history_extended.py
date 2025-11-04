"""
Extended tests for history management.
"""

import pytest
import os
import tempfile
import pandas as pd
from app.history import HistoryManager
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.exceptions import HistoryError


class TestHistoryManagerExtended:
    """Extended tests for HistoryManager."""
    
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
        config._config['CALCULATOR_HISTORY_FILE'] = os.path.join(temp_dir, 'test_history.csv')
        config._config['CALCULATOR_MAX_HISTORY_SIZE'] = 3
        return config
    
    @pytest.fixture
    def history_manager(self, config):
        """Create history manager instance."""
        return HistoryManager(config)
    
    def test_max_size_enforcement(self, history_manager):
        """Test that max size is enforced."""
        # Add more than max_size
        for i in range(5):
            calc = Calculation('add', i, i, i * 2)
            history_manager.add(calc)
        
        assert len(history_manager.get_all()) == 3
    
    def test_save_empty_history(self, history_manager, temp_dir):
        """Test saving empty history."""
        file_path = os.path.join(temp_dir, 'empty.csv')
        result_path = history_manager.save_to_csv(file_path)
        assert os.path.exists(result_path)
        
        # Verify file is empty or has headers
        df = pd.read_csv(result_path)
        assert len(df) == 0 or 'operation' in df.columns
    
    def test_load_malformed_csv(self, history_manager, temp_dir):
        """Test loading malformed CSV."""
        file_path = os.path.join(temp_dir, 'malformed.csv')
        # Create a file with invalid data
        with open(file_path, 'w') as f:
            f.write("invalid,data\n")
        
        # Should handle gracefully
        try:
            history_manager.load_from_csv(file_path)
        except HistoryError:
            pass  # Expected
    
    def test_save_load_roundtrip(self, history_manager, temp_dir):
        """Test save and load roundtrip."""
        calc1 = Calculation('add', 5, 3, 8)
        calc2 = Calculation('multiply', 2, 4, 8)
        calc3 = Calculation('divide', 10, 2, 5)
        
        history_manager.add(calc1)
        history_manager.add(calc2)
        history_manager.add(calc3)
        
        file_path = os.path.join(temp_dir, 'roundtrip.csv')
        history_manager.save_to_csv(file_path)
        
        # Clear and reload
        history_manager.clear()
        history_manager.load_from_csv(file_path)
        
        history = history_manager.get_all()
        assert len(history) == 3
        assert history[0].operation == 'add'
        assert history[1].operation == 'multiply'
        assert history[2].operation == 'divide'
    
    def test_get_all_returns_copy(self, history_manager):
        """Test that get_all returns a copy."""
        calc = Calculation('add', 5, 3, 8)
        history_manager.add(calc)
        
        history1 = history_manager.get_all()
        history1.append(Calculation('multiply', 2, 4, 8))
        
        history2 = history_manager.get_all()
        assert len(history2) == 1  # Original should be unchanged

