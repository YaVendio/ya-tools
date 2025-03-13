"""
Manual test to verify unified messaging tools.
This script tests both methods of sending messages:
1. Using company_id (general approach)
2. Using client_id (WhatsApp specific approach)
"""

import asyncio
import logging
from typing import Any

from services.whatsapp_service_mock import MockWhatsAppService

# Set up logging instead of using print
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


async def test_unified_tools() -> None:
    """Test the unified messaging tools."""
    logger.info("Testing unified messaging tools...")

    # Create a mock context
    whatsapp_service = MockWhatsAppService()
    lifespan_context: dict[str, Any] = {
        "message_service": None,  # We won't actually call the message service
        "whatsapp_service": whatsapp_service,
    }

    ctx = type(
        "Context",
        (),
        {
            "request_context": type(
                "RequestContext", (), {"lifespan_context": lifespan_context}
            )
        },
    )()

    # Register a test WhatsApp client
    await whatsapp_service.register_client(
        client_id="test_whatsapp_client", phone_id="123456789", token="test_token"
    )

    # Import the send_text function from server
    from app.server import send_text

    # Test with client_id (WhatsApp approach)
    logger.info("\nTesting with client_id (WhatsApp approach):")
    result = await send_text(
        ctx=ctx,
        company_id="test_company",  # Required but not used when client_id is provided
        phone_number="1234567890",
        message="Test message with client_id",
        client_id="test_whatsapp_client",
    )
    logger.info(f"WhatsApp message sent with result: {result}")


if __name__ == "__main__":
    asyncio.run(test_unified_tools())
