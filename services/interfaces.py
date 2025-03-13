"""
Service interfaces for yatools.
Defines the contracts that service implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import Any


class MessageServiceInterface(ABC):
    """Interface for message storage and retrieval."""

    @abstractmethod
    async def insert_message(self, message: dict[str, Any]) -> str:
        """
        Insert a message and return its ID.

        Args:
            message: Message data to store

        Returns:
            Message ID as string
        """
        pass


class WhatsAppServiceInterface(ABC):
    """Interface for WhatsApp client management and operations."""

    @abstractmethod
    async def get_client(self, client_id: str) -> Any:
        """
        Get a WhatsApp client by client_id.

        Args:
            client_id: Unique identifier for the client

        Returns:
            WhatsApp client instance
        """
        pass

    @abstractmethod
    async def register_client(self, client_id: str, phone_id: str, token: str) -> Any:
        """
        Register a new WhatsApp client.

        Args:
            client_id: Unique identifier for the client
            phone_id: WhatsApp phone ID
            token: WhatsApp API token

        Returns:
            WhatsApp client instance
        """
        pass

    @abstractmethod
    async def list_clients(self) -> list[str]:
        """
        List all registered client IDs.

        Returns:
            List of client IDs
        """
        pass

    @abstractmethod
    async def send_text(self, client_id: str, to: str, text: str) -> str:
        """
        Send a text message.

        Args:
            client_id: Client to use for sending
            to: Recipient phone number
            text: Message text

        Returns:
            Message ID
        """
        pass

    @abstractmethod
    async def send_image(
        self, client_id: str, to: str, image: str, caption: str | None = None
    ) -> str:
        """
        Send an image.

        Args:
            client_id: Client to use for sending
            to: Recipient phone number
            image: Image URL
            caption: Optional caption

        Returns:
            Message ID
        """
        pass

    @abstractmethod
    async def send_video(
        self, client_id: str, to: str, video: str, caption: str | None = None
    ) -> str:
        """
        Send a video.

        Args:
            client_id: Client to use for sending
            to: Recipient phone number
            video: Video URL
            caption: Optional caption

        Returns:
            Message ID
        """
        pass

    @abstractmethod
    async def send_document(
        self,
        client_id: str,
        to: str,
        document: str,
        caption: str | None = None,
        filename: str | None = None,
    ) -> str:
        """
        Send a document.

        Args:
            client_id: Client to use for sending
            to: Recipient phone number
            document: Document URL
            caption: Optional caption
            filename: Optional filename

        Returns:
            Message ID
        """
        pass

    @abstractmethod
    async def send_buttons(
        self, client_id: str, to: str, text: str, buttons: list[dict[str, str]]
    ) -> str:
        """
        Send a message with buttons.

        Args:
            client_id: Client to use for sending
            to: Recipient phone number
            text: Message text
            buttons: List of button configs [{"title": "...", "callback_data": "..."}]

        Returns:
            Message ID
        """
        pass
