"""
Tests for MessageService.
"""

import uuid

import pytest

from services.message_service import MessageService


@pytest.mark.asyncio
async def test_message_service_insert_message() -> None:
    """Test inserting a message through MessageService."""
    # Arrange
    service = MessageService()
    external_id = str(uuid.uuid4())
    test_message = {
        "external_id": external_id,
        "type": "text",
        "role": "assistant",
        "data": {"text": "Hello, world!"},
        "client": {"phone_number": "1234567890"},
        "commerce": {"id": "test-company"},
        "direction": "outbound",
        "timestamp": 1647432432.123,
    }

    # Act
    result = await service.insert_message(test_message)

    # Assert
    assert result == external_id, "Should return the external ID"


@pytest.mark.asyncio
async def test_message_service_init() -> None:
    """Test MessageService initialization."""
    # Act
    service = MessageService()

    # Assert
    assert isinstance(service, MessageService), "Should be a MessageService instance"


@pytest.mark.asyncio
async def test_message_service_interface_compliance() -> None:
    """Test that MessageService adheres to the MessageServiceInterface."""
    # This test checks that the service implements the required methods
    # from its interface. It should have an insert_message method.

    # Arrange
    service = MessageService()

    # Assert
    assert hasattr(service, "insert_message"), (
        "Service should have insert_message method"
    )
    assert callable(service.insert_message), "insert_message should be callable"


@pytest.mark.asyncio
async def test_message_service_missing_external_id() -> None:
    """Test handling of messages without external_id."""
    # Arrange
    service = MessageService()
    test_message = {
        # No external_id provided
        "type": "text",
        "role": "assistant",
        "data": {"text": "Hello, world!"},
    }

    # Act
    result = await service.insert_message(test_message)

    # Assert
    assert result == "no-id", "Should return default ID when external_id is missing"
