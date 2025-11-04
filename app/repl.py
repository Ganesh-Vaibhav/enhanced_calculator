"""
REPL (Read-Eval-Print Loop) interface for the calculator.
"""

import sys
from typing import Optional
from colorama import init, Fore, Style
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import CalculatorError, OperationError, ValidationError
from app.operations import OperationFactory


# Initialize colorama
init(autoreset=True)


class HelpMenuDecorator:
    """Decorator pattern for dynamic help menu generation."""
    
    def __init__(self, calculator: Calculator):
        """Initialize with calculator instance."""
        self.calculator = calculator
    
    def generate_help(self) -> str:
        """Generate help menu dynamically based on available operations."""
        help_text = f"\n{Fore.CYAN}{Style.BRIGHT}=== Calculator Help ==={Style.RESET_ALL}\n\n"
        
        # Get available operations
        operations = OperationFactory.get_available_operations()
        
        help_text += f"{Fore.YELLOW}Available Operations:{Style.RESET_ALL}\n"
        for op in operations:
            help_text += f"  {Fore.GREEN}{op}{Style.RESET_ALL} - Perform {op} operation\n"
        
        help_text += f"\n{Fore.YELLOW}History Commands:{Style.RESET_ALL}\n"
        help_text += f"  {Fore.GREEN}history{Style.RESET_ALL} - Display calculation history\n"
        help_text += f"  {Fore.GREEN}clear{Style.RESET_ALL} - Clear calculation history\n"
        help_text += f"  {Fore.GREEN}undo{Style.RESET_ALL} - Undo the last calculation\n"
        help_text += f"  {Fore.GREEN}redo{Style.RESET_ALL} - Redo the last undone calculation\n"
        
        help_text += f"\n{Fore.YELLOW}File Commands:{Style.RESET_ALL}\n"
        help_text += f"  {Fore.GREEN}save{Style.RESET_ALL} - Manually save calculation history to file\n"
        help_text += f"  {Fore.GREEN}load{Style.RESET_ALL} - Load calculation history from file\n"
        
        help_text += f"\n{Fore.YELLOW}Other Commands:{Style.RESET_ALL}\n"
        help_text += f"  {Fore.GREEN}help{Style.RESET_ALL} - Display this help menu\n"
        help_text += f"  {Fore.GREEN}exit{Style.RESET_ALL} - Exit the application\n"
        
        help_text += f"\n{Fore.CYAN}Usage Example:{Style.RESET_ALL}\n"
        help_text += f"  {Fore.WHITE}add 5 3{Style.RESET_ALL} - Adds 5 and 3\n"
        help_text += f"  {Fore.WHITE}power 2 8{Style.RESET_ALL} - Calculates 2 to the power of 8\n\n"
        
        return help_text


class CalculatorREPL:
    """REPL interface for calculator."""
    
    def __init__(self, calculator: Calculator):
        """Initialize REPL with calculator instance."""
        self.calculator = calculator
        self.help_decorator = HelpMenuDecorator(calculator)
        self.running = True
    
    def print_welcome(self):
        """Print welcome message."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Enhanced Calculator ==={Style.RESET_ALL}")
        print(f"{Fore.GREEN}Type 'help' for available commands{Style.RESET_ALL}\n")
    
    def print_error(self, message: str):
        """Print error message in red."""
        print(f"{Fore.RED}Error: {message}{Style.RESET_ALL}")
    
    def print_success(self, message: str):
        """Print success message in green."""
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
    
    def print_info(self, message: str):
        """Print info message in yellow."""
        print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
    
    def handle_calculation(self, operation: str, args: list):
        """Handle calculation command."""
        if len(args) < 2:
            self.print_error("Calculation requires two operands")
            return
        
        try:
            operand1 = float(args[0])
            operand2 = float(args[1])
            result = self.calculator.calculate(operation, operand1, operand2)
            print(f"{Fore.CYAN}Result: {result}{Style.RESET_ALL}")
        except (ValueError, ValidationError) as e:
            self.print_error(f"Invalid input: {str(e)}")
        except OperationError as e:
            self.print_error(str(e))
        except CalculatorError as e:
            self.print_error(str(e))
    
    def handle_history(self):
        """Handle history command."""
        history = self.calculator.get_history()
        if not history:
            self.print_info("No calculation history")
            return
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Calculation History ==={Style.RESET_ALL}")
        for i, calc in enumerate(history, 1):
            print(
                f"{Fore.WHITE}{i}. {calc.operand1} {calc.operation} "
                f"{calc.operand2} = {Fore.GREEN}{calc.result}{Style.RESET_ALL} "
                f"({calc.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"
            )
        print()
    
    def handle_save(self):
        """Handle save command."""
        try:
            file_path = self.calculator.save_history()
            self.print_success(f"History saved to {file_path}")
        except Exception as e:
            self.print_error(f"Failed to save history: {str(e)}")
    
    def handle_load(self):
        """Handle load command."""
        try:
            calculations = self.calculator.load_history()
            self.print_success(f"Loaded {len(calculations)} calculations from history")
        except Exception as e:
            self.print_error(f"Failed to load history: {str(e)}")
    
    def handle_undo(self):
        """Handle undo command."""
        if self.calculator.undo():
            self.print_success("Undo successful")
        else:
            self.print_error("Nothing to undo")
    
    def handle_redo(self):
        """Handle redo command."""
        if self.calculator.redo():
            self.print_success("Redo successful")
        else:
            self.print_error("Nothing to redo")
    
    def process_command(self, command: str):
        """Process a command."""
        parts = command.strip().split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Check if it's an operation
        available_ops = OperationFactory.get_available_operations()
        if cmd in available_ops:
            self.handle_calculation(cmd, args)
            return
        
        # Handle other commands
        if cmd == 'exit' or cmd == 'quit':
            self.running = False
            self.print_info("Goodbye!")
        elif cmd == 'help':
            print(self.help_decorator.generate_help())
        elif cmd == 'history':
            self.handle_history()
        elif cmd == 'clear':
            self.calculator.clear_history()
            self.print_success("History cleared")
        elif cmd == 'undo':
            self.handle_undo()
        elif cmd == 'redo':
            self.handle_redo()
        elif cmd == 'save':
            self.handle_save()
        elif cmd == 'load':
            self.handle_load()
        else:
            self.print_error(f"Unknown command: {cmd}. Type 'help' for available commands.")
    
    def run(self):
        """Run the REPL loop."""
        self.print_welcome()
        
        while self.running:
            try:
                command = input(f"{Fore.CYAN}calc> {Style.RESET_ALL}")
                self.process_command(command)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use 'exit' to quit{Style.RESET_ALL}")
            except EOFError:
                self.running = False
                self.print_info("Goodbye!")
            except Exception as e:
                self.print_error(f"Unexpected error: {str(e)}")


def main():
    """Main entry point for the calculator REPL."""
    try:
        config = CalculatorConfig()
        calculator = Calculator(config)
        repl = CalculatorREPL(calculator)
        repl.run()
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()

