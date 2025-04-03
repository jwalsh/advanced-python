# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Test Commands

- Install dependencies: `make install` or `poetry install`
- Create virtual environment: `make venv` or `python3 -m venv venv`
- Lint code: `make lint` or `poetry run flake8 .`
- Format code: `poetry run black .` and `poetry run isort .`
- Run all tests: `make test` or `poetry run pytest tests/`
- Run single test: `poetry run pytest tests/test_file.py::TestClass::test_method -v`
- Run tests in exercises: `cd exercises && poetry run pytest test_file.py`

## Code Style Guidelines

- Use Python 3.11+ features and syntax
- Follow PEP 8 style guidelines
- Use Black for code formatting and isort for import sorting
- Use type hints for function parameters and return values
- Use docstrings for all classes and functions
- Organize imports: standard library, third-party, local
- Use snake_case for variables and functions, PascalCase for classes
- Prefer context managers for file handling
- Use proper error handling with specific exceptions
- Organize code using modules and packages appropriately

## Documentation Standards

- Include a docstring for each module, class, and function
- Use descriptive variable and function names
- When creating examples, follow the existing patterns in the repository

## Simple Language Implementation

- The repository includes a simple language implementation with lexer, parser, and evaluator
- Key components: TokenType, Token, Lexer, Parser, Symbol, Environment, Procedure, and Evaluator classes
- The language supports basic arithmetic, conditionals, and functional programming constructs
- The interpreter includes reflection capabilities and a meta-circular evaluator