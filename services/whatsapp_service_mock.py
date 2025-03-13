"""
Mock implementation of WhatsApp service for testing and development.
"""

import uuid
from typing import Dict, List

from services.interfaces import WhatsAppServiceInterface


class MockWhatsAppClient:
    """Mock WhatsApp client that simulates PyWa client behavior."""

    def __init__(self, phone_id: str, token: str):
        """Initialize mock client with credentials."""
        self.phone_id = phone_id
        self.token = token

    def send_message(self, to: str, text: str, buttons=None):
        """Send a text message or message with buttons."""
        message_id = str(uuid.uuid4())
        print(f"[MOCK] Sending message to {to}: {text}")
        if buttons:
            button_texts = [b.title for b in buttons]
            print(f"[MOCK] With buttons: {button_texts}")
        return MockMessageResponse(message_id)

    def send_image(self, to: str, image: str, caption=None):
        """Send an image message."""
        message_id = str(uuid.uuid4())
        print(f"[MOCK] Sending image to {to}: {image}")
        if caption:
            print(f"[MOCK] With caption: {caption}")
        return MockMessageResponse(message_id)

    def send_video(self, to: str, video: str, caption=None):
        """Send a video message."""
        message_id = str(uuid.uuid4())
        print(f"[MOCK] Sending video to {to}: {video}")
        if caption:
            print(f"[MOCK] With caption: {caption}")
        return MockMessageResponse(message_id)

    def send_document(self, to: str, document: str, caption=None, filename=None):
        """Send a document message."""
        message_id = str(uuid.uuid4())
        print(f"[MOCK] Sending document to {to}: {document}")
        if caption:
            print(f"[MOCK] With caption: {caption}")
        if filename:
            print(f"[MOCK] With filename: {filename}")
        return MockMessageResponse(message_id)


class MockMessageResponse:
    """Mock message response that simulates PyWa response."""

    def __init__(self, message_id: str):
        """Initialize with message ID."""
        self.id = message_id


class MockWhatsAppService(WhatsAppServiceInterface):
    """In-memory mock implementation of WhatsApp service."""

    def __init__(self):
        """Initialize mock service."""
        self.clients = {}  # client_id -> MockWhatsAppClient
        self.tokens = {}  # client_id -> token
        self.phone_ids = {}  # client_id -> phone_id

    async def get_client(self, client_id: str) -> MockWhatsAppClient:
        """
        Get a WhatsApp client by client_id.

        Args:
            client_id: Unique identifier for the client

        Returns:
            MockWhatsAppClient instance
        """
        if client_id not in self.clients:
            if client_id in self.tokens and client_id in self.phone_ids:
                # Initialize new client
                self.clients[client_id] = MockWhatsAppClient(
                    phone_id=self.phone_ids[client_id], token=self.tokens[client_id]
                )
            else:
                raise ValueError(f"No client found for client_id: {client_id}")

        return self.clients[client_id]

    async def register_client(
        self, client_id: str, phone_id: str, token: str
    ) -> MockWhatsAppClient:
        """
        Register a new WhatsApp client.

        Args:
            client_id: Unique identifier for the client
            phone_id: WhatsApp phone ID
            token: WhatsApp API token

        Returns:
            MockWhatsAppClient instance
        """
        # Store credentials
        self.tokens[client_id] = token
        self.phone_ids[client_id] = phone_id

        # Initialize and store client
        client = MockWhatsAppClient(phone_id=phone_id, token=token)
        self.clients[client_id] = client

        print(f"[MOCK] Registered client {client_id} with phone_id {phone_id}")
        return client

    async def list_clients(self) -> List[str]:
        """
        List all registered client IDs.

        Returns:
            List of client IDs
        """
        return list(self.tokens.keys())

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
        client = await self.get_client(client_id)
        result = client.send_message(to=to, text=text)
        return result.id

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
        client = await self.get_client(client_id)
        result = client.send_image(to=to, image=image, caption=caption)
        return result.id

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
        client = await self.get_client(client_id)
        result = client.send_video(to=to, video=video, caption=caption)
        return result.id

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
        client = await self.get_client(client_id)
        result = client.send_document(
            to=to, document=document, caption=caption, filename=filename
        )
        return result.id

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

        # Convert dict buttons to mock Button objects
        class MockButton:
            def __init__(self, title, callback_data):
                self.title = title
                self.callback_data = callback_data

        button_objects = [
            MockButton(title=btn["title"], callback_data=btn.get("callback_data", ""))
            for btn in buttons
        ]

        client = await self.get_client(client_id)
        result = client.send_message(to=to, text=text, buttons=button_objects)
        return result.id
