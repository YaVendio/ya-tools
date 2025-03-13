"""
Tests for ImageTool with mock services.
"""

import uuid
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from tools.image_tool import ImageTool


@pytest.mark.asyncio
async def test_image_tool_single_url(test_context: dict[str, Any]) -> None:
    """Test the ImageTool with a single image URL."""
    # Arrange
    image_url = "https://example.com/image.jpg"
    image_tool = ImageTool(image_url)

    # Get services from context
    message_service = test_context["lifespan_context"]["message_service"]

    # Act
    message_ids = await image_tool.execute(test_context)

    # Assert
    assert len(message_ids) == 1, "Should return one message ID"
    assert message_ids[0] is not None, "Message ID should not be None"
    assert len(message_service.messages) == 1, "One message should be stored"

    # Check message details
    if message_service.messages:
        message = next(iter(message_service.messages.values()))
        assert message["type"] == "image", "Message type should be image"
        assert message["role"] == "media_assistant", (
            "Message role should be media_assistant"
        )
        assert message["data"]["url"] == image_url, "Image URL should match"


@pytest.mark.asyncio
async def test_image_tool_multiple_urls(test_context: dict[str, Any]) -> None:
    """Test the ImageTool with multiple image URLs."""
    # Arrange
    image_urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        "https://example.com/image3.jpg",
    ]
    image_tool = ImageTool(image_urls)

    # Get services from context
    message_service = test_context["lifespan_context"]["message_service"]

    # Act
    message_ids = await image_tool.execute(test_context)

    # Assert
    assert len(message_ids) == 3, "Should return three message IDs"
    assert len(message_service.messages) == 3, "Three messages should be stored"


@pytest.mark.asyncio
async def test_image_tool_empty_list(test_context: dict[str, Any]) -> None:
    """Test the ImageTool with an empty list of URLs."""
    # Arrange
    image_tool = ImageTool([])

    # Act
    message_ids = await image_tool.execute(test_context)

    # Assert
    assert len(message_ids) == 0, "Should return empty list of message IDs"


@pytest.mark.asyncio
async def test_image_tool_send_image_called(test_context: dict[str, Any]) -> None:
    """Test that _send_image method is called correctly."""
    # Arrange
    image_url = "https://example.com/image.jpg"
    image_tool = ImageTool(image_url)

    # Use patch to spy on the _send_image method
    with patch.object(
        image_tool, "_send_image", wraps=image_tool._send_image
    ) as mock_send_image:
        # Act
        await image_tool.execute(test_context)

        # Assert
        mock_send_image.assert_called_once_with(
            test_context["phone_number"], image_url, test_context["company_id"]
        )


@pytest.mark.asyncio
async def test_image_tool_handles_external_id(test_context: dict[str, Any]) -> None:
    """Test that the tool correctly handles external IDs."""
    # Arrange
    image_url = "https://example.com/image.jpg"
    image_tool = ImageTool(image_url)
    test_id = str(uuid.uuid4())

    # Mock the _send_image method to return a predetermined ID
    with patch.object(
        image_tool, "_send_image", new_callable=AsyncMock
    ) as mock_send_image:
        mock_send_image.return_value = test_id

        # Act
        message_ids = await image_tool.execute(test_context)

        # Assert
        assert message_ids[0] == test_id, (
            "Should return the external ID from _send_image"
        )

        # Check that ID is used in stored message
        message_service = test_context["lifespan_context"]["message_service"]
        for msg in message_service.messages.values():
            assert msg["external_id"] == test_id, (
                "External ID should be in stored message"
            )
