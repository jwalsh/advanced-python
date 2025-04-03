# Variables
PYTHON = poetry run ipython
POETRY = poetry

# Poetry Environment
.PHONY: install
install: # Install dependencies
	$(POETRY) install

# Format Code
.PHONY: format
format: # Format code with black and isort
	$(POETRY) run black .
	$(POETRY) run isort .

# Lint Code
.PHONY: lint
lint: # Run linters
	$(POETRY) run black --check .
	$(POETRY) run isort --check .
	$(POETRY) run flake8 .
	$(POETRY) run mypy .
	$(POETRY) run pylint .

# Type Check
.PHONY: typecheck
typecheck: # Run type checking
	$(POETRY) run mypy .

# Run Tests
.PHONY: test
test: # Run all tests
	$(POETRY) run pytest .

# Run Single Test
.PHONY: test-file
test-file: # Run a specific test file
	@echo "Usage: make test-file FILE=test_file.py"
	$(POETRY) run pytest $(FILE) -v

# Run Single Test Function
.PHONY: test-function
test-function: # Run a specific test function
	@echo "Usage: make test-function FILE=test_file.py::test_function"
	$(POETRY) run pytest $(FILE) -v

# Run specific exercise tests
.PHONY: test-topk
test-topk: # Run topk tests
	$(POETRY) run python test_topk.py

.PHONY: test-topk-clj
test-topk-clj: # Run topk Clojure tests
	bb topk.clj

# Run Interactive Shell
.PHONY: shell
shell: # Launch IPython shell
	$(PYTHON)

# Clean Up
.PHONY: clean
clean: # Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".mypy_cache" -delete
	find . -type d -name ".coverage_cache" -delete

# Help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install     Install dependencies"
	@echo "  make format      Format code with black and isort"
	@echo "  make lint        Lint the code"
	@echo "  make typecheck   Run type checking"
	@echo "  make test        Run all tests"
	@echo "  make test-file   Run a specific test file (make test-file FILE=test_file.py)"
	@echo "  make test-function Run a specific test function (make test-function FILE=test_file.py::test_function)"
	@echo "  make test-topk   Run topk tests"
	@echo "  make test-topk-clj Run topk Clojure tests"
	@echo "  make shell       Launch IPython shell"
	@echo "  make clean       Clean up generated files"
	@echo "  make help        Show this help message"

# Default Target
.DEFAULT_GOAL := help