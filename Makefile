.PHONY: help install dev-install sync test lint lint-fix format clean typecheck

# Help command
help:
	@echo "YaVendió Tools Makefile Commands:"
	@echo ""
	@echo "install       - Install project dependencies"
	@echo "dev-install   - Install development dependencies"
	@echo "sync          - Sync all dependencies (regular and dev)"
	@echo "test          - Run tests"
	@echo "coverage      - Run tests with coverage report"
	@echo "lint          - Run linter"
	@echo "lint-fix      - Run linter and automatically fix issues"
	@echo "format        - Format code"
	@echo "typecheck     - Run type checker"
	@echo "clean         - Clean cache files and directories"
	@echo "run           - Run the application with MCP Inspector (dev mode)"
	@echo "run-prod      - Run the application with MCP (production mode)"
	@echo "install-mcp   - Install the app in Claude Desktop"
	@echo ""

# Install dependencies
install:
	@echo "Installing dependencies..."
	uv sync

# Install development dependencies
dev-install:
	@echo "Installing development dependencies..."
	uv sync --extra dev

# Sync all dependencies
sync: install dev-install
	@echo "All dependencies synced"

# Run tests
# Usage: make test [TEST_PATH=path/to/test] [TEST_ARGS="-v -m 'not slow'"]
TEST_PATH ?= 
TEST_ARGS ?= 

test:
	@echo "Running tests..."
	python -m pytest $(TEST_PATH) $(TEST_ARGS)

# Run tests with coverage
coverage:
	@echo "Running tests with coverage..."
	python -m pytest --cov=app --cov=services --cov=tools --cov-report=term --cov-report=html

# Run linter
lint:
	@echo "Running linter..."
	ruff check app services tools scripts tests

# Run linter and fix issues
lint-fix:
	@echo "Running linter and fixing issues..."
	ruff check --fix app services tools scripts tests

# Run type checker
typecheck:
	@echo "Running type checker..."
	uv run pyright app services tools scripts tests

# Format code
format:
	@echo "Formatting code..."
	ruff format app services tools scripts tests

# Clean cache files and directories
clean:
	@echo "Cleaning caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf htmlcov
	rm -rf .coverage

# Run application in development mode with MCP Inspector
run:
	@echo "Running in development mode with MCP Inspector..."
	ENVIRONMENT=development mcp dev app/server.py

# Run application in production mode with MCP
run-prod:
	@echo "Running in production mode..."
	ENVIRONMENT=production mcp run app/server.py

# Install in Claude Desktop
mcp-install:
	@echo "Installing in Claude Desktop..."
	mcp install app/server.py

# Run with MCP in development mode
mcp-dev:
	@echo "Running in MCP development mode..."
	mcp dev app/server.py

# Install from PyPI package
mcp-install-pkg:
	@echo "Installing MCP package from PyPI..."
	mcp install ya-tools