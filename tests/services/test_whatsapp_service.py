"""
Tests for WhatsApp service mock implementation.
"""

import asyncio
import unittest
from unittest.mock import patch

from services.whatsapp_service_mock import MockWhatsAppService


class TestWhatsAppServiceMock(unittest.TestCase):
    """Test cases for the WhatsApp service mock."""

    def setUp(self):
        """Set up test environment."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.service = MockWhatsAppService()

    def test_register_client(self):
        """Test registering a new WhatsApp client."""
        # Register a client
        with patch("logging.Logger.info") as mock_logger:
            _ = self.loop.run_until_complete(
                self.service.register_client(
                    client_id="test_client", phone_id="123456789", token="test_token"
                )
            )

            # Check if client was registered and logger was called
            mock_logger.assert_called_with(
                "[MOCK] Registered client test_client with phone_id 123456789"
            )

    def test_get_client_existing(self):
        """Test getting an existing WhatsApp client."""
        # First register a client
        with patch("logging.Logger.info"):
            client = self.loop.run_until_complete(
                self.service.register_client(
                    client_id="test_client", phone_id="123456789", token="test_token"
                )
            )

        # Then get the client
        result = self.loop.run_until_complete(
            self.service.get_client(client_id="test_client")
        )

        # Check if client was returned and has the right properties
        self.assertIsNotNone(result)
        self.assertEqual(result.phone_id, "123456789")
        self.assertEqual(result.token, "test_token")

    def test_get_client_nonexisting(self):
        """Test getting a non-existing WhatsApp client."""
        # This should raise an exception
        with self.assertRaises(ValueError):
            self.loop.run_until_complete(
                self.service.get_client(client_id="nonexistent")
            )

    def test_list_clients(self):
        """Test listing all registered WhatsApp clients."""
        # Register a couple of clients
        with patch("logging.Logger.info"):
            self.loop.run_until_complete(
                self.service.register_client(
                    client_id="client1", phone_id="123456789", token="token1"
                )
            )
            self.loop.run_until_complete(
                self.service.register_client(
                    client_id="client2", phone_id="987654321", token="token2"
                )
            )

        # List clients
        clients = self.loop.run_until_complete(self.service.list_clients())

        # Check if both clients are in the list
        self.assertEqual(len(clients), 2)
        self.assertIn("client1", clients)
        self.assertIn("client2", clients)

    def test_send_text(self):
        """Test sending a text message."""
        # Register a client first
        with patch("logging.Logger.info"):
            self.loop.run_until_complete(
                self.service.register_client(
                    client_id="test_client", phone_id="123456789", token="test_token"
                )
            )

        # Send a text message
        with patch("logging.Logger.info") as mock_logger:
            message_id = self.loop.run_until_complete(
                self.service.send_text(
                    client_id="test_client", to="987654321", text="Hello, world!"
                )
            )

            # Check if message ID is returned and logger was called
            self.assertIsNotNone(message_id)
            mock_logger.assert_called_with(
                "[MOCK] Sending message to 987654321: Hello, world!"
            )

    def test_send_image(self):
        """Test sending an image message."""
        # Register a client first
        with patch("logging.Logger.info"):
            self.loop.run_until_complete(
                self.service.register_client(
                    client_id="test_client", phone_id="123456789", token="test_token"
                )
            )

        # Send an image message
        with patch("logging.Logger.info") as mock_logger:
            message_id = self.loop.run_until_complete(
                self.service.send_image(
                    client_id="test_client",
                    to="987654321",
                    image="https://example.com/image.jpg",
                    caption="Check this out",
                )
            )

            # Check if message ID is returned and logger was called
            self.assertIsNotNone(message_id)
            mock_logger.assert_any_call(
                "[MOCK] Sending image to 987654321: https://example.com/image.jpg"
            )
            mock_logger.assert_any_call("[MOCK] With caption: Check this out")

    def test_send_buttons(self):
        """Test sending buttons."""
        # Register a client first
        with patch("logging.Logger.info"):
            self.loop.run_until_complete(
                self.service.register_client(
                    client_id="test_client", phone_id="123456789", token="test_token"
                )
            )

        # Create mock buttons
        buttons = [
            {"title": "Button 1", "callback_data": "btn1"},
            {"title": "Button 2", "callback_data": "btn2"},
        ]

        # Send buttons
        with patch("logging.Logger.info") as mock_logger:
            message_id = self.loop.run_until_complete(
                self.service.send_buttons(
                    client_id="test_client",
                    to="987654321",
                    text="Choose an option",
                    buttons=buttons,
                )
            )

            # Check if message ID is returned and logger was called
            self.assertIsNotNone(message_id)
            mock_logger.assert_any_call(
                "[MOCK] Sending message to 987654321: Choose an option"
            )
            mock_logger.assert_any_call("[MOCK] With buttons: ['Button 1', 'Button 2']")


if __name__ == "__main__":
    unittest.main()
