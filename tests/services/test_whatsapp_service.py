"""
Tests for WhatsApp service mock implementation.
"""

import asyncio
import unittest
from unittest.mock import patch

from services.whatsapp_service_mock import MockWhatsAppService


class TestWhatsAppServiceMock(unittest.TestCase):
    """Test suite for the WhatsApp service mock implementation."""

    def setUp(self):
        """Set up test environment."""
        self.service = MockWhatsAppService()
        # For asyncio tests
        self.loop = asyncio.get_event_loop()

    def test_register_client(self):
        """Test registering a new WhatsApp client."""
        # Register a client
        client = self.loop.run_until_complete(
            self.service.register_client(
                client_id="test_client", phone_id="123456789", token="test_token"
            )
        )

        # Check if client was registered properly
        self.assertIn("test_client", self.service.clients)
        self.assertEqual(self.service.tokens["test_client"], "test_token")
        self.assertEqual(self.service.phone_ids["test_client"], "123456789")

    def test_get_client_existing(self):
        """Test retrieving an existing client."""
        # Register a client first
        self.loop.run_until_complete(
            self.service.register_client(
                client_id="test_client", phone_id="123456789", token="test_token"
            )
        )

        # Get the client
        client = self.loop.run_until_complete(self.service.get_client("test_client"))

        # Verify the client
        self.assertEqual(client.phone_id, "123456789")
        self.assertEqual(client.token, "test_token")

    def test_get_client_nonexisting(self):
        """Test getting a non-existing client raises an error."""
        with self.assertRaises(ValueError):
            self.loop.run_until_complete(self.service.get_client("non_existing_client"))

    def test_list_clients(self):
        """Test listing registered clients."""
        # Register two clients
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

        # Verify the list contains both client IDs
        self.assertIn("client1", clients)
        self.assertIn("client2", clients)
        self.assertEqual(len(clients), 2)

    def test_send_text(self):
        """Test sending a text message."""
        # Register a client
        self.loop.run_until_complete(
            self.service.register_client(
                client_id="test_client", phone_id="123456789", token="test_token"
            )
        )

        # Send a text message
        with patch("builtins.print") as mock_print:
            message_id = self.loop.run_until_complete(
                self.service.send_text(
                    client_id="test_client", to="987654321", text="Hello world"
                )
            )

            # Check if message ID is returned and print was called
            self.assertIsNotNone(message_id)
            mock_print.assert_called_with(
                "[MOCK] Sending message to 987654321: Hello world"
            )

    def test_send_image(self):
        """Test sending an image."""
        # Register a client
        self.loop.run_until_complete(
            self.service.register_client(
                client_id="test_client", phone_id="123456789", token="test_token"
            )
        )

        # Send an image
        with patch("builtins.print") as mock_print:
            message_id = self.loop.run_until_complete(
                self.service.send_image(
                    client_id="test_client",
                    to="987654321",
                    image="https://example.com/image.jpg",
                    caption="An image",
                )
            )

            # Check if message ID is returned and print was called
            self.assertIsNotNone(message_id)
            mock_print.assert_any_call(
                "[MOCK] Sending image to 987654321: https://example.com/image.jpg"
            )
            mock_print.assert_any_call("[MOCK] With caption: An image")

    def test_send_buttons(self):
        """Test sending a message with buttons."""
        # Register a client
        self.loop.run_until_complete(
            self.service.register_client(
                client_id="test_client", phone_id="123456789", token="test_token"
            )
        )

        # Create buttons
        buttons = [
            {"title": "Button 1", "callback_data": "btn1"},
            {"title": "Button 2", "callback_data": "btn2"},
        ]

        # Send buttons
        with patch("builtins.print") as mock_print:
            message_id = self.loop.run_until_complete(
                self.service.send_buttons(
                    client_id="test_client",
                    to="987654321",
                    text="Choose an option",
                    buttons=buttons,
                )
            )

            # Check if message ID is returned and print was called
            self.assertIsNotNone(message_id)
            mock_print.assert_any_call(
                "[MOCK] Sending message to 987654321: Choose an option"
            )
            mock_print.assert_any_call("[MOCK] With buttons: ['Button 1', 'Button 2']")


if __name__ == "__main__":
    unittest.main()
