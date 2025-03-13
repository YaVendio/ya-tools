"""
Tests for DocumentTool with mock services.
"""

import uuid
from typing import Any
from unittest.mock import patch

import pytest

from tools.document_tool import DocumentTool


@pytest.mark.asyncio
async def test_document_tool_single_file(test_context: dict[str, Any]) -> None:
    """Test the DocumentTool with a single document file."""
    # Arrange
    file = {"url": "https://example.com/doc.pdf", "filename": "document.pdf"}
    document_tool = DocumentTool([file])

    # Get services from context
    message_service = test_context["lifespan_context"]["message_service"]

    # Act
    message_ids = await document_tool.execute(test_context)

    # Assert
    assert len(message_ids) == 1, "Should return one message ID"
    assert message_ids[0] is not None, "Message ID should not be None"
    assert len(message_service.messages) == 1, "One message should be stored"

    # Check message details
    if message_service.messages:
        message = next(iter(message_service.messages.values()))
        assert message["type"] == "document", "Message type should be document"
        assert message["role"] == "media_assistant", (
            "Message role should be media_assistant"
        )
        assert message["data"]["url"] == file["url"], "Document URL should match"
        assert message["data"]["filename"] == file["filename"], "Filename should match"
        assert "mime_type" in message["data"], "MIME type should be included"


@pytest.mark.asyncio
async def test_document_tool_multiple_files(test_context: dict[str, Any]) -> None:
    """Test the DocumentTool with multiple document files."""
    # Arrange
    files = [
        {"url": "https://example.com/doc1.pdf", "filename": "document1.pdf"},
        {"url": "https://example.com/doc2.pdf", "filename": "document2.pdf"},
        {"url": "https://example.com/doc3.pdf", "filename": "document3.pdf"},
    ]
    document_tool = DocumentTool(files)

    # Get services from context
    message_service = test_context["lifespan_context"]["message_service"]

    # Act
    message_ids = await document_tool.execute(test_context)

    # Assert
    assert len(message_ids) == 3, "Should return three message IDs"
    assert len(message_service.messages) == 3, "Three messages should be stored"


@pytest.mark.asyncio
async def test_document_tool_empty_list(test_context: dict[str, Any]) -> None:
    """Test the DocumentTool with an empty list of files."""
    # Arrange
    document_tool = DocumentTool([])

    # Act
    message_ids = await document_tool.execute(test_context)

    # Assert
    assert len(message_ids) == 0, "Should return empty list of message IDs"


@pytest.mark.asyncio
async def test_document_tool_invalid_file(test_context: dict[str, Any]) -> None:
    """Test the DocumentTool with invalid file data."""
    # Arrange - Missing filename
    files = [
        {"url": "https://example.com/doc1.pdf"},  # Missing filename
        {"filename": "document2.pdf"},  # Missing URL
        "not_a_dict",  # Not a dict
    ]
    document_tool = DocumentTool(files)

    # Act
    message_ids = await document_tool.execute(test_context)

    # Assert
    assert len(message_ids) == 0, "Should return empty list when all files are invalid"


@pytest.mark.asyncio
async def test_document_tool_send_document_called(test_context: dict[str, Any]) -> None:
    """Test that _send_document method is called correctly."""
    # Arrange
    file = {"url": "https://example.com/doc.pdf", "filename": "document.pdf"}
    document_tool = DocumentTool([file])

    # Use patch as context manager to mock the method while preserving access to self
    with patch.object(DocumentTool, "_send_document", autospec=True) as mock_method:
        # Setup the mock to return a UUID
        test_id = str(uuid.uuid4())
        mock_method.return_value = test_id

        # Act
        await document_tool.execute(test_context)

        # Assert
        mock_method.assert_called_once()
        # Check that the arguments match what we expect
        args = mock_method.call_args[0]
        # args[0] is 'self', args[1] is phone_number, etc.
        assert args[1] == test_context["phone_number"]
        assert args[2] == file["url"]
        assert args[3] == file["filename"]
        assert args[4] == test_context["company_id"]
