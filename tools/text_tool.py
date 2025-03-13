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

        # Get recipient information from context
        phone_number = context["phone_number"]
        company_id = context["company_id"]

        # Send message and store it
        external_id = await self._send_message(phone_number, self.message, company_id)

        # Store the message with message service
        message_id = await message_service.insert_message(
            {
                "external_id": external_id,
                "company_id": company_id,
                "role": "assistant",
                "type": "text",
                "data": {"text": self.message},
                "timestamp": uuid.uuid4().hex,
            }
        )

        return message_id

    async def _send_message(
        self, _phone_number: str, _message: str, _company_id: str
    ) -> str:
        """
        Placeholder for external API call.
        In a real implementation, this would call an actual messaging API.

        Args:
            _phone_number: Recipient's phone number
            _message: Text message to send
            _company_id: Company identifier

        Returns:
            External message ID
        """
        # This is a placeholder that would normally call an actual API
        # Return a UUID as a mock external ID
        return str(uuid.uuid4())
