# Quick Setup Guide

## Initial Setup

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file**:
   Create a `.env` file in the project root with the following content:
   ```env
   CALCULATOR_LOG_DIR=logs
   CALCULATOR_HISTORY_DIR=history
   CALCULATOR_MAX_HISTORY_SIZE=100
   CALCULATOR_AUTO_SAVE=true
   CALCULATOR_PRECISION=10
   CALCULATOR_MAX_INPUT_VALUE=1e308
   CALCULATOR_DEFAULT_ENCODING=utf-8
   ```

4. **Run the calculator**:
   ```bash
   python main.py
   ```

5. **Run tests**:
   ```bash
   pytest --cov=app --cov-report=term --cov-fail-under=90
   ```

## Git Initial Setup

If you haven't initialized Git yet:
```bash
git init
git add .
git commit -m "Initial commit: Enhanced calculator with all required features"
```

## Features Implemented

✅ All required arithmetic operations (power, root, modulus, int_divide, percent, abs_diff)
✅ Factory Design Pattern for operations
✅ Memento Pattern for undo/redo
✅ Observer Pattern for logging and auto-save
✅ Configuration management with .env
✅ Input validation and error handling
✅ Comprehensive logging
✅ REPL interface with color-coded output
✅ Dynamic help menu with Decorator pattern
✅ Data persistence with pandas (CSV)
✅ Comprehensive unit tests
✅ GitHub Actions CI workflow

