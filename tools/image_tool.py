"""
Image tool for sending images
"""

import uuid
from typing import Any

from tools.base_tool import MessageTool


class ImageTool(MessageTool):
    """Tool for sending image messages."""

    def __init__(self, urls: list[str] | str):
        """
        Initialize with image URLs.

        Args:
            urls: Single URL or list of image URLs
        """
        self.urls = urls if isinstance(urls, list) else [urls]

    async def execute(self, context: dict[str, Any]) -> list[str]:
        """
        Send images.

        Args:
            context: Execution context

        Returns:
            List of message IDs
        """
        message_service = context["lifespan_context"]["message_service"]

        # Define explicit type for the sent_ids list
        sent_ids: list[str] = []
        for url in self.urls:
            external_id = await self._send_image(
                context["phone_number"], url, context["company_id"]
            )

            # Create outbound message
            outbound_message = self.get_outbound_message(
                external_id, context, url, "image", "media_assistant"
            )

            # Store the message
            await message_service.insert_message(outbound_message)

            # Now append to the explicitly typed list
            sent_ids.append(external_id)

        # Return with explicit type
        return sent_ids

    async def _send_image(self, phone_number: str, url: str, company_id: str) -> str:
        """
        Placeholder for external API call.

        Args:
            phone_number: Recipient's phone number
            url: Image URL
            company_id: Company identifier

        Returns:
            External message ID
        """
        # Parameters intentionally unused in this mock implementation
        _ = phone_number, url, company_id
        # Implement actual image sending here
        # This would typically call a WhatsApp API provider
        return str(uuid.uuid4())
