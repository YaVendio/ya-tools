# YaVendió Tools

An MCP-based messaging and notifications system that allows AI systems to interact with various messaging platforms through the Model Context Protocol (MCP). This project implements an MCP server that exposes messaging tools for sending text, images, documents, buttons, and alerts.

## Features

- **Messaging Capabilities**:
  - Send text messages via WhatsApp and other platforms
  - Send images and media with proper formatting
  - Send videos with appropriate metadata
  - Send documents with filenames and metadata
  - Create interactive buttons for user engagement
  
- **WhatsApp Client Management**:
  - Register and manage multiple WhatsApp clients with different credentials
  - Store tokens securely using Redis
  - Stateless architecture for client management
  - Dedicated tools for each WhatsApp operation
  
- **Notification Features**:
  - Configure alerts across multiple channels (WhatsApp, Email, SMS)
  - Support for payment buttons and transaction notifications
  
- **Conversation Management**:
  - Track message delivery status and metadata
  
- **Additional Utilities**:
  - Sleep/delay functionality for timed interactions
  - Configuration management for companies and users
  - Real-time message delivery with status tracking

## What is MCP?

The Model Context Protocol (MCP) is an open standard developed by Anthropic that enables seamless integration between AI systems and external data sources or tools. It provides a universal, open standard for connecting AI systems with data sources, replacing fragmented integrations with a single protocol.

This project implements an MCP server that exposes various messaging tools, making them accessible to AI systems in a standardized way. By using MCP, AI assistants can:

- Send WhatsApp messages directly to users
- Upload and send media files
- Create interactive experiences with buttons
- Manage conversation context efficiently
- Trigger multi-channel notifications

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for package management:

```bash
# Install uv if you don't have it
curl -L https://github.com/astral-sh/uv/releases/latest/download/install.sh | sh

# Alternatively, install with pip
pip install uv

# Clone the repository
git clone https://your-repo-url/yatools.git
cd yatools

# Install all dependencies (including dev dependencies)
make sync
# Or individually
make install      # Regular dependencies
make dev-install  # Development dependencies
```

### Requirements

- Python 3.13 or higher
- Docker and Docker Compose (for containerized deployment)

## Configuration

Create a `.env` file in the root directory with your configuration:

```
# Logging configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## Running with Docker

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f app
```

## Running Locally

```bash
# Development mode with auto-reload
make run

# Production mode
make run-prod

# Run with specific port
PORT=8080 make run
```

## Development

The project includes several Makefile commands to streamline development:

```bash
# Show all available commands
make help

# Run tests
make test

# Run tests with coverage report
make coverage

# Format code
make format

# Lint code
make lint

# Clean cache files
make clean
```

## Project Structure

- `app/`: Main application code
  - `server.py`: The MCP server implementation
  - `logging.py`: Logging configuration with structlog
  - `lifespan.py`: Application lifecycle management

- `tools/`: Tool implementations
  - `base_tool.py`: Abstract base classes for all tools
  - `text_tool.py`: Tool for sending text messages
  - `image_tool.py`: Tool for sending images
  - `video_tool.py`: Tool for sending videos
  - `document_tool.py`: Tool for sending documents
  - `button_tool.py`: Tool for sending interactive buttons
  - `alert_tool.py`: Tool for sending multi-channel alerts
  - `sleep_tool.py`: Tool for adding delays in tool execution

- `services/`: Service implementations
  - `interfaces.py`: Service interfaces defining contracts
  - `message_service.py`: Service for message storage and retrieval
  - `message_service_mock.py`: Mock implementation for testing
  - `whatsapp_service.py`: Service for WhatsApp client management
  - `whatsapp_service_mock.py`: Mock WhatsApp service for testing

- `tests/`: Test implementations
  - `app/`: Tests for application structure
  - `tools/`: Tests for individual tools
  - `services/`: Tests for services
  - `server/`: Tests for MCP server integration

## MCP Integration

This service can be integrated with LLM applications through the Model Context Protocol:

```bash
# Install the server in Claude Desktop
mcp install app/server.py

# Run in development mode with auto-reload
mcp dev app/server.py

# Install from PyPI (if published)
mcp install ya-tools
```

### Available MCP Tools

#### `send_text`

Sends a text message to a WhatsApp number.

**Parameters:**

- `company_id`: Company identifier
- `phone_number`: Recipient's phone number
- `message`: Text to send

**Example:**

```python
result = await send_text(
    company_id="company123",
    phone_number="5551234567",
    message="Hello, this is a test message!"
)
print(f"Message ID: {result['message_id']}")
```

#### `send_image`

Sends one or more images to a WhatsApp number.

**Parameters:**

- `company_id`: Company identifier
- `phone_number`: Recipient's phone number
- `image_urls`: List of image URLs to send

**Example:**

```python
result = await send_image(
    company_id="company123",
    phone_number="5551234567",
    image_urls=["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
)
print(f"Message IDs: {result['message_ids']}")
```

#### `send_video`

Sends one or more videos to a WhatsApp number.

**Parameters:**

- `company_id`: Company identifier
- `phone_number`: Recipient's phone number
- `video_urls`: List of video URLs to send

**Example:**

```python
result = await send_video(
    company_id="company123",
    phone_number="5551234567",
    video_urls=["https://example.com/video.mp4"]
)
print(f"Message IDs: {result['message_ids']}")
```

#### `send_document`

Sends document files to a WhatsApp number.

**Parameters:**

- `company_id`: Company identifier
- `phone_number`: Recipient's phone number
- `files`: List of document files as `{"url": "...", "filename": "..."}`

**Example:**

```python
result = await send_document(
    company_id="company123",
    phone_number="5551234567",
    files=[
        {
            "url": "https://example.com/document.pdf",
            "filename": "report.pdf"
        }
    ]
)
print(f"Message IDs: {result['message_ids']}")
```

#### `send_alert`

Sends alerts through multiple channels (WhatsApp, Email, SMS).

**Parameters:**

- `company_id`: Company identifier
- `phone_number`: Recipient's phone number
- `message`: Alert message
- `whatsapp`: Whether to send WhatsApp message
- `email`: Email configuration `{"subject": "..."}`
- `sms`: SMS configuration `{"type": "...", "recipients": ["..."]}`
- `pause_number`: Whether to pause the conversation
- `track_sale`: Whether to track this as a sale

**Example:**

```python
result = await send_alert(
    company_id="company123",
    phone_number="5551234567",
    message="Important alert: New activity detected",
    whatsapp=True,
    email={
        "subject": "Important Alert", 
        "recipients": ["user@example.com"]
    },
    sms={
        "type": "urgent", 
        "recipients": ["5551234567", "5557654321"]
    },
    pause_number=False,
    track_sale=True
)
print(f"Alert Result: {result['result']}")
```

#### `sleep`

Pauses execution for specified seconds.

**Parameters:**

- `company_id`: Company identifier
- `phone_number`: Recipient's phone number
- `seconds`: Number of seconds to sleep

**Example:**

```python
result = await sleep(
    company_id="company123",
    phone_number="5551234567",
    seconds=5
)
print(f"Slept for {result['seconds']} seconds")
```

#### `send_button`

Sends interactive buttons.

**Parameters:**

- `company_id`: Company identifier
- `phone_number`: Recipient's phone number
- `body_text`: Button message body
- `buttons`: List of button configs `[{"id": "...", "title": "..."}]`
- `button_type`: "reply" or "payment"
- `header`: Optional header configuration
- `footer_text`: Optional footer text
- `payment_data`: Payment data for payment buttons

**Example (Reply Buttons):**

```python
result = await send_button(
    company_id="company123",
    phone_number="5551234567",
    body_text="Please select an option:",
    buttons=[
        {"id": "btn1", "title": "Option 1"},
        {"id": "btn2", "title": "Option 2"},
        {"id": "btn3", "title": "Option 3"}
    ],
    button_type="reply",
    footer_text="Tap a button to proceed"
)
print(f"Button Message ID: {result['message_id']}")
```

**Example (Payment Button):**

```python
result = await send_button(
    company_id="company123",
    phone_number="5551234567",
    body_text="Complete your purchase:",
    buttons=[{"id": "pay1", "title": "Pay Now"}],
    button_type="payment",
    payment_data={
        "title": "Premium Subscription",
        "url": "https://pay.example.com/invoice123",
        "amount": "19.99",
        "currency": "USD"
    }
)
print(f"Payment Button Message ID: {result['message_id']}")
```

#### `get_config`

Gets company configuration.

**Parameters:**

- `company_id`: Company identifier

**Example:**

```python
config = await get_config(
    company_id="company123"
)
print(f"Company Config: {config['config']}")
```

#### `update_config`

Updates company configuration.

**Parameters:**

- `company_id`: Company identifier
- `config`: New configuration

**Example:**

```python
result = await update_config(
    company_id="company123",
    config={
        "welcome_message": "Welcome to our service!",
        "auto_reply": True,
        "notification_emails": ["admin@example.com"]
    }
)
print(f"Update Result: {result['message']}")
```

### WhatsApp Client Management Tools

These tools allow you to manage multiple WhatsApp clients with different credentials.

#### `register_whatsapp_client`

Registers a new WhatsApp client with the specified credentials.

**Parameters:**

- `client_id`: Unique identifier for the client
- `phone_id`: WhatsApp phone ID
- `token`: WhatsApp API token

**Example:**

```python
result = await register_whatsapp_client(
    client_id="client123",
    phone_id="1234567890",
    token="your_whatsapp_token"
)
print(f"Client registered: {result['client_id']}")
```

#### `list_whatsapp_clients`

Lists all registered WhatsApp clients.

**Example:**

```python
result = await list_whatsapp_clients()
print(f"Registered clients: {result['clients']}")
```

#### `send_whatsapp_text`

Sends a text message through a specific WhatsApp client.

**Parameters:**

- `client_id`: Client to use for sending
- `phone_number`: Recipient's phone number
- `message`: Text message to send

**Example:**

```python
result = await send_whatsapp_text(
    client_id="client123",
    phone_number="5551234567",
    message="Hello from WhatsApp!"
)
print(f"Message ID: {result['message_id']}")
```

#### `send_whatsapp_image`

Sends an image through a specific WhatsApp client.

**Parameters:**

- `client_id`: Client to use for sending
- `phone_number`: Recipient's phone number
- `image_url`: URL of the image to send
- `caption`: Optional caption for the image

**Example:**

```python
result = await send_whatsapp_image(
    client_id="client123",
    phone_number="5551234567",
    image_url="https://example.com/image.jpg",
    caption="Check out this image!"
)
print(f"Message ID: {result['message_id']}")
```

#### `send_whatsapp_video`

Sends a video through a specific WhatsApp client.

**Parameters:**

- `client_id`: Client to use for sending
- `phone_number`: Recipient's phone number
- `video_url`: URL of the video to send
- `caption`: Optional caption for the video

**Example:**

```python
result = await send_whatsapp_video(
    client_id="client123",
    phone_number="5551234567",
    video_url="https://example.com/video.mp4",
    caption="Check out this video!"
)
print(f"Message ID: {result['message_id']}")
```

#### `send_whatsapp_document`

Sends a document through a specific WhatsApp client.

**Parameters:**

- `client_id`: Client to use for sending
- `phone_number`: Recipient's phone number
- `document_url`: URL of the document to send
- `caption`: Optional caption for the document
- `filename`: Optional filename for the document

**Example:**

```python
result = await send_whatsapp_document(
    client_id="client123",
    phone_number="5551234567",
    document_url="https://example.com/document.pdf",
    caption="Important document",
    filename="report.pdf"
)
print(f"Message ID: {result['message_id']}")
```

#### `send_whatsapp_buttons`

Sends interactive buttons through a specific WhatsApp client.

**Parameters:**

- `client_id`: Client to use for sending
- `phone_number`: Recipient's phone number
- `text`: Message text to display
- `buttons`: List of button configs `[{"title": "...", "callback_data": "..."}]`

**Example:**

```python
result = await send_whatsapp_buttons(
    client_id="client123",
    phone_number="5551234567",
    text="Please select an option:",
    buttons=[
        {"title": "Option 1", "callback_data": "opt1"},
        {"title": "Option 2", "callback_data": "opt2"}
    ]
)
print(f"Message ID: {result['message_id']}")
```

## Testing

Tests are organized by module and use pytest with pytest-asyncio for async test support:

```bash
# Run all tests
make test

# Run tests with coverage
make coverage

# Run specific test file
python -m pytest tests/tools/test_text_tool.py

# Run tests with specific marker
python -m pytest -m "not slow"

# Run only app and tools tests (excluding server tests)
python -m pytest tests/app tests/tools

# Run with verbose output
python -m pytest -v
```

### Writing Tests

Here's an example of how to write a test for a tool:

```python
import pytest
from tools.text_tool import TextTool

@pytest.mark.asyncio
async def test_text_tool_execution(test_context):
    """Test the TextTool with mock services."""
    # Create and execute text tool
    text_tool = TextTool("Hello, this is a test message!")
    message_id = await text_tool.execute(test_context)

    # Get services from context
    message_service = test_context["lifespan_context"]["message_service"]

    # Assertions
    assert message_id is not None, "Message ID should be returned"
    assert len(message_service.messages) > 0, "Message should be stored"
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure they pass (`make test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
