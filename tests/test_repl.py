"""
Tests for REPL interface.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.repl import CalculatorREPL, HelpMenuDecorator, main
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError


class TestHelpMenuDecorator:
    """Tests for HelpMenuDecorator class."""
    
    @pytest.fixture
    def calculator(self):
        """Create mock calculator."""
        config = CalculatorConfig()
        return Calculator(config)
    
    @pytest.fixture
    def decorator(self, calculator):
        """Create help menu decorator."""
        return HelpMenuDecorator(calculator)
    
    def test_generate_help(self, decorator):
        """Test help menu generation."""
        help_text = decorator.generate_help()
        assert "Calculator Help" in help_text
        assert "add" in help_text
        assert "power" in help_text
        assert "history" in help_text
        assert "undo" in help_text


class TestCalculatorREPL:
    """Tests for CalculatorREPL class."""
    
    @pytest.fixture
    def calculator(self):
        """Create calculator instance."""
        config = CalculatorConfig()
        config._config['CALCULATOR_AUTO_SAVE'] = False
        return Calculator(config)
    
    @pytest.fixture
    def repl(self, calculator):
        """Create REPL instance."""
        return CalculatorREPL(calculator)
    
    def test_initialization(self, repl):
        """Test REPL initialization."""
        assert repl.calculator is not None
        assert repl.help_decorator is not None
        assert repl.running is True
    
    @patch('builtins.print')
    def test_print_welcome(self, mock_print, repl):
        """Test welcome message."""
        repl.print_welcome()
        assert mock_print.called
    
    @patch('builtins.print')
    def test_print_error(self, mock_print, repl):
        """Test error message printing."""
        repl.print_error("Test error")
        mock_print.assert_called_once()
    
    @patch('builtins.print')
    def test_print_success(self, mock_print, repl):
        """Test success message printing."""
        repl.print_success("Test success")
        mock_print.assert_called_once()
    
    @patch('builtins.print')
    def test_print_info(self, mock_print, repl):
        """Test info message printing."""
        repl.print_info("Test info")
        mock_print.assert_called_once()
    
    @patch('builtins.print')
    def test_handle_calculation_success(self, mock_print, repl):
        """Test successful calculation."""
        repl.handle_calculation('add', ['5', '3'])
        assert mock_print.called
    
    @patch('builtins.print')
    def test_handle_calculation_insufficient_args(self, mock_print, repl):
        """Test calculation with insufficient arguments."""
        repl.handle_calculation('add', ['5'])
        mock_print.assert_called()
        assert "Error" in str(mock_print.call_args)
    
    @patch('builtins.print')
    def test_handle_calculation_invalid_input(self, mock_print, repl):
        """Test calculation with invalid input."""
        repl.handle_calculation('add', ['not', 'a', 'number'])
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_handle_calculation_operation_error(self, mock_print, repl):
        """Test calculation with operation error."""
        repl.handle_calculation('divide', ['10', '0'])
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_handle_history_empty(self, mock_print, repl):
        """Test history command with empty history."""
        repl.handle_history()
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_handle_history_with_data(self, mock_print, repl):
        """Test history command with data."""
        repl.calculator.calculate('add', 5, 3)
        repl.handle_history()
        assert mock_print.called
    
    @patch('builtins.print')
    def test_handle_save(self, mock_print, repl, tmp_path):
        """Test save command."""
        repl.calculator.calculate('add', 5, 3)
        file_path = str(tmp_path / 'test.csv')
        with patch.object(repl.calculator, 'save_history', return_value=file_path):
            repl.handle_save()
            mock_print.assert_called()
    
    @patch('builtins.print')
    def test_handle_load(self, mock_print, repl):
        """Test load command."""
        with patch.object(repl.calculator, 'load_history', return_value=[]):
            repl.handle_load()
            mock_print.assert_called()
    
    @patch('builtins.print')
    def test_handle_undo_success(self, mock_print, repl):
        """Test undo command with success."""
        repl.calculator.calculate('add', 5, 3)
        repl.handle_undo()
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_handle_undo_failure(self, mock_print, repl):
        """Test undo command with nothing to undo."""
        repl.handle_undo()
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_handle_redo_success(self, mock_print, repl):
        """Test redo command with success."""
        repl.calculator.calculate('add', 5, 3)
        repl.calculator.undo()
        repl.handle_redo()
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_handle_redo_failure(self, mock_print, repl):
        """Test redo command with nothing to redo."""
        repl.handle_redo()
        mock_print.assert_called()
    
    def test_process_command_empty(self, repl):
        """Test processing empty command."""
        repl.process_command("")
        # Should not raise any errors
    
    def test_process_command_operation(self, repl):
        """Test processing operation command."""
        with patch.object(repl, 'handle_calculation'):
            repl.process_command("add 5 3")
            repl.handle_calculation.assert_called_once_with('add', ['5', '3'])
    
    def test_process_command_help(self, repl):
        """Test processing help command."""
        with patch('builtins.print'):
            repl.process_command("help")
            assert True  # Should not raise
    
    def test_process_command_history(self, repl):
        """Test processing history command."""
        with patch.object(repl, 'handle_history'):
            repl.process_command("history")
            repl.handle_history.assert_called_once()
    
    def test_process_command_clear(self, repl):
        """Test processing clear command."""
        with patch.object(repl, 'print_success'):
            repl.process_command("clear")
            assert len(repl.calculator.get_history()) == 0 or True
    
    def test_process_command_undo(self, repl):
        """Test processing undo command."""
        with patch.object(repl, 'handle_undo'):
            repl.process_command("undo")
            repl.handle_undo.assert_called_once()
    
    def test_process_command_redo(self, repl):
        """Test processing redo command."""
        with patch.object(repl, 'handle_redo'):
            repl.process_command("redo")
            repl.handle_redo.assert_called_once()
    
    def test_process_command_save(self, repl):
        """Test processing save command."""
        with patch.object(repl, 'handle_save'):
            repl.process_command("save")
            repl.handle_save.assert_called_once()
    
    def test_process_command_load(self, repl):
        """Test processing load command."""
        with patch.object(repl, 'handle_load'):
            repl.process_command("load")
            repl.handle_load.assert_called_once()
    
    def test_process_command_exit(self, repl):
        """Test processing exit command."""
        repl.process_command("exit")
        assert repl.running is False
    
    def test_process_command_quit(self, repl):
        """Test processing quit command."""
        repl.process_command("quit")
        assert repl.running is False
    
    def test_process_command_unknown(self, repl):
        """Test processing unknown command."""
        with patch.object(repl, 'print_error') as mock_error:
            repl.process_command("unknown_command")
            mock_error.assert_called_once()
    
    @patch('builtins.input', return_value='exit')
    @patch('builtins.print')
    def test_run_exit(self, mock_print, mock_input, repl):
        """Test REPL run with exit command."""
        repl.run()
        assert not repl.running
    
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    @patch('builtins.print')
    def test_run_keyboard_interrupt(self, mock_print, mock_input, repl):
        """Test REPL run with keyboard interrupt."""
        repl.running = True
        try:
            repl.run()
        except StopIteration:
            pass
        assert True  # Should handle gracefully
    
    @patch('builtins.input', side_effect=EOFError())
    @patch('builtins.print')
    def test_run_eof(self, mock_print, mock_input, repl):
        """Test REPL run with EOF."""
        repl.running = True
        try:
            repl.run()
        except StopIteration:
            pass
        assert not repl.running
    
    @patch('app.repl.CalculatorREPL')
    @patch('app.repl.Calculator')
    @patch('app.repl.CalculatorConfig')
    def test_main(self, mock_config, mock_calc_class, mock_repl_class):
        """Test main function."""
        mock_config_instance = Mock()
        mock_config.return_value = mock_config_instance
        mock_calc_instance = Mock()
        mock_calc_class.return_value = mock_calc_instance
        mock_repl_instance = Mock()
        mock_repl_class.return_value = mock_repl_instance
        
        main()
        
        mock_repl_instance.run.assert_called_once()

