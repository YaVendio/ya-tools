"""
Mock implementation of message service for testing and development.
"""

import uuid
from typing import Any, Dict

from services.interfaces import MessageServiceInterface


class MockMessageService(MessageServiceInterface):
    """In-memory mock implementation of message service."""

    def __init__(self):
        self.messages = {}  # message_id -> message

    async def insert_message(self, message: Dict[str, Any]) -> str:
        """
        Insert a message and return its ID.

        Args:
            message: Message data to store

        Returns:
            Message ID as string
        """
        message_id = str(uuid.uuid4())
        self.messages[message_id] = message
        print(f"[MOCK] Message stored with ID: {message_id}")
        return message_id
