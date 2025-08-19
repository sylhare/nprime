# Contributing to nprime

Thank you for your interest in contributing to nprime! This guide will help you set up your development environment and understand the contribution process.

## 🚀 Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and development workflows.

### Prerequisites

- Python 3.9 or higher
- Git
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Setup Development Environment

1. **Install uv** if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/Sylhare/nprime.git
   cd nprime
   ```

3. **Set up the development environment**:
   ```bash
   uv sync --extra dev --extra test --extra coverage
   ```

## 🧪 Running Tests

### Basic Testing
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_pyprime.py

# Run with verbose output
uv run pytest -v

# Run tests matching a pattern
uv run pytest -k "test_prime"
```

### Test Coverage
```bash
# Generate coverage report
uv run pytest --cov=nprime.pyprime --cov-report=term-missing

# Generate HTML coverage report
uv run pytest --cov=nprime.pyprime --cov-report=html

# View coverage report (HTML)
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```
