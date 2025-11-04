"""
Logging configuration and utilities.
"""

import logging
import os
from pathlib import Path
from typing import Optional
from app.calculator_config import CalculatorConfig


class CalculatorLogger:
    """Configures and manages logging for the calculator."""
    
    _logger: Optional[logging.Logger] = None
    
    @classmethod
    def setup(cls, config: CalculatorConfig):
        """Setup logging configuration."""
        if cls._logger is not None:
            return cls._logger
        
        logger = logging.getLogger('calculator')
        logger.setLevel(logging.INFO)
        
        # Prevent duplicate handlers
        if logger.handlers:
            return logger
        
        # File handler
        log_file = config.get('CALCULATOR_LOG_FILE')
        log_dir = os.path.dirname(log_file)
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        cls._logger = logger
        return logger
    
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Get the configured logger instance."""
        if cls._logger is None:
            raise RuntimeError("Logger not initialized. Call setup() first.")
        return cls._logger

