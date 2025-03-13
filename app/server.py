#!/usr/bin/env python
"""
Tools System MCP Server
Provides messaging and notification tools using the Model Context Protocol
"""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List

import dotenv
from mcp.server.fastmcp import Context, FastMCP

from services.message_service_mock import MockMessageService
from services.whatsapp_service_mock import (
    MockWhatsAppService,  # Add import for WhatsApp service
)

# Load environment variables from .env file
dotenv_path = Path(__file__).parent.parent / ".env"
if dotenv_path.exists():
    dotenv.load_dotenv(str(dotenv_path))

# Import tools
# Import services
from tools.alert_tool import AlertTool
from tools.button_tool import ButtonTool
from tools.document_tool import DocumentTool
from tools.image_tool import ImageTool
from tools.sleep_tool import SleepTool
from tools.text_tool import TextTool
from tools.video_tool import VideoTool

# Create the MCP server
mcp = FastMCP(title="YaVendió Tools")


@asynccontextmanager
async def lifespan(_: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Application lifecycle management with typed context."""
    # Setup resources
    message_service = MockMessageService()  # Using mock service for tests
    whatsapp_service = MockWhatsAppService()  # Add WhatsApp service

    try:
        # Yield shared context
        lifespan_context = {
            "message_service": message_service,
            "whatsapp_service": whatsapp_service,  # Add WhatsApp service to context
        }
        yield lifespan_context
    finally:
        # Cleanup resources
        pass


@mcp.tool()
async def send_text(
    ctx: Context,
    company_id: str,
    phone_number: str,
    message: str,
) -> Dict[str, Any]:
    """Send a text message to a phone number.

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        message: Text to send
    """
    context = {
        "company_id": company_id,
        "phone_number": phone_number,
        "lifespan_context": ctx.request_context.lifespan_context,
    }

    tool = TextTool(message)
    message_id = await tool.execute(context)

    return {
        "status": "success",
        "message_id": message_id,
    }


@mcp.tool()
async def send_image(
    ctx: Context,
    company_id: str,
    phone_number: str,
    image_urls: List[str],
) -> Dict[str, Any]:
    """Send one or more images to a phone number.

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        image_urls: List of image URLs to send
    """
    context = {
        "company_id": company_id,
        "phone_number": phone_number,
        "lifespan_context": ctx.request_context.lifespan_context,
    }

    tool = ImageTool(image_urls)
    message_ids = await tool.execute(context)

    return {
        "status": "success",
        "message_ids": message_ids,
    }


@mcp.tool()
async def send_video(
    ctx: Context,
    company_id: str,
    phone_number: str,
    video_urls: List[str],
) -> Dict[str, Any]:
    """Send one or more videos to a phone number.

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        video_urls: List of video URLs to send
    """
    context = {
        "company_id": company_id,
        "phone_number": phone_number,
        "lifespan_context": ctx.request_context.lifespan_context,
    }

    tool = VideoTool(video_urls)
    message_ids = await tool.execute(context)

    return {
        "status": "success",
        "message_ids": message_ids,
    }


@mcp.tool()
async def send_document(
    ctx: Context,
    company_id: str,
    phone_number: str,
    files: List[Dict[str, str]],
) -> Dict[str, Any]:
    """Send document files to a phone number.

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        files: List of document files as {"url": "...", "filename": "..."}
    """
    context = {
        "company_id": company_id,
        "phone_number": phone_number,
        "lifespan_context": ctx.request_context.lifespan_context,
    }

    tool = DocumentTool(files)
    message_ids = await tool.execute(context)

    return {
        "status": "success",
        "message_ids": message_ids,
    }


@mcp.tool()
async def send_alert(
    ctx: Context,
    company_id: str,
    phone_number: str,
    message: str,
    whatsapp: bool = False,
    email: Dict[str, Any] | None = None,
    sms: Dict[str, Any] | None = None,
    pause_number: bool = False,
    track_sale: bool = False,
) -> Dict[str, Any]:
    """Send alerts through multiple channels (WhatsApp, Email, SMS).

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        message: Alert message
        whatsapp: Whether to send WhatsApp message
        email: Email configuration {"subject": "..."}
        sms: SMS configuration {"type": "...", "recipients": ["..."]}
        pause_number: Whether to pause the conversation
        track_sale: Whether to track this as a sale
    """
    context = {
        "company_id": company_id,
        "phone_number": phone_number,
        "lifespan_context": ctx.request_context.lifespan_context,
    }

    tool = AlertTool(
        message,
        whatsapp=whatsapp,
        email=email,
        sms=sms,
        pause_number=pause_number,
        track_sale=track_sale,
    )
    result = await tool.execute(context)

    return {
        "status": "success",
        "result": result,
    }


@mcp.tool()
async def sleep(
    ctx: Context,
    company_id: str,
    phone_number: str,
    seconds: int,
) -> Dict[str, Any]:
    """Pause execution for specified seconds.

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        seconds: Number of seconds to sleep
    """
    context = {
        "company_id": company_id,
        "phone_number": phone_number,
        "lifespan_context": ctx.request_context.lifespan_context,
    }

    tool = SleepTool(seconds)
    await tool.execute(context)

    return {
        "status": "success",
        "seconds": seconds,
    }


@mcp.tool()
async def send_button(
    ctx: Context,
    company_id: str,
    phone_number: str,
    body_text: str,
    buttons: List[Dict[str, str]],
    button_type: str = "reply",
    header: Dict[str, Any] | None = None,
    footer_text: str | None = None,
    payment_data: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    """Send interactive buttons.

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        body_text: Button message body
        buttons: List of button configs [{"id": "...", "title": "..."}]
        button_type: "reply" or "payment"
        header: Optional header configuration
        footer_text: Optional footer text
        payment_data: Payment data for payment buttons
    """
    context = {
        "company_id": company_id,
        "phone_number": phone_number,
        "lifespan_context": ctx.request_context.lifespan_context,
    }

    tool = ButtonTool(
        body_text,
        buttons,
        button_type,
        header=header,
        footer_text=footer_text,
        payment_data=payment_data,
    )
    message_id = await tool.execute(context)

    return {
        "status": "success",
        "message_id": message_id,
    }


@mcp.tool()
async def get_config(ctx: Context, company_id: str) -> Dict[str, Any]:
    """Get company configuration.

    Args:
        company_id: Company identifier
    """
    # Mock implementation that returns a sample config
    sample_config = {
        "welcome_message": "Hello, welcome to our service!",
        "auto_reply": True,
        "notification_emails": ["admin@example.com"],
        "company_name": "Test Company",
    }

    return {"status": "success", "source": "mock", "config": sample_config}


@mcp.tool()
async def update_config(
    ctx: Context, company_id: str, config: Dict[str, Any]
) -> Dict[str, Any]:
    """Update company configuration.

    Args:
        company_id: Company identifier
        config: New configuration
    """
    # Mock implementation that pretends to update the config
    return {"status": "success", "message": "Configuration updated (mock)"}


# Add new WhatsApp client management tools


@mcp.tool()
async def register_whatsapp_client(
    ctx: Context,
    client_id: str,
    phone_id: str,
    token: str,
) -> Dict[str, Any]:
    """Register a new WhatsApp client.

    Args:
        client_id: Unique identifier for the client
        phone_id: WhatsApp phone ID
        token: WhatsApp API token
    """
    whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]

    try:
        client = await whatsapp_service.register_client(
            client_id=client_id, phone_id=phone_id, token=token
        )
        return {
            "status": "success",
            "client_id": client_id,
            "message": f"Client registered successfully",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to register client: {str(e)}"}


@mcp.tool()
async def list_whatsapp_clients(
    ctx: Context,
) -> Dict[str, Any]:
    """List all registered WhatsApp clients.

    Returns:
        Dictionary containing the list of client IDs
    """
    whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]

    try:
        clients = await whatsapp_service.list_clients()
        return {"status": "success", "clients": clients}
    except Exception as e:
        return {"status": "error", "message": f"Failed to list clients: {str(e)}"}


@mcp.tool()
async def send_whatsapp_text(
    ctx: Context,
    client_id: str,
    phone_number: str,
    message: str,
) -> Dict[str, Any]:
    """Send a text message through WhatsApp.

    Args:
        client_id: Client to use for sending
        phone_number: Recipient's phone number
        message: Text message to send
    """
    whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]

    try:
        message_id = await whatsapp_service.send_text(
            client_id=client_id, to=phone_number, text=message
        )
        return {"status": "success", "message_id": message_id}
    except Exception as e:
        return {"status": "error", "message": f"Failed to send text message: {str(e)}"}


@mcp.tool()
async def send_whatsapp_image(
    ctx: Context,
    client_id: str,
    phone_number: str,
    image_url: str,
    caption: str | None = None,
) -> Dict[str, Any]:
    """Send an image through WhatsApp.

    Args:
        client_id: Client to use for sending
        phone_number: Recipient's phone number
        image_url: URL of the image to send
        caption: Optional caption for the image
    """
    whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]

    try:
        message_id = await whatsapp_service.send_image(
            client_id=client_id, to=phone_number, image=image_url, caption=caption
        )
        return {"status": "success", "message_id": message_id}
    except Exception as e:
        return {"status": "error", "message": f"Failed to send image: {str(e)}"}


@mcp.tool()
async def send_whatsapp_video(
    ctx: Context,
    client_id: str,
    phone_number: str,
    video_url: str,
    caption: str | None = None,
) -> Dict[str, Any]:
    """Send a video through WhatsApp.

    Args:
        client_id: Client to use for sending
        phone_number: Recipient's phone number
        video_url: URL of the video to send
        caption: Optional caption for the video
    """
    whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]

    try:
        message_id = await whatsapp_service.send_video(
            client_id=client_id, to=phone_number, video=video_url, caption=caption
        )
        return {"status": "success", "message_id": message_id}
    except Exception as e:
        return {"status": "error", "message": f"Failed to send video: {str(e)}"}


@mcp.tool()
async def send_whatsapp_document(
    ctx: Context,
    client_id: str,
    phone_number: str,
    document_url: str,
    caption: str | None = None,
    filename: str | None = None,
) -> Dict[str, Any]:
    """Send a document through WhatsApp.

    Args:
        client_id: Client to use for sending
        phone_number: Recipient's phone number
        document_url: URL of the document to send
        caption: Optional caption for the document
        filename: Optional filename for the document
    """
    whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]

    try:
        message_id = await whatsapp_service.send_document(
            client_id=client_id,
            to=phone_number,
            document=document_url,
            caption=caption,
            filename=filename,
        )
        return {"status": "success", "message_id": message_id}
    except Exception as e:
        return {"status": "error", "message": f"Failed to send document: {str(e)}"}


@mcp.tool()
async def send_whatsapp_buttons(
    ctx: Context,
    client_id: str,
    phone_number: str,
    text: str,
    buttons: List[Dict[str, str]],
) -> Dict[str, Any]:
    """Send interactive buttons through WhatsApp.

    Args:
        client_id: Client to use for sending
        phone_number: Recipient's phone number
        text: Message text to display
        buttons: List of button configs [{"title": "...", "callback_data": "..."}]
    """
    whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]

    try:
        message_id = await whatsapp_service.send_buttons(
            client_id=client_id, to=phone_number, text=text, buttons=buttons
        )
        return {"status": "success", "message_id": message_id}
    except Exception as e:
        return {"status": "error", "message": f"Failed to send buttons: {str(e)}"}


async def create_server(mcp_instance: FastMCP | None = None) -> FastMCP:
    """Create and start the MCP server with all tools registered.

    Args:
        mcp_instance: Optional existing FastMCP instance to use

    Returns:
        Configured FastMCP instance
    """
    # Use provided instance or create a new one
    server = mcp_instance or FastMCP(title="YaVendió Tools", lifespan=lifespan)

    # For FastMCP, we need to use decorator syntax to register tools
    # but we'll add the references to the tool_functions dict for documentation
    tool_functions = {
        "send_text": send_text,
        "send_image": send_image,
        "send_video": send_video,
        "send_document": send_document,
        "send_alert": send_alert,
        "sleep": sleep,
        "send_button": send_button,
        "get_config": get_config,
        "update_config": update_config,
        "register_whatsapp_client": register_whatsapp_client,
        "list_whatsapp_clients": list_whatsapp_clients,
        "send_whatsapp_text": send_whatsapp_text,
        "send_whatsapp_image": send_whatsapp_image,
        "send_whatsapp_video": send_whatsapp_video,
        "send_whatsapp_document": send_whatsapp_document,
        "send_whatsapp_buttons": send_whatsapp_buttons,
    }

    # When a mock server is provided (for testing), we need to register tools explicitly
    if mcp_instance is not None:
        # This is for test compatibility - the mock server has register_tool mocked
        for name, func in tool_functions.items():
            if hasattr(server, "register_tool"):
                server.register_tool(name, func)

    return server


if __name__ == "__main__":
    # Add logging to help debug
    import sys

    print("Starting YaVendió Tools MCP server...", file=sys.stderr)

    # Run the server directly as shown in the MCP documentation
    # No need for async setup here - mcp.run() handles it
    mcp.run()
