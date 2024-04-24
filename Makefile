# Variables
PYTHON = python3
PIP = pip3
VENV_NAME = venv

# Virtual Environment
$(VENV_NAME):
	$(PYTHON) -m venv $(VENV_NAME)

# Activate Virtual Environment
activate:
	source $(VENV_NAME)/bin/activate

# Install Dependencies
install: $(VENV_NAME)
	$(VENV_NAME)/bin/$(PIP) install -r requirements.txt

# Update Dependencies
update:
	$(VENV_NAME)/bin/$(PIP) install --upgrade -r requirements.txt

# Freeze Dependencies
freeze:
	$(VENV_NAME)/bin/$(PIP) freeze > requirements.txt

# New Exercise Workspace
new-exercise:
	git checkout -b $(USER)-exercise-$(shell date +%Y%m%d-%H%M)

# Solutions
solutions:
	git checkout -b solutions

# Lint Code
lint:
	$(VENV_NAME)/bin/flake8 .

# Run Tests
test:
	$(VENV_NAME)/bin/pytest tests/

# Run Application
run:
	$(VENV_NAME)/bin/python main.py

# Generate Data
data.txt:
	seq 10 > data.txt

# Clean Up
clean:
	rm -rf $(VENV_NAME)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Help
help:
	@echo "Available commands:"
	@echo "  make install    Install dependencies"
	@echo "  make update     Update dependencies"
	@echo "  make freeze     Freeze dependencies"
	@echo "  make lint       Lint the code"
	@echo "  make test       Run tests"
	@echo "  make run        Run the application"
	@echo "  make clean      Clean up generated files"
	@echo "  make help       Show this help message"

# Default Target
.DEFAULT_GOAL := help
