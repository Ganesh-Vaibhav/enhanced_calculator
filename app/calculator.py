"""
Main calculator class with Observer pattern and REPL interface.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal, getcontext
from app.calculation import Calculation
from app.operations import OperationFactory
from app.input_validators import InputValidator
from app.history import HistoryManager
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorCaretaker
from app.exceptions import CalculatorError, OperationError, ValidationError
from app.logger import CalculatorLogger


class Observer(ABC):
    """Abstract observer interface."""
    
    @abstractmethod
    def update(self, calculation: Calculation):
        """Called when a new calculation is performed."""
        pass


class LoggingObserver(Observer):
    """Observer that logs calculations."""
    
    def update(self, calculation: Calculation):
        """Log the calculation."""
        try:
            logger = CalculatorLogger.get_logger()
            logger.info(
                f"Calculation: {calculation.operand1} {calculation.operation} "
                f"{calculation.operand2} = {calculation.result}"
            )
        except RuntimeError:
            # Logger not initialized, skip logging
            pass


class AutoSaveObserver(Observer):
    """Observer that auto-saves history to CSV."""
    
    def __init__(self, history_manager: HistoryManager):
        """Initialize with history manager."""
        self.history_manager = history_manager
    
    def update(self, calculation: Calculation):
        """Auto-save history after calculation."""
        try:
            self.history_manager.save_to_csv()
        except Exception as e:
            try:
                logger = CalculatorLogger.get_logger()
                logger.error(f"Auto-save failed: {str(e)}")
            except RuntimeError:
                # Logger not initialized, skip logging
                pass


class Calculator:
    """Main calculator class with history, undo/redo, and observer pattern."""
    
    def __init__(self, config: CalculatorConfig):
        """Initialize calculator with configuration."""
        self.config = config
        self.validator = InputValidator(config)
        self.history_manager = HistoryManager(config)
        self.caretaker = CalculatorCaretaker()
        self.observers: List[Observer] = []
        
        # Set precision for Decimal operations
        precision = config.get('CALCULATOR_PRECISION', 10)
        getcontext().prec = precision
        
        # Setup logger
        CalculatorLogger.setup(config)
        
        # Register default observers
        self._register_default_observers()
    
    def _register_default_observers(self):
        """Register default observers based on configuration."""
        # Always register logging observer
        self.register_observer(LoggingObserver())
        
        # Register auto-save observer if enabled
        if self.config.get('CALCULATOR_AUTO_SAVE', False):
            self.register_observer(AutoSaveObserver(self.history_manager))
    
    def register_observer(self, observer: Observer):
        """Register an observer to be notified of calculations."""
        self.observers.append(observer)
    
    def remove_observer(self, observer: Observer):
        """Remove an observer."""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def _notify_observers(self, calculation: Calculation):
        """Notify all observers of a new calculation."""
        for observer in self.observers:
            try:
                observer.update(calculation)
            except Exception as e:
                # Try to log error, but don't fail if logger isn't available
                try:
                    logger = CalculatorLogger.get_logger()
                    logger.error(f"Observer notification failed: {str(e)}")
                except RuntimeError:
                    # Logger not initialized, skip logging
                    pass
    
    def calculate(self, operation: str, operand1: float, operand2: float) -> float:
        """Perform a calculation and return the result."""
        # Validate inputs
        operation = self.validator.validate_operation(operation)
        operand1, operand2 = self.validator.validate_operands(operand1, operand2)
        
        # Create operation instance
        op = OperationFactory.create(operation)
        
        # Execute operation
        try:
            result = op.execute(operand1, operand2)
        except OperationError:
            raise
        except Exception as e:
            raise OperationError(f"Operation failed: {str(e)}")
        
        # Round result based on precision
        precision = self.config.get('CALCULATOR_PRECISION', 10)
        result = round(result, precision)
        
        # Create calculation record
        calculation = Calculation(
            operation=operation,
            operand1=operand1,
            operand2=operand2,
            result=result
        )
        
        # Save state for undo
        self.caretaker.save_state(self.history_manager.get_all())
        
        # Add to history
        self.history_manager.add(calculation)
        
        # Notify observers
        self._notify_observers(calculation)
        
        return result
    
    def get_history(self) -> List[Calculation]:
        """Get calculation history."""
        return self.history_manager.get_all()
    
    def clear_history(self):
        """Clear calculation history."""
        self.caretaker.save_state(self.history_manager.get_all())
        self.history_manager.clear()
        try:
            logger = CalculatorLogger.get_logger()
            logger.info("History cleared")
        except RuntimeError:
            # Logger not initialized, skip logging
            pass
    
    def undo(self) -> bool:
        """Undo the last calculation."""
        if not self.caretaker.can_undo():
            return False
        
        previous_history = self.caretaker.undo(self.history_manager.get_all())
        self.history_manager.history = previous_history
        try:
            logger = CalculatorLogger.get_logger()
            logger.info("Undo performed")
        except RuntimeError:
            # Logger not initialized, skip logging
            pass
        return True
    
    def redo(self) -> bool:
        """Redo the last undone calculation."""
        if not self.caretaker.can_redo():
            return False
        
        next_history = self.caretaker.redo(self.history_manager.get_all())
        self.history_manager.history = next_history
        try:
            logger = CalculatorLogger.get_logger()
            logger.info("Redo performed")
        except RuntimeError:
            # Logger not initialized, skip logging
            pass
        return True
    
    def save_history(self, file_path: Optional[str] = None) -> str:
        """Save history to CSV file."""
        return self.history_manager.save_to_csv(file_path)
    
    def load_history(self, file_path: Optional[str] = None) -> List[Calculation]:
        """Load history from CSV file."""
        calculations = self.history_manager.load_from_csv(file_path)
        try:
            logger = CalculatorLogger.get_logger()
            logger.info(f"Loaded {len(calculations)} calculations from history")
        except RuntimeError:
            # Logger not initialized, skip logging
            pass
        return calculations

