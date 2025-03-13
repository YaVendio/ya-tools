"""
Application lifecycle management.
"""

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from services.message_service_mock import MockMessageService

# Set up structured logging
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Set up and tear down application resources."""

    # Initialize mock services
    message_service = MockMessageService()

    # Store in app state and lifespan context
    app.state.lifespan_context = {
        "message_service": message_service,
    }

    logger.info("Mock services initialized", event="startup")

    yield

    logger.info("Application shutting down", event="shutdown")
