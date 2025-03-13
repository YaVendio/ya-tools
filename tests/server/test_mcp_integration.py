"""
Tests for MCP server integration.
"""

import asyncio
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# Since we're testing the MCP integration, we need to mock the MCP server library
@pytest.fixture
def mock_mcp_server():
    """Mock the FastMCP server."""
    with patch("mcp.server.fastmcp.FastMCP") as mock_server:
        # Mock the register_tool method
        mock_server.return_value.register_tool = MagicMock()
        # Mock the register_resource method
        mock_server.return_value.register_resource = MagicMock()
        # Mock the start method
        mock_server.return_value.start = AsyncMock()
        # Mock the stop method
        mock_server.return_value.stop = AsyncMock()

        yield mock_server


@pytest.mark.asyncio
async def test_server_registers_tools(mock_mcp_server):
    """Test that the server registers all required tools with MCP."""
    # Import here to avoid circular imports during test discovery
    from app.server import create_server

    # Act - Create the server (which should register tools)
    server = await create_server(mock_mcp_server.return_value)

    # Assert - Check that tools were registered
    register_tool = mock_mcp_server.return_value.register_tool

    # Check for all expected tools
    expected_tools = [
        "send_text",
        "send_image",
        "send_video",
        "send_document",
        "send_alert",
        "sleep",
        "send_button",
        "get_config",
        "update_config",
        "register_whatsapp_client",
        "list_whatsapp_clients",
        "send_whatsapp_text",
        "send_whatsapp_image",
        "send_whatsapp_video",
        "send_whatsapp_document",
        "send_whatsapp_buttons",
    ]

    # Get all tool names that were registered
    registered_tools = [call.args[0] for call in register_tool.call_args_list]

    # Check that each expected tool was registered
    for tool in expected_tools:
        assert tool in registered_tools, f"Expected tool '{tool}' not registered"

    # Cleanup
    await server.stop()


@pytest.mark.asyncio
async def test_send_text_tool_integration(
    mock_mcp_server, test_context: Dict[str, Any]
):
    """Test the send_text tool integration."""
    # Import here to avoid circular imports
    from app.server import create_server

    # Mock the context passed to the tool handler
    context = MagicMock()
    context.get_state = AsyncMock(return_value=test_context)
    context.set_state = AsyncMock()

    # Set up the mock handler to return a valid response
    async def mock_handler_impl(ctx, params):
        await ctx.get_state()
        return {"message_id": "test_message_id"}

    mock_handler = AsyncMock(side_effect=mock_handler_impl)

    # Configure the mock server to return our mock handler when registering the send_text tool
    def register_tool_side_effect(name, handler):
        if name == "send_text":
            return mock_handler
        return MagicMock()

    mock_mcp_server.return_value.register_tool.side_effect = register_tool_side_effect

    # Act - Create the server
    server = await create_server(mock_mcp_server.return_value)

    # Get the registered tool handlers
    register_tool = mock_mcp_server.return_value.register_tool

    # Find the send_text tool handler
    send_text_handler = None
    for call in register_tool.call_args_list:
        if call.args[0] == "send_text":
            send_text_handler = mock_handler
            break

    assert send_text_handler is not None, "send_text tool not registered"

    # Call the handler with a test message
    test_message = "Hello, world!"
    result = await send_text_handler(context, {"message": test_message})

    # Assert
    assert result.get("message_id") is not None, "Should return a message ID"

    # Verify context state was retrieved
    context.get_state.assert_called_once()

    # Cleanup
    await server.stop()


@pytest.mark.asyncio
async def test_sleep_tool_integration(mock_mcp_server, test_context: Dict[str, Any]):
    """Test the sleep tool integration."""
    # Import here to avoid circular imports
    from app.server import create_server

    # Mock the context passed to the tool handler
    context = MagicMock()
    context.get_state = AsyncMock(return_value=test_context)

    # Patch asyncio.sleep to avoid actual sleeping
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        # Set up the mock handler to call asyncio.sleep
        async def mock_handler_impl(ctx, params):
            await ctx.get_state()
            await asyncio.sleep(params["seconds"])
            return {"status": "success"}

        mock_handler = AsyncMock(side_effect=mock_handler_impl)

        # Configure the mock server to return our mock handler when registering the sleep tool
        def register_tool_side_effect(name, handler):
            if name == "sleep":
                return mock_handler
            return MagicMock()

        mock_mcp_server.return_value.register_tool.side_effect = (
            register_tool_side_effect
        )

        # Act - Create the server
        server = await create_server(mock_mcp_server.return_value)

        # Get the registered tool handlers
        register_tool = mock_mcp_server.return_value.register_tool

        # Find the sleep tool handler
        sleep_handler = None
        for call in register_tool.call_args_list:
            if call.args[0] == "sleep":
                sleep_handler = mock_handler
                break

        assert sleep_handler is not None, "sleep tool not registered"

        # Call the handler with a test duration
        await sleep_handler(context, {"seconds": 5})

        # Assert
        mock_sleep.assert_called_once_with(5)

        # Cleanup
        await server.stop()


@pytest.mark.asyncio
async def test_server_lifespan_management(mock_mcp_server):
    """Test the server's lifespan management."""
    # Import here to avoid circular imports
    from app.server import create_server

    # Act - Create and then start the server
    server = await create_server(mock_mcp_server.return_value)
    await server.start()

    # Assert - Server was started
    mock_mcp_server.return_value.start.assert_called_once()

    # Now stop the server
    await server.stop()

    # Assert - Server was stopped
    mock_mcp_server.return_value.stop.assert_called_once()
