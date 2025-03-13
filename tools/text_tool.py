"""
Text messaging tool for sending text messages
"""

import uuid
from typing import Any

from services.interfaces import MessageServiceInterface
from tools.base_tool import MessageTool


class TextTool(MessageTool):
    """Tool for sending text messages."""

    def __init__(self, message: str):
        """
        Initialize with message text.

        Args:
            message: Text message content
        """
        self.message = message

    async def execute(self, context: dict[str, Any]) -> str | None:
        """
        Send a text message.

        Args:
            context: Execution context

        Returns:
            Message ID if sent successfully
        """
        if not self.message:
            return None

        # Get services from context using proper interfaces
        message_service: MessageServiceInterface = context["lifespan_context"][
            "message_service"
        ]

        # In a real implementation, this would call an external service
        external_id = await self._send_message(
            context["phone_number"], self.message, context["company_id"]
        )

        # Create outbound message
        outbound_message = self.get_outbound_message(
            external_id, context, self.message, "text", "assistant"
        )

        # Store the message using the service
        await message_service.insert_message(outbound_message)

        return external_id

    async def _send_message(
        self, phone_number: str, message: str, company_id: str
    ) -> str:
        """
        Placeholder for external API call.

        Args:
            phone_number: Recipient's phone number
            message: Message content
            company_id: Company identifier

        Returns:
            External message ID
        """
        # Implement actual message sending here
        # This would typically call a WhatsApp API provider
        return str(uuid.uuid4())
