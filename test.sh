#!/bin/bash
# Test runner script

echo "🧪 Running Bluetooth Scanner tests..."

# Install test dependencies
echo "📦 Installing test dependencies..."
pip install -r requirements-dev.txt

# Run tests with coverage
echo "🔍 Running tests with coverage..."
python -m pytest tests/ -v --cov=bluetooth_scanner --cov-report=html --cov-report=term

# Run linting
echo "🔍 Running code quality checks..."
echo "Running flake8..."
flake8 bluetooth_scanner.py tests/ --max-line-length=100

echo "Running mypy..."
mypy bluetooth_scanner.py --ignore-missing-imports

echo "✅ All tests and checks completed!"
