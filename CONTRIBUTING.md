# Contributing to Bluetooth Scanner

Thank you for your interest in contributing to Bluetooth Scanner! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Setting up Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ussdeveloper/bluetooth-scanner.git
   cd bluetooth-scanner
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\activate
   
   # On Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### Running Tests

Run all tests:
```bash
# Windows
test.bat

# Linux/macOS
./test.sh
```

Run specific tests:
```bash
pytest tests/test_bluetooth_scanner.py::TestBluetoothScanner::test_get_manufacturer_name -v
```

### Code Quality

We use several tools to maintain code quality:

- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking
- **Pytest** for testing

Run quality checks:
```bash
# Format code
black bluetooth_scanner.py tests/

# Check linting
flake8 bluetooth_scanner.py tests/ --max-line-length=100

# Type checking
mypy bluetooth_scanner.py --ignore-missing-imports
```

### Building Binaries

Create standalone executables:
```bash
# Windows
build.bat

# Linux/macOS
./build.sh
```

## Contributing Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep lines under 100 characters
- Use type hints where appropriate

### Commit Messages

Use clear and descriptive commit messages:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when applicable

Examples:
```
Add support for device filtering by manufacturer
Fix PDF generation for devices with long names
Update README with installation instructions
```

### Pull Request Process

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the coding guidelines
3. **Add tests** for any new functionality
4. **Run tests** and ensure they pass
5. **Update documentation** if needed
6. **Submit a pull request** with a clear description

### Testing

- Write tests for all new features
- Ensure existing tests still pass
- Aim for high test coverage
- Test on both Windows and Linux if possible

### Bug Reports

When reporting bugs, include:
- Operating system and version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs
- Screenshots if applicable

### Feature Requests

For new features:
- Explain the use case
- Describe the expected behavior
- Consider backwards compatibility
- Discuss implementation approach

## Project Structure

```
bluetooth-scanner/
├── bluetooth_scanner.py    # Main scanner module
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Development dependencies
├── tests/                  # Test files
│   ├── conftest.py        # Test configuration
│   └── test_bluetooth_scanner.py
├── build.bat              # Windows build script
├── build.sh               # Linux/macOS build script
├── test.bat               # Windows test runner
├── test.sh                # Linux/macOS test runner
├── setup.py               # Package setup
├── pytest.ini            # Pytest configuration
├── LICENSE                # MIT License
├── README.md              # Project documentation
└── CONTRIBUTING.md        # This file
```

## Release Process

1. Update version in `setup.py`
2. Update `README.md` with new features
3. Create and push git tag
4. Build and test binaries
5. Create GitHub release
6. Upload binaries to release

## Questions?

If you have questions about contributing, please:
- Check existing issues and discussions
- Create a new issue for discussion
- Contact the maintainers

Thank you for contributing to Bluetooth Scanner!
