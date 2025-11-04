# Enhanced Calculator Application

A comprehensive calculator application with advanced features including history management, undo/redo functionality, observer pattern for logging and auto-save, and multiple design patterns.

## Features

### Core Functionality
- **Additional Arithmetic Operations**: Power, Root, Modulus, Integer Division, Percentage, and Absolute Difference
- **Factory Design Pattern**: Dynamic operation creation
- **History Management**: Track all calculations with timestamps
- **Undo/Redo Functionality**: Memento Design Pattern for state management
- **Observer Pattern**: Automatic logging and CSV auto-save
- **Configuration Management**: Environment-based configuration using `.env` file
- **Input Validation**: Robust error handling and validation
- **Comprehensive Logging**: File and console logging
- **REPL Interface**: User-friendly command-line interface with color-coded output
- **Data Persistence**: Save and load history using pandas (CSV format)

### Optional Features
- **Dynamic Help Menu**: Decorator Pattern for automatically generating help based on available operations
- **Color-Coded Output**: Enhanced user experience with Colorama

## Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup Steps

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd enhanced_calculator
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**:
   Copy the example configuration and customize as needed:
   ```bash
   cp .env.example .env
   ```
   
   Or create a `.env` file with the following content:
   ```env
   # Base Directories
   CALCULATOR_LOG_DIR=logs
   CALCULATOR_HISTORY_DIR=history
   
   # History Settings
   CALCULATOR_MAX_HISTORY_SIZE=100
   CALCULATOR_AUTO_SAVE=true
   
   # Calculation Settings
   CALCULATOR_PRECISION=10
   CALCULATOR_MAX_INPUT_VALUE=1e308
   CALCULATOR_DEFAULT_ENCODING=utf-8
   ```

## Configuration

The application uses environment variables loaded from a `.env` file. Available configuration options:

### Base Directories
- `CALCULATOR_LOG_DIR`: Directory for log files (default: `logs`)
- `CALCULATOR_HISTORY_DIR`: Directory for history files (default: `history`)

### History Settings
- `CALCULATOR_MAX_HISTORY_SIZE`: Maximum number of history entries (default: `100`)
- `CALCULATOR_AUTO_SAVE`: Whether to auto-save history after each calculation (default: `true`)

### Calculation Settings
- `CALCULATOR_PRECISION`: Number of decimal places for calculations (default: `10`)
- `CALCULATOR_MAX_INPUT_VALUE`: Maximum allowed input value (default: `1e308`)
- `CALCULATOR_DEFAULT_ENCODING`: Default encoding for file operations (default: `utf-8`)

## Usage

### Running the Calculator

Start the calculator REPL interface:
```bash
python -m app.repl
```

Or if you have a main entry point:
```bash
python main.py
```

### Available Commands

#### Arithmetic Operations
- `add <num1> <num2>` - Addition
- `subtract <num1> <num2>` - Subtraction
- `multiply <num1> <num2>` - Multiplication
- `divide <num1> <num2>` - Division
- `power <base> <exponent>` - Raise base to the power of exponent
- `root <number> <degree>` - Calculate nth root
- `modulus <num1> <num2>` - Remainder of division
- `int_divide <num1> <num2>` - Integer division
- `percent <num1> <num2>` - Calculate percentage (num1 / num2 * 100)
- `abs_diff <num1> <num2>` - Absolute difference between two numbers

#### History Commands
- `history` - Display calculation history
- `clear` - Clear calculation history
- `undo` - Undo the last calculation
- `redo` - Redo the last undone calculation

#### File Commands
- `save` - Manually save calculation history to CSV file
- `load` - Load calculation history from CSV file

#### Other Commands
- `help` - Display help menu with all available commands
- `exit` or `quit` - Exit the application

### Example Usage

```
calc> add 5 3
Result: 8.0

calc> power 2 8
Result: 256.0

calc> percent 25 100
Result: 25.0

calc> history
=== Calculation History ===
1. 5.0 add 3.0 = 8.0 (2024-01-01 12:00:00)
2. 2.0 power 8.0 = 256.0 (2024-01-01 12:00:05)
3. 25.0 percent 100.0 = 25.0 (2024-01-01 12:00:10)

calc> undo
Undo successful

calc> exit
Goodbye!
```

## Testing

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app --cov-report=term
```

Run tests with coverage and enforce 90% threshold:
```bash
pytest --cov=app --cov-report=term --cov-fail-under=90
```

### Test Coverage

The project aims for 90% or better test coverage. Coverage reports are generated using `pytest-cov`. To exclude specific lines from coverage (e.g., error handlers that are hard to test), use the `# pragma: no cover` comment.

## Project Structure

```
project_root/
├── app/
│   ├── __init__.py
│   ├── calculator.py          # Main calculator class with Observer pattern
│   ├── calculation.py         # Calculation data model
│   ├── calculator_config.py   # Configuration management
│   ├── calculator_memento.py  # Memento pattern for undo/redo
│   ├── exceptions.py          # Custom exceptions
│   ├── history.py             # History management with pandas
│   ├── input_validators.py    # Input validation
│   ├── operations.py          # Operations with Factory pattern
│   ├── logger.py              # Logging configuration
│   └── repl.py                # REPL interface
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_calculation.py
│   ├── test_operations.py
│   ├── test_input_validators.py
│   ├── test_history.py
│   └── test_calculator_memento.py
├── .env.example               # Example environment configuration
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── .github/
    └── workflows/
        └── python-app.yml     # GitHub Actions CI workflow
```

## Design Patterns

### Factory Pattern
Used in `operations.py` to create operation instances dynamically based on operation names.

### Memento Pattern
Implemented in `calculator_memento.py` to support undo/redo functionality by storing calculator state snapshots.

### Observer Pattern
Used in `calculator.py` to notify observers (LoggingObserver, AutoSaveObserver) when calculations are performed.

### Decorator Pattern
Implemented in `repl.py` for dynamically generating help menus based on available operations.

## CI/CD

The project includes a GitHub Actions workflow (`.github/workflows/python-app.yml`) that:
- Runs on every push and pull request to the main branch
- Sets up Python environment
- Installs dependencies
- Runs tests with coverage measurement
- Enforces 90% test coverage threshold

## Logging

Logs are written to the file specified in `CALCULATOR_LOG_FILE` (default: `logs/calculator.log`). Logs include:
- Calculation details (operation, operands, result)
- Error messages
- History operations (clear, undo, redo)
- File operations (save, load)

## Error Handling

The application includes comprehensive error handling:
- **OperationError**: Raised when operations cannot be performed (e.g., division by zero)
- **ValidationError**: Raised when input validation fails
- **HistoryError**: Raised when history operations fail
- **ConfigurationError**: Raised when configuration is invalid

All errors are logged and displayed to the user with helpful messages.

## Contributing

1. Make sure you have a clear commit history showing your development process
2. Write tests for new features
3. Ensure test coverage remains above 90%
4. Follow the existing code style and structure

## License

This project is part of an academic assignment.

## Notes

- The application requires a `.env` file for configuration. Create one based on `.env.example`
- Log and history directories are created automatically if they don't exist
- History is automatically saved to CSV when `CALCULATOR_AUTO_SAVE` is enabled
- Use `# pragma: no cover` comments for lines intentionally excluded from coverage

