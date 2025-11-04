"""
History management with pandas for serialization.
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional
from app.calculation import Calculation
from app.exceptions import HistoryError
from app.calculator_config import CalculatorConfig


class HistoryManager:
    """Manages calculation history with pandas serialization."""
    
    def __init__(self, config: CalculatorConfig):
        """Initialize history manager with configuration."""
        self.config = config
        self.history: List[Calculation] = []
        self.max_size = config.get('CALCULATOR_MAX_HISTORY_SIZE', 100)
    
    def add(self, calculation: Calculation):
        """Add a calculation to history."""
        self.history.append(calculation)
        if len(self.history) > self.max_size:
            self.history.pop(0)  # Remove oldest entry
    
    def clear(self):
        """Clear all history."""
        self.history.clear()
    
    def get_all(self) -> List[Calculation]:
        """Get all calculations in history."""
        return self.history.copy()
    
    def save_to_csv(self, file_path: Optional[str] = None) -> str:
        """Save history to CSV file using pandas."""
        if file_path is None:
            file_path = self.config.get('CALCULATOR_HISTORY_FILE')
        
        try:
            # Convert history to DataFrame
            if not self.history:
                # Create empty DataFrame with correct columns
                df = pd.DataFrame(columns=['operation', 'operand1', 'operand2', 'result', 'timestamp'])
            else:
                data = [calc.to_dict() for calc in self.history]
                df = pd.DataFrame(data)
            
            # Ensure directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save to CSV
            encoding = self.config.get('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
            df.to_csv(file_path, index=False, encoding=encoding)
            
            return file_path
        except Exception as e:
            raise HistoryError(f"Failed to save history to CSV: {str(e)}")
    
    def load_from_csv(self, file_path: Optional[str] = None) -> List[Calculation]:
        """Load history from CSV file using pandas."""
        if file_path is None:
            file_path = self.config.get('CALCULATOR_HISTORY_FILE')
        
        try:
            # Check if file exists
            if not Path(file_path).exists():
                return []
            
            # Read CSV
            encoding = self.config.get('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
            df = pd.read_csv(file_path, encoding=encoding)
            
            # Validate required columns
            required_columns = ['operation', 'operand1', 'operand2', 'result', 'timestamp']
            if not all(col in df.columns for col in required_columns):
                raise HistoryError(f"CSV file missing required columns: {required_columns}")
            
            # Convert DataFrame rows to Calculation objects
            calculations = []
            for _, row in df.iterrows():
                try:
                    calc = Calculation.from_dict(row.to_dict())
                    calculations.append(calc)
                except Exception as e:
                    # Skip invalid rows but log the error
                    continue
            
            self.history = calculations
            return calculations
        except pd.errors.EmptyDataError:
            return []
        except Exception as e:
            raise HistoryError(f"Failed to load history from CSV: {str(e)}")

