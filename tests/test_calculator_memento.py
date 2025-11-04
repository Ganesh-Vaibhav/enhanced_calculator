"""
Tests for memento pattern implementation.
"""

from app.calculator_memento import CalculatorMemento, CalculatorCaretaker
from app.calculation import Calculation


class TestCalculatorMemento:
    """Tests for CalculatorMemento class."""
    
    def test_memento_creation(self):
        """Test creating a memento."""
        history = [Calculation('add', 5, 3, 8)]
        memento = CalculatorMemento(history)
        assert len(memento.get_history()) == 1
    
    def test_memento_isolation(self):
        """Test that memento creates a copy."""
        history = [Calculation('add', 5, 3, 8)]
        memento = CalculatorMemento(history)
        history.append(Calculation('multiply', 2, 4, 8))
        assert len(memento.get_history()) == 1


class TestCalculatorCaretaker:
    """Tests for CalculatorCaretaker class."""
    
    def test_save_state(self):
        """Test saving state."""
        caretaker = CalculatorCaretaker()
        history = [Calculation('add', 5, 3, 8)]
        caretaker.save_state(history)
        assert caretaker.can_undo()
    
    def test_undo(self):
        """Test undo functionality."""
        caretaker = CalculatorCaretaker()
        history1 = [Calculation('add', 5, 3, 8)]
        history2 = [Calculation('add', 5, 3, 8), Calculation('multiply', 2, 4, 8)]
        
        caretaker.save_state(history1)
        caretaker.save_state(history2)
        
        restored = caretaker.undo(history2)
        assert len(restored) == 1
    
    def test_redo(self):
        """Test redo functionality."""
        caretaker = CalculatorCaretaker()
        history1 = [Calculation('add', 5, 3, 8)]
        history2 = [Calculation('add', 5, 3, 8), Calculation('multiply', 2, 4, 8)]
        
        caretaker.save_state(history1)
        caretaker.save_state(history2)
        caretaker.undo(history2)
        
        restored = caretaker.redo(history1)
        assert len(restored) == 2
    
    def test_redo_cleared_on_new_action(self):
        """Test that redo is cleared on new action."""
        caretaker = CalculatorCaretaker()
        history1 = [Calculation('add', 5, 3, 8)]
        history2 = [Calculation('add', 5, 3, 8), Calculation('multiply', 2, 4, 8)]
        history3 = [Calculation('subtract', 10, 3, 7)]
        
        caretaker.save_state(history1)
        caretaker.save_state(history2)
        caretaker.undo(history2)
        assert caretaker.can_redo()
        
        caretaker.save_state(history3)
        assert not caretaker.can_redo()
    
    def test_can_undo(self):
        """Test can_undo method."""
        caretaker = CalculatorCaretaker()
        assert not caretaker.can_undo()
        
        caretaker.save_state([Calculation('add', 5, 3, 8)])
        assert caretaker.can_undo()
    
    def test_can_redo(self):
        """Test can_redo method."""
        caretaker = CalculatorCaretaker()
        assert not caretaker.can_redo()
        
        history1 = [Calculation('add', 5, 3, 8)]
        history2 = [Calculation('multiply', 2, 4, 8)]
        caretaker.save_state(history1)
        caretaker.save_state(history2)
        caretaker.undo(history2)
        assert caretaker.can_redo()

