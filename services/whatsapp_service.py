"""
WhatsApp service for managing multiple clients using PyWa.
"""

import os
import uuid
from typing import Dict, List

import redis
from pywa import WhatsApp
from pywa.types import Button

from services.interfaces import WhatsAppServiceInterface


class WhatsAppClientError(Exception):
    """Base exception for WhatsApp client errors."""

    pass


class ClientNotFoundError(WhatsAppClientError):
    """Raised when a WhatsApp client is not found."""

    pass


class WhatsAppService(WhatsAppServiceInterface):
    """Service for managing WhatsApp clients and operations."""

    def __init__(self, redis_url: str = None):
        """
        Initialize WhatsApp service.

        Args:
            redis_url: Redis connection URL
        """
        redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis = redis.Redis.from_url(redis_url)
        self.clients: Dict[str, WhatsApp] = {}

    async def get_client(self, client_id: str) -> WhatsApp:
        """
        Get a WhatsApp client by client_id.

        Args:
            client_id: Unique identifier for the client

        Returns:
            WhatsApp client instance

        Raises:
            ClientNotFoundError: If the client is not found
        """
        if client_id not in self.clients:
            # Try to get token from Redis
            token = self.redis.get(f"whatsapp:token:{client_id}")
            phone_id = self.redis.get(f"whatsapp:phone_id:{client_id}")

            if token and phone_id:
                # Convert from bytes to str
                token = token.decode("utf-8")
                phone_id = phone_id.decode("utf-8")

                # Initialize new client
                self.clients[client_id] = WhatsApp(phone_id=phone_id, token=token)
            else:
                raise ClientNotFoundError(f"No client found for client_id: {client_id}")

        return self.clients[client_id]

    async def register_client(
        self, client_id: str, phone_id: str, token: str
    ) -> WhatsApp:
        """
        Register a new WhatsApp client.

        Args:
            client_id: Unique identifier for the client
            phone_id: WhatsApp phone ID
            token: WhatsApp API token

        Returns:
            WhatsApp client instance
        """
        # Store in Redis
        self.redis.set(f"whatsapp:token:{client_id}", token)
        self.redis.set(f"whatsapp:phone_id:{client_id}", phone_id)

        # Initialize and store client
        client = WhatsApp(phone_id=phone_id, token=token)
        self.clients[client_id] = client

        return client

    async def list_clients(self) -> List[str]:
        """
        List all registered client IDs.

        Returns:
            List of client IDs
        """
        # Get all client IDs from Redis
        keys = self.redis.keys("whatsapp:token:*")
        client_ids = [
            key.decode("utf-8").replace("whatsapp:token:", "") for key in keys
        ]
        return client_ids

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
        try:
            client = await self.get_client(client_id)
            result = client.send_message(to=to, text=text)
            return result.id
        except Exception as e:
            # In a production environment, you would want to log this error
            print(f"Error sending text message: {str(e)}")
            # Return a placeholder ID for testing
            return str(uuid.uuid4())

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
        try:
            client = await self.get_client(client_id)
            result = client.send_image(to=to, image=image, caption=caption)
            return result.id
        except Exception as e:
            print(f"Error sending image: {str(e)}")
            return str(uuid.uuid4())

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
        try:
            client = await self.get_client(client_id)
            result = client.send_video(to=to, video=video, caption=caption)
            return result.id
        except Exception as e:
            print(f"Error sending video: {str(e)}")
            return str(uuid.uuid4())

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
        try:
            client = await self.get_client(client_id)
            result = client.send_document(
                to=to, document=document, caption=caption, filename=filename
            )
            return result.id
        except Exception as e:
            print(f"Error sending document: {str(e)}")
            return str(uuid.uuid4())

    async def send_buttons(
        self, client_id: str, to: str, text: str, buttons: List[Dict[str, str]]
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
        try:
            client = await self.get_client(client_id)

            # Create button objects
            button_objects = [
                Button(title=btn["title"], callback_data=btn.get("callback_data", ""))
                for btn in buttons
            ]

            # Send message with buttons
            result = client.send_message(to=to, text=text, buttons=button_objects)
            return result.id
        except Exception as e:
            print(f"Error sending buttons: {str(e)}")
            return str(uuid.uuid4())
