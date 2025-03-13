#!/usr/bin/env python
"""
Test script for mock services.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from services.message_service_mock import MockMessageService
from tools.text_tool import TextTool


async def test_text_tool():
    """Test the TextTool with mock services."""
    print("=== Testing TextTool with Mock Services ===")

    # Create mock services
    message_service = MockMessageService()

    # Create test context
    context = {
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
    print(f"\nMessage ID: {message_id}")
    print(f"Messages stored: {len(message_service.messages)}")

    # Print stored message details
    if message_service.messages:
        sample_message = next(iter(message_service.messages.values()))
        print(f"\nStored message type: {sample_message.get('type')}")
        print(f"Stored message role: {sample_message.get('role')}")

    print("\n=== Test completed successfully ===")


if __name__ == "__main__":
    asyncio.run(test_text_tool())
