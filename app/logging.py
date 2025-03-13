"""
Logging configuration for the application.

This module provides a structured logging setup using structlog:
- Development: Rich console output with colors and pretty formatting
- Production: JSON format for better integration with log aggregation systems
"""

import os
from typing import Any

import structlog
from rich.console import Console

# Rich console for development logging
console = Console()


def configure_logging(env: str | None = None) -> None:
    """
    Configure structlog based on the environment.

    Args:
        env: The environment to configure for ("development" or "production").
             If None, will try to read from ENVIRONMENT env var, defaulting to "development".
    """
    # Determine environment
    if env is None:
        env = os.environ.get("ENVIRONMENT", "development")

    # Common processors for all environments
    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    # Configure based on environment
    if env.lower() == "development":
        # Development: Rich console output
        processors = [
            *shared_processors,
            # Add color and proper formatting
            structlog.dev.ConsoleRenderer(
                colors=True, exception_formatter=structlog.dev.rich_traceback
            )
        ]
    else:
        # Production: JSON format
        processors = [
            *shared_processors,
            # Convert exceptions to dict before JSON serializing
            structlog.processors.format_exc_info,
            structlog.processors.dict_tracebacks,
            # Render as JSON
            structlog.processors.JSONRenderer(),
        ]

    # Apply configuration
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """
    Get a configured logger.

    Args:
        name: Optional name for the logger (defaults to module name)

    Returns:
        A configured structlog logger
    """
    if name is None:
        # Use the calling module name if no name provided
        # Using inspect instead of sys._getframe to avoid private method usage
        import inspect
        frame = inspect.currentframe()
        if frame and frame.f_back:
            name = frame.f_back.f_globals.get("__name__", "unknown")
        else:
            name = "unknown"

    return structlog.get_logger(name)


# Configure logging when this module is imported
configure_logging()
