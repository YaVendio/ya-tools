.PHONY: help install dev-install sync test lint format clean

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
	@echo "format        - Format code"
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
test:
	@echo "Running tests..."
	python -m pytest

# Run tests with coverage
coverage:
	@echo "Running tests with coverage..."
	python -m pytest --cov=app --cov=services --cov=tools --cov-report=term --cov-report=html

# Run linter
lint:
	@echo "Running linter..."
	ruff check app services tools scripts tests

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
install-mcp:
	@echo "Installing in Claude Desktop..."
	mcp install app/server.py 