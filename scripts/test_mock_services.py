#!/usr/bin/env python
"""
Test script for mock services.
"""

import asyncio
import sys
from pathlib import Path
from typing import Any

import structlog

# Set up structured logging
logger = structlog.get_logger(__name__)

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Import local modules after path is set
from services.message_service_mock import MockMessageService  # noqa: E402
from tools.text_tool import TextTool  # noqa: E402


async def test_text_tool():
    """Test the TextTool with mock services."""
    logger.info("Testing TextTool with Mock Services", test_started=True)

    # Create mock services
    message_service = MockMessageService()

    # Create test context with proper type annotation
    context: dict[str, Any] = {
        "lifespan_context": {
            "message_service": message_service,
        },
        "phone_number": "1234567890",
        "company_id": "test-company",
    }

    # Create and execute text tool
    text_tool = TextTool("Hello, this is a test message!")
    message_id = await text_tool.execute(context)

    # Verify results
    logger.info(
        "Message sent", 
        message_id=message_id, 
        messages_count=len(message_service.messages)
    )

    # Print stored message details
    if message_service.messages:
        sample_message: dict[str, Any] = next(iter(message_service.messages.values()))
        logger.info(
            "Message details",
            message_type=sample_message.get('type', ''),
            message_role=sample_message.get('role', '')
        )

    logger.info("Test completed successfully", test_completed=True)


if __name__ == "__main__":
    asyncio.run(test_text_tool())
