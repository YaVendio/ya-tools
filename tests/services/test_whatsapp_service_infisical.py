"""
Tests for WhatsApp service with Infisical integration.
"""

import asyncio
import unittest
from typing import Any, cast
from unittest.mock import MagicMock, patch

from services.whatsapp_service import InfisicalSDKClientProtocol, WhatsAppService


class TestWhatsAppServiceInfisical(unittest.TestCase):
    """Test cases for the WhatsApp service with Infisical integration."""

    def setUp(self):
        """Set up test environment."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Mock Infisical client
        self.infisical_mock = MagicMock(spec=InfisicalSDKClientProtocol)

        # Create service with mocks
        with patch("infisical_sdk.InfisicalSDKClient", return_value=self.infisical_mock):
            self.service = WhatsAppService(
                infisical_host="https://infisical.yvd.io",
                infisical_client_id="test_client_id",
                infisical_client_secret="test_client_secret",
            )

            # Replace real infisical with mock
            self.service.infisical = self.infisical_mock

    def test_register_client_infisical(self):
        """Test registering a new WhatsApp client with Infisical."""
        client_id = "test_client"
        phone_id = "123456789"
        token = "test_token"

        # Mock successful secret creation
        mock_get_secret = cast(Any, self.service.infisical.get_secret)
        mock_get_secret.side_effect = Exception("Secret not found")
        
        mock_create_secret = cast(Any, self.service.infisical.create_secret)
        mock_create_secret.return_value = MagicMock()

        # Register client
        client = self.loop.run_until_complete(
            self.service.register_client(
                client_id=client_id, phone_id=phone_id, token=token
            )
        )

        # Check client was created
        self.assertIsNotNone(client)

        # Verify Infisical called with correct parameters for token
        mock_create_secret = cast(Any, self.service.infisical.create_secret)
        mock_create_secret.assert_any_call(
            project_id=self.service.project_id,
            environment=client_id,
            path="/",
            secret_name="WHATSAPP_TOKEN",
            secret_value=token,
        )

        # Verify Infisical called with correct parameters for phone_id
        mock_create_secret = cast(Any, self.service.infisical.create_secret)
        mock_create_secret.assert_any_call(
            project_id=self.service.project_id,
            environment=client_id,
            path="/",
            secret_name="WHATSAPP_PHONE_ID",
            secret_value=phone_id,
        )

        # No need to verify Redis wasn't used since it's completely removed

    def test_register_client_infisical_update(self):
        """Test updating existing WhatsApp client with Infisical."""
        client_id = "test_client"
        phone_id = "123456789"
        token = "test_token"

        # Mock secret already exists
        mock_get_secret = cast(Any, self.service.infisical.get_secret)
        mock_get_secret.return_value = MagicMock()
        
        mock_update_secret = cast(Any, self.service.infisical.update_secret)
        mock_update_secret.return_value = MagicMock()

        # Register client
        client = self.loop.run_until_complete(
            self.service.register_client(
                client_id=client_id, phone_id=phone_id, token=token
            )
        )

        # Check client was created
        self.assertIsNotNone(client)

        # Verify update_secret was called for token
        mock_update_secret = cast(Any, self.service.infisical.update_secret)
        mock_update_secret.assert_any_call(
            secret_name="WHATSAPP_TOKEN",
            project_id=self.service.project_id,
            environment=client_id,
            path="/",
            secret_value=token,
        )

        # Verify update_secret was called for phone_id
        mock_update_secret = cast(Any, self.service.infisical.update_secret)
        mock_update_secret.assert_any_call(
            secret_name="WHATSAPP_PHONE_ID",
            project_id=self.service.project_id,
            environment=client_id,
            path="/",
            secret_value=phone_id,
        )

        # No need to verify Redis wasn't used since it's completely removed

    def test_register_client_infisical_error_handling(self):
        """Test error handling when Infisical fails (no Redis fallback)."""
        client_id = "test_client"
        phone_id = "123456789"
        token = "test_token"

        # Mock Infisical failure
        mock_get_secret = cast(Any, self.service.infisical.get_secret)
        mock_get_secret.side_effect = Exception("Connection error")
        
        mock_create_secret = cast(Any, self.service.infisical.create_secret)
        mock_create_secret.side_effect = Exception("Connection error")

        # Register client - should handle errors gracefully
        with self.assertRaises(Exception):
            self.loop.run_until_complete(
                self.service.register_client(
                    client_id=client_id, phone_id=phone_id, token=token
                )
            )

    def test_get_client_infisical(self):
        """Test retrieving client from Infisical."""
        client_id = "test_client"
        phone_id = "123456789"
        token = "test_token"

        # Create secret return values
        token_secret = MagicMock()
        token_secret.secret_value = token
        phone_id_secret = MagicMock()
        phone_id_secret.secret_value = phone_id

        # Mock successful secret retrieval
        mock_get_secret = cast(Any, self.service.infisical.get_secret)
        mock_get_secret.side_effect = [token_secret, phone_id_secret]

        # Get client
        client = self.loop.run_until_complete(
            self.service.get_client(client_id=client_id)
        )

        # Check client properties
        self.assertIsNotNone(client)
        self.assertEqual(client.phone_id, phone_id)
        self.assertEqual(client.token, token)

        # Verify Infisical was called
        mock_get_secret = cast(Any, self.service.infisical.get_secret)
        mock_get_secret.assert_any_call(
            secret_name="WHATSAPP_TOKEN",
            project_id=self.service.project_id,
            environment=client_id,
            path="/",
        )

        mock_get_secret.assert_any_call(
            secret_name="WHATSAPP_PHONE_ID",
            project_id=self.service.project_id,
            environment=client_id,
            path="/",
        )

        # No need to verify Redis wasn't used since it's completely removed

    def test_get_client_infisical_error_handling(self):
        """Test error handling when Infisical fails (no Redis fallback)."""
        client_id = "test_client"

        # Mock Infisical failure
        mock_get_secret = cast(Any, self.service.infisical.get_secret)
        mock_get_secret.side_effect = Exception("Connection error")

        # Get client should raise an exception without Redis fallback
        with self.assertRaises(Exception):
            self.loop.run_until_complete(self.service.get_client(client_id=client_id))

    def test_list_clients(self):
        """Test listing clients from in-memory store."""
        # Setup some clients in the in-memory store
        self.service.clients = {"client1": MagicMock(), "client2": MagicMock()}

        # List clients
        clients = self.loop.run_until_complete(self.service.list_clients())

        # Check result
        self.assertEqual(len(clients), 2)
        self.assertIn("client1", clients)
        self.assertIn("client2", clients)


if __name__ == "__main__":
    unittest.main()
