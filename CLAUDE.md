# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Test Commands

- Install dependencies: `make install` or `poetry install`
- Create virtual environment: `make venv` or `python3 -m venv venv`
- Format code: `make format` or `poetry run black . && poetry run isort .`
- Lint code: `make lint` or `poetry run flake8 . && poetry run mypy .`
- Type check: `make typecheck` or `poetry run mypy .`
- Run all tests: `make test` or `poetry run pytest tests/`
- Run single test file: `make test-file FILE=tests/test_file.py` or `poetry run pytest tests/test_file.py -v`
- Run single test function: `make test-function FILE=tests/test_file.py::test_function` or `poetry run pytest tests/test_file.py::TestClass::test_method -v`
- Run tests in exercises: `cd exercises && poetry run pytest test_file.py`

## Code Style Guidelines

- Use Python 3.11+ features and syntax
- Follow PEP 8 style guidelines with Black (line-length=88) and isort
- Use strict type hints throughout (mypy with disallow_untyped_defs=true)
- Use snake_case for variables/functions, PascalCase for classes
- Organize imports: standard library, third-party, local
- Include docstrings for all modules, classes, and functions
- Use context managers for resource handling
- Raise specific exceptions with descriptive messages
- Validate input parameters with assertions or value checks
- Structure code using modules and packages appropriately

## Language Implementation Notes

The repository includes a simple language implementation with lexer, parser, and evaluator supporting functional programming constructs and reflection capabilities.