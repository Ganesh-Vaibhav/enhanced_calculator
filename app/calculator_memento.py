"""
Memento Design Pattern for undo/redo functionality.
"""

from copy import deepcopy
from typing import List
from app.calculation import Calculation


class CalculatorMemento:
    """Memento class to store calculator state."""
    
    def __init__(self, history: List[Calculation]):
        """Initialize memento with a copy of the history."""
        self._history = deepcopy(history)
    
    def get_history(self) -> List[Calculation]:
        """Get the stored history."""
        return deepcopy(self._history)


class CalculatorCaretaker:
    """Manages mementos for undo/redo operations."""
    
    def __init__(self):
        """Initialize caretaker with empty stacks."""
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []
    
    def save_state(self, history: List[Calculation]):
        """Save current state to undo stack and clear redo stack."""
        memento = CalculatorMemento(history)
        self._undo_stack.append(memento)
        self._redo_stack.clear()  # Clear redo when new action is performed
    
    def undo(self, current_history: List[Calculation]) -> List[Calculation]:
        """Restore previous state from undo stack."""
        if not self._undo_stack:
            return current_history
        
        # Save current state to redo stack
        current_memento = CalculatorMemento(current_history)
        self._redo_stack.append(current_memento)
        
        # Restore previous state
        previous_memento = self._undo_stack.pop()
        return previous_memento.get_history()
    
    def redo(self, current_history: List[Calculation]) -> List[Calculation]:
        """Restore next state from redo stack."""
        if not self._redo_stack:
            return current_history
        
        # Save current state to undo stack
        current_memento = CalculatorMemento(current_history)
        self._undo_stack.append(current_memento)
        
        # Restore next state
        next_memento = self._redo_stack.pop()
        return next_memento.get_history()
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return len(self._undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return len(self._redo_stack) > 0

