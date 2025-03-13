#!/usr/bin/env python
"""
Tools System MCP Server
Provides messaging and notification tools using the Model Context Protocol
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import dotenv
from mcp.server.fastmcp import Context, FastMCP

from services.message_service_mock import MockMessageService
from services.whatsapp_service_mock import MockWhatsAppService
from tools.alert_tool import AlertTool
from tools.button_tool import ButtonTool
from tools.document_tool import DocumentTool
from tools.image_tool import ImageTool
from tools.sleep_tool import SleepTool
from tools.text_tool import TextTool
from tools.video_tool import VideoTool

# Load environment variables from .env file
dotenv_path = Path(__file__).parent.parent / ".env"
if dotenv_path.exists():
    dotenv.load_dotenv(str(dotenv_path))

# Create the MCP server
mcp = FastMCP(title="YaVendió Tools")


@asynccontextmanager
async def lifespan(_: FastMCP) -> AsyncIterator[dict[str, Any]]:
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
    client_id: str | None = None,  # Optional parameter for specific client selection
) -> dict[str, Any]:
    """Send a text message to a phone number.

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        message: Text to send
        client_id: Optional WhatsApp client ID (if None, uses default client for company)
    """
    # If client_id is provided, use WhatsApp service directly
    if client_id:
        whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]
        try:
            message_id = await whatsapp_service.send_text(
                client_id=client_id, to=phone_number, text=message
            )
            return {"status": "success", "message_id": message_id}
        except Exception as e:
            return {"status": "error", "message": f"Failed to send message: {e!s}"}

    # Otherwise use the TextTool for general routing
    context: dict[str, Any] = {
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
    image_urls: list[str] | str,
    client_id: str | None = None,
    caption: str | None = None,
) -> dict[str, Any]:
    """Send one or more images to a phone number.

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        image_urls: Single image URL or list of image URLs to send
        client_id: Optional WhatsApp client ID (if None, uses default client for company)
        caption: Optional caption for the image (only used with client_id)
    """
    # If client_id is provided, use WhatsApp service directly
    if client_id:
        whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]
        try:
            # For WhatsApp service, we can only send one image at a time
            image_url = image_urls[0] if isinstance(image_urls, list) else image_urls
            message_id = await whatsapp_service.send_image(
                client_id=client_id,
                to=phone_number,
                image=image_url,
                caption=caption or "",
            )
            return {"status": "success", "message_id": message_id}
        except Exception as e:
            return {"status": "error", "message": f"Failed to send image: {e!s}"}

    # Otherwise use the ImageTool for general routing
    context: dict[str, Any] = {
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
    video_urls: list[str] | str,
    client_id: str | None = None,
    caption: str | None = None,
) -> dict[str, Any]:
    """Send one or more videos to a phone number.

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        video_urls: Single video URL or list of video URLs to send
        client_id: Optional WhatsApp client ID (if None, uses default client for company)
        caption: Optional caption for the video (only used with client_id)
    """
    # If client_id is provided, use WhatsApp service directly
    if client_id:
        whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]
        try:
            # For WhatsApp service, we can only send one video at a time
            video_url = video_urls[0] if isinstance(video_urls, list) else video_urls
            message_id = await whatsapp_service.send_video(
                client_id=client_id,
                to=phone_number,
                video=video_url,
                caption=caption or "",
            )
            return {"status": "success", "message_id": message_id}
        except Exception as e:
            return {"status": "error", "message": f"Failed to send video: {e!s}"}

    # Otherwise use the VideoTool for general routing
    context: dict[str, Any] = {
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
    files: list[dict[str, str]] | dict[str, str] | str,
    client_id: str | None = None,
    caption: str | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Send document files to a phone number.

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        files: Single document URL as string, a dict {"url": "...", "filename": "..."}
               or list of document files as {"url": "...", "filename": "..."}
        client_id: Optional WhatsApp client ID (if None, uses default client for company)
        caption: Optional caption for the document (only used with client_id)
        filename: Optional filename for the document (only used with client_id and string URL)
    """
    # If client_id is provided, use WhatsApp service directly
    if client_id:
        whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]
        try:
            # Extract document URL and filename based on input type
            document_url: str = ""
            doc_filename: str = "document.pdf"  # Default filename

            if isinstance(files, str):
                document_url = files
                doc_filename = filename or doc_filename
            elif isinstance(files, dict):
                document_url = files.get("url", "")
                doc_filename = files.get("filename") or filename or doc_filename
            elif len(files) > 0:  # It's a list
                document_url = files[0].get("url", "")
                doc_filename = files[0].get("filename") or filename or doc_filename
            else:
                return {"status": "error", "message": "Invalid document files format"}

            message_id = await whatsapp_service.send_document(
                client_id=client_id,
                to=phone_number,
                document=document_url,
                caption=caption or "",
                filename=doc_filename,
            )
            return {"status": "success", "message_id": message_id}
        except Exception as e:
            return {"status": "error", "message": f"Failed to send document: {e!s}"}

    # Otherwise use the DocumentTool for general routing
    context: dict[str, Any] = {
        "company_id": company_id,
        "phone_number": phone_number,
        "lifespan_context": ctx.request_context.lifespan_context,
    }

    # Convert to proper format if needed
    files_list: list[dict[str, str]] = []
    if isinstance(files, str):
        files_list = [{"url": files, "filename": filename or "document.pdf"}]
    elif isinstance(files, dict):
        files_list = [files]
    else:
        files_list = files

    tool = DocumentTool(files_list)
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
    email: dict[str, Any] | None = None,
    sms: dict[str, Any] | None = None,
    pause_number: bool = False,
    track_sale: bool = False,
) -> dict[str, Any]:
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
    context: dict[str, Any] = {
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
) -> dict[str, Any]:
    """Pause execution for specified seconds.

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        seconds: Number of seconds to sleep
    """
    context: dict[str, Any] = {
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
    buttons: list[dict[str, str]],
    button_type: str = "reply",
    header: dict[str, Any] | None = None,
    footer_text: str | None = None,
    payment_data: dict[str, str] | None = None,
    client_id: str | None = None,
) -> dict[str, Any]:
    """Send interactive buttons.

    Args:
        company_id: Company identifier
        phone_number: Recipient's phone number
        body_text: Button message body
        buttons: List of button configs [{"id": "...", "title": "..."} or {"title": "...", "callback_data": "..."}]
        button_type: "reply" or "payment"
        header: Optional header configuration
        footer_text: Optional footer text
        payment_data: Payment data for payment buttons
        client_id: Optional WhatsApp client ID (if None, uses default client for company)
    """
    # If client_id is provided, use WhatsApp service directly
    if client_id:
        whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]
        try:
            # Convert buttons to WhatsApp format if needed
            whatsapp_buttons = []
            for button in buttons:
                if "id" in button and "title" in button:
                    whatsapp_buttons.append(
                        {"title": button["title"], "callback_data": button["id"]}
                    )
                else:
                    whatsapp_buttons.append(button)

            message_id = await whatsapp_service.send_buttons(
                client_id=client_id,
                to=phone_number,
                text=body_text,
                buttons=whatsapp_buttons,
            )
            return {"status": "success", "message_id": message_id}
        except Exception as e:
            return {"status": "error", "message": f"Failed to send buttons: {e!s}"}

    # Otherwise use the ButtonTool for general routing
    context: dict[str, Any] = {
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
async def get_config(_ctx: Context, _company_id: str) -> dict[str, Any]:
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
    _ctx: Context, _company_id: str, _config: dict[str, Any]
) -> dict[str, Any]:
    """Update company configuration.

    Args:
        company_id: Company identifier
        config: New configuration
    """
    # Mock implementation that pretends to update the config
    return {"status": "success", "message": "Configuration updated (mock)"}


# WhatsApp Client Management Tools


@mcp.tool()
async def register_whatsapp_client(
    ctx: Context,
    client_id: str,
    phone_id: str,
    token: str,
) -> dict[str, Any]:
    """Register a new WhatsApp client.

    Args:
        client_id: Unique identifier for the client
        phone_id: WhatsApp phone ID
        token: WhatsApp API token
    """
    whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]

    try:
        # Client response is not needed, we just need the operation to succeed
        _: Any = await whatsapp_service.register_client(
            client_id=client_id, phone_id=phone_id, token=token
        )
        return {
            "status": "success",
            "client_id": client_id,
            "message": "Client registered successfully",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to register client: {e!s}"}


@mcp.tool()
async def list_whatsapp_clients(
    ctx: Context,
) -> dict[str, Any]:
    """List all registered WhatsApp clients.

    Returns:
        Dictionary containing the list of client IDs
    """
    whatsapp_service = ctx.request_context.lifespan_context["whatsapp_service"]

    try:
        clients = await whatsapp_service.list_clients()
        return {"status": "success", "clients": clients}
    except Exception as e:
        return {"status": "error", "message": f"Failed to list clients: {e!s}"}


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
    }

    # When a mock server is provided (for testing), we need to register tools explicitly
    if mcp_instance is not None:
        # Testing support - try to register tools using a "register_tool" method if it exists
        # This is only for test compatibility with mock servers
        register_method = getattr(mcp_instance, "register_tool", None)
        if register_method and callable(register_method):
            for name, func in tool_functions.items():
                register_method(name, func)

    return server


if __name__ == "__main__":
    # Add logging to help debug
    import sys

    print("Starting YaVendió Tools MCP server...", file=sys.stderr)

    # Run the server directly as shown in the MCP documentation
    # No need for async setup here - mcp.run() handles it
    mcp.run()
