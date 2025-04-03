# Variables
PYTHON = poetry run ipython
PIP = pip3
POETRY = poetry

# Poetry Environment
.PHONY: install
install:
	$(POETRY) install

# Update Dependencies
.PHONY: update
update:
	$(POETRY) update

# Export Dependencies
.PHONY: export
export:
	$(POETRY) export -f requirements.txt --output requirements.txt

# New Exercise Workspace
.PHONY: new-exercise
new-exercise:
	git checkout -b $(USER)-exercise-$(shell date +%Y%m%d-%H%M)

# Solutions
.PHONY: solutions
solutions:
	git checkout -b solutions

# Format Code
.PHONY: format
format:
	$(POETRY) run black .
	$(POETRY) run isort .

# Lint Code
.PHONY: lint
lint:
	$(POETRY) run flake8 .
	$(POETRY) run mypy .
	$(POETRY) run pylint .

# Type Check
.PHONY: typecheck
typecheck:
	$(POETRY) run mypy .

# Run Tests
.PHONY: test
test:
	$(POETRY) run pytest tests/

# Run Single Test
.PHONY: test-file
test-file:
	@echo "Usage: make test-file FILE=tests/test_file.py"
	$(POETRY) run pytest $(FILE) -v

# Run Single Test Function
.PHONY: test-function
test-function:
	@echo "Usage: make test-function FILE=tests/test_file.py::test_function"
	$(POETRY) run pytest $(FILE) -v

# Run Interactive Shell
.PHONY: shell
shell:
	$(PYTHON)

# Generate Data
.PHONY: data.txt
data.txt:
	seq 10 > data.txt

# Clean Up
.PHONY: clean
clean:
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
	@echo "  make update      Update dependencies"
	@echo "  make export      Export dependencies to requirements.txt"
	@echo "  make format      Format code with black and isort"
	@echo "  make lint        Lint the code"
	@echo "  make typecheck   Run type checking"
	@echo "  make test        Run all tests"
	@echo "  make test-file   Run a specific test file (make test-file FILE=tests/test_file.py)"
	@echo "  make test-function Run a specific test function (make test-function FILE=tests/test_file.py::test_function)"
	@echo "  make shell       Launch IPython shell"
	@echo "  make clean       Clean up generated files"
	@echo "  make help        Show this help message"

# Default Target
.DEFAULT_GOAL := help
