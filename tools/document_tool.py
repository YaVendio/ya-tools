"""
Document tool for sending documents
"""

import uuid
from typing import Any

from tools.base_tool import MessageTool


class DocumentTool(MessageTool):
    """Tool for sending document files."""

    def __init__(self, files: list[dict[str, str]]):
        """
        Initialize with document files.

        Args:
            files: List of document files as {"url": "...", "filename": "..."}
        """
        self.files = files

    async def execute(self, context: dict[str, Any]) -> list[str]:
        """
        Send documents.

        Args:
            context: Execution context

        Returns:
            List of message IDs
        """
        message_service = context["lifespan_context"]["message_service"]

        sent_ids = []
        for file in self.files:
            if (
                not isinstance(file, dict)
                or "url" not in file
                or "filename" not in file
            ):
                continue

            url = file["url"]
            filename = file["filename"]

            external_id = await self._send_document(
                context["phone_number"], url, filename, context["company_id"]
            )

            # Create outbound message
            outbound_message = self.get_outbound_message(
                external_id,
                context,
                {
                    "url": url,
                    "filename": filename,
                    "mime_type": self._get_mime_type("document"),
                },
                "document",
                "media_assistant",
            )

            # Store the message
            await message_service.insert_message(outbound_message)

            sent_ids.append(external_id)

        return sent_ids

    async def _send_document(
        self, phone_number: str, url: str, filename: str, company_id: str
    ) -> str:
        """
        Placeholder for external API call.

        Args:
            phone_number: Recipient's phone number
            url: Document URL
            filename: Document filename
            company_id: Company identifier

        Returns:
            External message ID
        """
        # Implement actual document sending here
        # This would typically call a WhatsApp API provider
        return str(uuid.uuid4())
