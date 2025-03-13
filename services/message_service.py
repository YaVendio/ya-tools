"""
Message service for handling message storage and retrieval
"""

from typing import Any, Dict

from services.interfaces import MessageServiceInterface


class MessageService(MessageServiceInterface):
    """Message service for persisting messages."""

    def __init__(self):
        """
        Initialize message service.
        """
        # We're no longer using a database here
        pass

    async def insert_message(self, message: Dict[str, Any]) -> str:
        """
        Insert a message and return its ID.

        Args:
            message: Message data to store

        Returns:
            Message ID as string
        """
        # Just a stub implementation that returns the external_id from the message
        return message.get("external_id", "no-id")
