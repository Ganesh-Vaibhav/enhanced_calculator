"""
Configuration management using .env file.
"""

import os
from pathlib import Path
from typing import Any, Optional
from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages calculator configuration from .env file."""
    
    def __init__(self, env_file: str = '.env'):
        """Initialize configuration by loading .env file."""
        self._config = {}
        self._load_config(env_file)
    
    def _load_config(self, env_file: str):
        """Load configuration from .env file."""
        env_path = Path(env_file)
        if env_path.exists():
            load_dotenv(env_path)
        
        # Base directories with defaults
        self._config['CALCULATOR_LOG_DIR'] = os.getenv(
            'CALCULATOR_LOG_DIR', 
            os.path.join(os.getcwd(), 'logs')
        )
        self._config['CALCULATOR_HISTORY_DIR'] = os.getenv(
            'CALCULATOR_HISTORY_DIR',
            os.path.join(os.getcwd(), 'history')
        )
        
        # History settings
        self._config['CALCULATOR_MAX_HISTORY_SIZE'] = int(os.getenv(
            'CALCULATOR_MAX_HISTORY_SIZE',
            '100'
        ))
        self._config['CALCULATOR_AUTO_SAVE'] = os.getenv(
            'CALCULATOR_AUTO_SAVE',
            'true'
        ).lower() == 'true'
        
        # Calculation settings
        self._config['CALCULATOR_PRECISION'] = int(os.getenv(
            'CALCULATOR_PRECISION',
            '10'
        ))
        self._config['CALCULATOR_MAX_INPUT_VALUE'] = float(os.getenv(
            'CALCULATOR_MAX_INPUT_VALUE',
            '1e308'
        ))
        self._config['CALCULATOR_DEFAULT_ENCODING'] = os.getenv(
            'CALCULATOR_DEFAULT_ENCODING',
            'utf-8'
        )
        
        # File paths
        self._config['CALCULATOR_LOG_FILE'] = os.path.join(
            self._config['CALCULATOR_LOG_DIR'],
            'calculator.log'
        )
        self._config['CALCULATOR_HISTORY_FILE'] = os.path.join(
            self._config['CALCULATOR_HISTORY_DIR'],
            'calculator_history.csv'
        )
        
        # Create directories if they don't exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure configuration directories exist."""
        Path(self._config['CALCULATOR_LOG_DIR']).mkdir(parents=True, exist_ok=True)
        Path(self._config['CALCULATOR_HISTORY_DIR']).mkdir(parents=True, exist_ok=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        """Get configuration value using bracket notation."""
        if key not in self._config:
            raise ConfigurationError(f"Configuration key '{key}' not found")
        return self._config[key]

