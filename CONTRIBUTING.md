# Contributing to nprime

Thank you for your interest in contributing to nprime! This guide will help you set up your development environment and understand the contribution process.

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sylhare/nprime.git
   cd nprime
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   # Install the package in development mode
   pip install -e .
   
   # Install development dependencies
   pip install -r requirements.txt
   ```

## 🧪 Running Tests

### Run all tests
```bash
# Using unittest (recommended)
python -m unittest discover tests/ -v

# Run specific test file
python -m unittest tests.test_pyprime -v

# Run specific test
python -m unittest tests.test_pyprime.TestPyPrime.test_001_is_zero_not_prime -v
```

### Test Coverage
```bash
# Run tests with coverage
python -m pytest tests/ --cov=nprime --cov-report=html --cov-report=term-missing

# View coverage report
open htmlcov/index.html  # macOS
# or
start htmlcov/index.html  # Windows
```
