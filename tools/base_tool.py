"""
Base tool class for implementing messaging tools
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class Tool(ABC):
    """
    Abstract base class for all action tools.

    All tools should inherit from this class and implement
    the execute method.
    """

    @abstractmethod
    async def execute(self, context: dict[str, Any]) -> Any:
        """
        Execute the tool with the given context.

        Args:
            context: Execution context with necessary data

        Returns:
            Tool-specific result
        """
        pass


class MessageTool(Tool):
    """
    Base class for tools that send messages.

    Provides common functionality for message formatting
    and structure.
    """

    def get_outbound_message(
        self,
        external_id: str,
        context: dict[str, Any],
        data: Any,
        message_type: str,
        role: str = "system",
    ) -> dict[str, Any]:
        """
        Create a standardized outbound message.

        Args:
            external_id: External message identifier
            context: Execution context
            data: Message data/content
            message_type: Type of message (text, image, etc.)
            role: Message sender role

        Returns:
            Formatted message object
        """
        return {
            "system": "whatsapp",
            "type": message_type,
            "data": self._format_data(data, message_type),
            "client": {"phone_number": context["phone_number"]},
            "commerce": {"id": context["company_id"]},
            "external_id": external_id,
            "direction": "outbound",
            "role": role,
            "timestamp": datetime.now().timestamp(),
        }

    def _format_data(self, content: Any, message_type: str) -> dict[str, Any]:
        """
        Format content based on message type.

        Args:
            content: Raw message content
            message_type: Type of message

        Returns:
            Formatted message data
        """
        if message_type == "text":
            return {"text": content}
        elif message_type in ["image", "video", "document"]:
            if isinstance(content, dict) and "url" in content:
                return content
            return {"url": content, "mime_type": self._get_mime_type(message_type)}
        return {"content": content}

    def _get_mime_type(self, message_type: str) -> str:
        """
        Get MIME type based on message type.

        Args:
            message_type: Type of message

        Returns:
            Appropriate MIME type
        """
        mime_types = {
            "image": "image/jpeg",
            "video": "video/mp4",
            "document": "application/pdf",
        }
        return mime_types.get(message_type, "application/octet-stream")
