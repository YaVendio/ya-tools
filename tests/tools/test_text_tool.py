"""
Test for TextTool with mock services.
"""

from typing import Any

import pytest

from services.message_service_mock import MockMessageService
from tools.text_tool import TextTool


@pytest.fixture
def mock_services() -> dict[str, Any]:
    """Fixture providing mock services for tests."""
    return {
        "message_service": MockMessageService(),
    }


@pytest.fixture
def test_context(mock_services: dict[str, Any]) -> dict[str, Any]:
    """Fixture providing test context with mock services."""
    return {
        "lifespan_context": mock_services,
        "phone_number": "1234567890",
        "company_id": "test-company",
    }


@pytest.mark.asyncio
async def test_text_tool_execution(test_context: dict[str, Any]) -> None:
    """Test the TextTool with mock services."""
    # Create and execute text tool
    text_tool = TextTool("Hello, this is a test message!")
    message_id = await text_tool.execute(test_context)

    # Get services from context
    message_service = test_context["lifespan_context"]["message_service"]

    # Assertions
    assert message_id is not None, "Message ID should be returned"
    assert len(message_service.messages) > 0, "Message should be stored"

    # Check message details
    if message_service.messages:
        sample_message = next(iter(message_service.messages.values()))
        assert "type" in sample_message, "Message should have a type"
        assert "role" in sample_message, "Message should have a role"
