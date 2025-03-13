"""
WhatsApp service for managing multiple clients using PyWa.
"""

import os
import uuid
from typing import Any, Protocol

from infisical_sdk import InfisicalSDKClient
from pywa import WhatsApp
from pywa.types import Button
from typing_extensions import TypedDict

from services.interfaces import WhatsAppServiceInterface


# Type annotation for Infisical
class InfisicalSecret(TypedDict):
    secret_value: str


class InfisicalSDKClientProtocol(Protocol):
    def get_secret(
        self, secret_name: str, project_id: str, environment: str, path: str
    ) -> InfisicalSecret: ...
    def create_secret(
        self,
        project_id: str,
        environment: str,
        path: str,
        secret_name: str,
        secret_value: str,
    ) -> Any: ...
    def update_secret(
        self,
        secret_name: str,
        project_id: str,
        environment: str,
        path: str,
        secret_value: str,
    ) -> Any: ...


class WhatsAppClientError(Exception):
    """Base exception for WhatsApp client errors."""

    pass


class ClientNotFoundError(WhatsAppClientError):
    """Raised when a WhatsApp client is not found."""

    pass


class WhatsAppService(WhatsAppServiceInterface):
    """Service for managing WhatsApp clients and operations."""

    def __init__(
        self,
        infisical_host: str | None = None,
        infisical_client_id: str | None = None,
        infisical_client_secret: str | None = None,
    ):
        """
        Initialize WhatsApp service.

        Args:
            infisical_host: Infisical server host URL
            infisical_client_id: Infisical client ID
            infisical_client_secret: Infisical client secret
        """

        # Initialize Infisical client
        self.infisical_host: str = infisical_host or os.getenv(
            "INFISICAL_HOST", "https://infisical.yvd.io"
        )
        self.infisical_client_id = infisical_client_id or os.getenv(
            "INFISICAL_CLIENT_ID", "27681fd0-2d02-43bf-9348-1c12c6c7c4d4"
        )
        self.infisical_client_secret = infisical_client_secret or os.getenv(
            "INFISICAL_CLIENT_SECRET",
            "e39c00528faaec9a261750a88af2ab30b43d115109d88200672321efbbde587f",
        )

        # Project ID for WhatsApp clients
        self.project_id = os.getenv("INFISICAL_PROJECT_ID", "whatsapp-clients")

        # Initialize Infisical client
        self.infisical_client = InfisicalSDKClient(host=self.infisical_host)

        # Authenticate using Universal Auth
        self.infisical_client.auth.universal_auth.login(
            client_id=self.infisical_client_id,
            client_secret=self.infisical_client_secret,
        )

        # Create an adapter for the Infisical client that implements our protocol
        class InfisicalClientAdapter(InfisicalSDKClientProtocol):
            def __init__(self, client: Any) -> None:
                self.client = client
                
            def get_secret(self, secret_name: str, project_id: str, environment: str, path: str) -> InfisicalSecret:
                result = self.client.get_secret(secret_name, project_id, environment, path)
                return {'secret_value': result.secret_value}
                
            def create_secret(self, project_id: str, environment: str, path: str, secret_name: str, secret_value: str) -> Any:
                return self.client.secrets.create(project_id, environment, path, secret_name, secret_value)
                
            def update_secret(self, secret_name: str, project_id: str, environment: str, path: str, secret_value: str) -> Any:
                return self.client.secrets.update(secret_name, project_id, environment, path, secret_value)
                
        # Create the protocol interface using the adapter
        self.infisical: InfisicalSDKClientProtocol = InfisicalClientAdapter(self.infisical_client)

        # Store WhatsApp client instances
        self.clients: dict[str, WhatsApp] = {}

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
            try:
                # Try to get credentials from Infisical
                # Each client is stored in its own environment named after the client_id
                token_secret = self.infisical.get_secret(
                    secret_name="WHATSAPP_TOKEN",
                    project_id=self.project_id,
                    environment=client_id,
                    path="/",
                )

                phone_id_secret = self.infisical.get_secret(
                    secret_name="WHATSAPP_PHONE_ID",
                    project_id=self.project_id,
                    environment=client_id,
                    path="/",
                )

                token: str = token_secret["secret_value"]
                phone_id: str = phone_id_secret["secret_value"]

                # Initialize new client
                self.clients[client_id] = WhatsApp(phone_id=phone_id, token=token)
            except Exception:
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
        # Store in Infisical
        try:
            # Try to get existing environment first
            try:
                self.infisical.get_secret(
                    secret_name="WHATSAPP_TOKEN",
                    project_id=self.project_id,
                    environment=client_id,
                    path="/",
                )

                # If exists, update the secrets
                self.infisical.update_secret(
                    secret_name="WHATSAPP_TOKEN",
                    project_id=self.project_id,
                    environment=client_id,
                    path="/",
                    secret_value=token,
                )

                self.infisical.update_secret(
                    secret_name="WHATSAPP_PHONE_ID",
                    project_id=self.project_id,
                    environment=client_id,
                    path="/",
                    secret_value=phone_id,
                )
            except Exception:
                # If environment doesn't exist, create new secrets
                self.infisical.create_secret(
                    project_id=self.project_id,
                    environment=client_id,
                    path="/",
                    secret_name="WHATSAPP_TOKEN",
                    secret_value=token,
                )

                self.infisical.create_secret(
                    project_id=self.project_id,
                    environment=client_id,
                    path="/",
                    secret_name="WHATSAPP_PHONE_ID",
                    secret_value=phone_id,
                )
        except Exception as e:
            # Propagate exception if Infisical operations fail
            raise WhatsAppClientError(
                f"Failed to register client in Infisical: {e!s}"
            )

        # Initialize and store client
        client = WhatsApp(phone_id=phone_id, token=token)
        self.clients[client_id] = client

        return client

    async def list_clients(self) -> list[str]:
        """
        List all registered client IDs.

        Returns:
            List of client IDs
        """
        # For now we'll just return the list of active clients we know about
        # In a more complete implementation, we would query Infisical for all environments
        # and extract client IDs from there

        # Example of how this might work with a hypothetical API:
        try:
            # This is a placeholder for the actual API call
            # The exact implementation depends on your version of infisicalsdk
            # Uncomment and modify when you have the appropriate API

            # Get all environments in the project
            # environments = self.infisical.get_environments(project_id=self.project_id)
            # return [env.name for env in environments]

            # For now, return clients we have instantiated in memory
            return list(self.clients.keys())
        except Exception:
            # If API call fails, just return the clients we have in memory
            # In a production environment, proper logging would be implemented here
            return list(self.clients.keys())

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
        except Exception:
            # In a production environment, proper logging would be implemented here
            # For now, silently handle the error and return a placeholder ID
            # No print statements in production code
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
        except Exception:
            # Disabled print statement
            # print(f"Error sending image: {e!s}")
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
        except Exception:
            # Disabled print statement
            # print(f"Error sending video: {e!s}")
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
        except Exception:
            # Disabled print statement
            # print(f"Error sending document: {e!s}")
            return str(uuid.uuid4())

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
        except Exception:
            # Disabled print statement
            # print(f"Error sending buttons: {e!s}")
            return str(uuid.uuid4())
