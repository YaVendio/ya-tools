"""
Button tool for sending interactive buttons
"""

import uuid
from typing import Any

from tools.base_tool import MessageTool


class ButtonTool(MessageTool):
    """Tool for sending interactive buttons."""

    def __init__(
        self,
        body_text: str,
        buttons: list[dict[str, Any]],
        button_type: str = "reply",
        header: dict[str, Any] | None = None,
        footer_text: str | None = None,
        payment_data: dict[str, Any] | None = None,
    ):
        """
        Initialize button tool with parameters.

        Args:
            body_text: Button message body
            buttons: List of button configurations
            button_type: Type of buttons ("reply" or "payment")
            header: Optional header configuration
            footer_text: Optional footer text
            payment_data: Payment data for payment buttons
        """
        self.body_text = body_text
        self.buttons = (
            buttons[:3] if button_type == "reply" else buttons
        )  # Max 3 buttons for reply type
        self.button_type = button_type
        self.header = header
        self.footer_text = footer_text
        self.payment_data = payment_data

    async def execute(self, context: dict[str, Any]) -> str:
        """
        Send button message.

        Args:
            context: Execution context

        Returns:
            Message ID
        """
        message_service = context["lifespan_context"]["message_service"]

        # In real implementation, this would call an external service
        if self.button_type == "payment":
            external_id = await self._send_link_payment(
                context["phone_number"], context["company_id"]
            )

            # Format message body for display
            body_text = self.body_text if self.body_text else ""
            footer_text = self.footer_text if self.footer_text else ""
            title = self.payment_data["title"] if self.payment_data else ""
            url = self.payment_data["url"] if self.payment_data else ""
            message_text = f"{body_text}\n{footer_text}\n{title}\n{url}"
        else:
            external_id = await self._send_reply_button(
                context["phone_number"], context["company_id"]
            )

            # Format message body for display
            body_text = self.body_text if self.body_text else ""
            footer_text = self.footer_text if self.footer_text else ""
            button_text = self._get_button_text()
            message_text = f"{body_text}\n{footer_text}\nOptions: {button_text}"

        # Create outbound message with interactive data
        button_data: dict[str, Any] = {
            "text": message_text,
            "button_type": self.button_type,
            "buttons": self.buttons,
        }

        # Add header if provided
        if self.header:
            button_data["header"] = self.header

        # Add footer if provided
        if self.footer_text:
            button_data["footer"] = {"text": self.footer_text}

        # Add payment data if provided
        if self.payment_data and self.button_type == "payment":
            button_data["payment"] = self.payment_data

        outbound_message = self.get_outbound_message(
            external_id, context, button_data, "interactive", "assistant"
        )

        # Store the message
        await message_service.insert_message(outbound_message)

        return external_id

    async def _send_reply_button(self, phone_number: str, company_id: str) -> str:
        """
        Placeholder for sending reply buttons.

        Args:
            phone_number: Recipient's phone number
            company_id: Company identifier

        Returns:
            External message ID
        """
        # Format buttons if needed
        self._format_reply_buttons()

        # Actual button sending would go here
        return str(uuid.uuid4())

    async def _send_link_payment(self, phone_number: str, company_id: str) -> str:
        """
        Placeholder for sending payment link.

        Args:
            phone_number: Recipient's phone number
            company_id: Company identifier

        Returns:
            External message ID
        """
        # Parameters intentionally unused in this mock implementation
        _ = phone_number, company_id
        # Actual payment link sending would go here
        return str(uuid.uuid4())

    def _format_reply_buttons(self) -> None:
        """
        Format buttons to WhatsApp API structure.

        Transforms simple button objects into the format expected
        by the WhatsApp API.
        """
        self.buttons = [
            {
                "type": "reply",
                "reply": {
                    "id": button.get("id", str(i)),
                    "title": button.get("title", ""),
                },
            }
            for i, button in enumerate(self.buttons)
        ]

    def _get_button_text(self) -> str:
        """
        Get text representation of buttons.

        Returns:
            Comma-separated list of button titles
        """
        try:
            if self.button_type == "reply":
                # Extract titles as strings with proper type handling
                button_titles: list[str] = []
                for button in self.buttons:
                    # Use type narrowing instead of isinstance
                    # First case: direct title in dict
                    if hasattr(button, "get"):
                        # Safely handle the title retrieval
                        title = button.get("title", None)
                        if isinstance(title, str):
                            button_titles.append(title)
                        # Handle reply button case - get returns Any, so we need to check the type
                        reply_value = button.get("reply", None)  # This could be any type
                        
                        # Type guard to ensure it's a dictionary before proceeding
                        if isinstance(reply_value, dict):
                            # Now that we know it's a dict, create a typed dictionary
                            # Use a type guard pattern with assignment
                            typed_reply_dict: dict[str, Any] = reply_value
                            
                            # Get title with explicit None default to avoid Any type
                            title_value: Any = typed_reply_dict.get("title")
                            
                            # Only add to the list if the title is a string
                            if isinstance(title_value, str):
                                button_titles.append(title_value)
                
                return ", ".join(button_titles)
            return ""
        except Exception:
            return ""
