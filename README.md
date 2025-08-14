# Autotests API

A comprehensive API testing framework built with Python, designed for automated testing of web APIs with advanced reporting and coverage measurement capabilities.

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [API Coverage](#api-coverage)
- [Reports](#reports)
- [Development](#development)
- [Project Structure](#project-structure)

## Tech Stack

- **Python 3.12** - Programming language
- **pytest** - Testing framework
- **httpx** - Modern HTTP client library
- **pydantic** - Data validation and serialization
- **pydantic-settings** - Configuration management
- **allure-pytest** - Advanced test reporting
- **swagger-coverage-tool** - API coverage measurement
- **ruff** - Fast Python linter and formatter
- **pytest-xdist** - Parallel test execution
- **pytest-rerunfailures** - Test retry functionality
- **Faker** - Test data generation

## Project Architecture

The framework follows a multi-layered architecture for HTTP clients:

### 1. Base HTTP Builders
- `public_http_builder.py` - Creates public httpx.Client without authentication
- `private_http_builder.py` - Creates private httpx.Client with Bearer token authentication

### 2. Base API Client (`api_client.py`)
- Wrapper around httpx.Client with Allure step decorators
- Provides standardized GET, POST, PATCH, DELETE methods
- Automatic request/response logging

### 3. Specialized Clients
Each domain has its own client in `clients/*/` folders:
- Authentication - login and token management
- Users - user management operations
- Courses - course-related endpoints
- Exercises - exercise management
- Files - file upload/download operations

All clients use pydantic schemas for data validation and are separated into public and private endpoints.

### 4. Fixtures System
Organized fixtures in `fixtures/` folder:
- `authentication.py` - authentication client setup
- `users.py` - user data management
- `courses.py`, `exercises.py`, `files.py` - domain-specific fixtures
- `allure.py` - Allure report configuration

### 5. Assertion Utilities
Specialized assertion functions in `tools/assertions/`:
- `base.py` - basic assertions (status code, equality, length)
- `schema.py` - JSON schema validation
- Domain-specific assertions for each API module

## Installation

### Requirements
- Python 3.12+
- macOS (Apple Silicon supported)

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd autotests-api
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables
Configure the `.env` file with your specific values. Replace the example values with your actual configuration:

- HTTP client settings (URL, timeout)
- Test data file paths
- Swagger coverage configuration

### Settings
The project uses `pydantic-settings` for configuration management. See `config.py` for available settings:
- HTTP client configuration (URL, timeout)
- Test data paths
- Allure results directory

## Running Tests

### Basic Commands
```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific module tests
pytest tests/authentication/

# Run tests in parallel
pytest -n auto

# Run tests with retries on failure
pytest --reruns 2
```

### Test Markers
Use pytest markers to run specific test categories:

```bash
# Run by domain
pytest -m authentication
pytest -m users
pytest -m files
pytest -m courses
pytest -m exercises

# Run by test type
pytest -m smoke          # Smoke tests
pytest -m regression     # Regression tests

# Combine markers
pytest -m "authentication and regression"
```

Available markers:
- `authentication` - Authentication-related tests
- `users` - User management tests
- `files` - File operations tests
- `courses` - Course management tests
- `exercises` - Exercise management tests
- `regression` - Regression test suite
- `smoke` - Smoke test suite

## API Coverage

The project uses [swagger-coverage-tool](https://github.com/viclovsky/swagger-coverage) to measure API coverage:

### Features
- Tracks which API endpoints are covered by tests
- Generates detailed coverage reports
- Identifies untested API paths and methods
- Integrates with CI/CD pipelines

### Usage
API coverage is automatically tracked during test execution through decorators in client classes. Coverage results are stored in `coverage-results/` directory.

### Generating Coverage Reports
Coverage reports are automatically generated and can be found in:
- `coverage-report.json` - Latest coverage summary
- `coverage-history.json` - Historical coverage data
- `coverage-results/` - Detailed coverage files

## Reports

### Allure Reports
Generate and view Allure reports:

```bash
# Generate and serve Allure report
allure serve allure-results
```


## Development

### Code Quality
The project uses Ruff for linting and formatting:

```bash
# Check code with linter
ruff check

# Automatically fix linting issues
ruff check --fix

# Format code
ruff format
```

### Configuration
- **Line length**: 100 characters
- **Target Python version**: 3.12
- **Code style**: Similar to Black formatter
- **Import sorting**: isort-compatible

### Adding New Tests
1. Create test files in the appropriate `tests/` subdirectory
2. Use appropriate pytest markers
3. Follow the existing test structure with Allure annotations
4. Create domain-specific fixtures and assertions as needed

### Adding New API Clients
1. Create client directory in `clients/`
2. Implement client class inheriting from `APIClient`
3. Create pydantic schemas for request/response validation
4. Add appropriate fixtures
5. Create domain-specific assertion utilities

## Project Structure

```
autotests-api/
├── clients/                    # API client implementations
│   ├── api_client.py          # Base API client
│   ├── authentication/        # Authentication client
│   ├── courses/               # Courses client
│   ├── exercises/             # Exercises client
│   ├── files/                 # Files client
│   ├── users/                 # Users client
│   └── ...
├── fixtures/                  # Pytest fixtures
│   ├── authentication.py
│   ├── users.py
│   └── ...
├── tests/                     # Test modules
│   ├── authentication/
│   ├── courses/
│   ├── exercises/
│   ├── files/
│   ├── users/
│   └── ...
├── tools/                     # Utility modules
│   ├── allure/               # Allure constants
│   ├── assertions/           # Custom assertions
│   ├── http/                 # HTTP utilities
│   └── ...
├── testdata/                 # Test data files
├── config.py                 # Application configuration
├── conftest.py              # Pytest configuration
├── pytest.ini              # Pytest settings
├── pyproject.toml           # Ruff configuration
├── requirements.txt         # Python dependencies
└── CLAUDE.md               # Claude Code instructions
```

