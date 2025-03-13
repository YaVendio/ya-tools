"""
Application lifecycle management.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.message_service_mock import MockMessageService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Set up and tear down application resources."""

    # Initialize mock services
    message_service = MockMessageService()

    # Store in app state and lifespan context
    app.state.lifespan_context = {
        "message_service": message_service,
    }

    print("[STARTUP] Mock services initialized")

    yield

    print("[SHUTDOWN] Application shutting down")
