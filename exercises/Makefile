deps: # Install dependencies
	poetry install
	poetry run pip install black flake8 isort mypy

black: # Run black 
	poetry run python -m black .

.PHONY: isort
isort: # Run isort
	poetry run python -m isort .

.PHONY: lint
lint: # Run linters
	poetry run python -m black --check .
	poetry run python -m isort --check .
	poetry run python -m flake8 .
	poetry run python -m mypy .

.PHONY: test
test: # Run tests
	poetry run python -m pytest .

test-topk: # Run tests
	poetry run python test_topk.py

test-topk-clj: # Run tests
	bb topk.clj
