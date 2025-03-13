"""
Alert tool for sending notifications across channels
"""

import uuid
from typing import Any

from tools.base_tool import MessageTool


class AlertTool(MessageTool):
    """Tool for sending alerts through multiple channels."""

    def __init__(
        self,
        message: str,
        whatsapp: bool = False,
        email: dict[str, str] | None = None,
        sms: dict[str, Any] | None = None,
        pause_number: bool = False,
        track_sale: bool = False,
    ):
        """
        Initialize alert tool with parameters.

        Args:
            message: Alert message
            whatsapp: Whether to send WhatsApp message
            email: Email configuration
            sms: SMS configuration
            pause_number: Whether to pause the conversation
            track_sale: Whether to track this as a sale
        """
        self.message = message
        self.whatsapp = whatsapp
        self.email = email
        self.sms = sms
        self.pause_number = pause_number
        self.track_sale = track_sale

    async def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Send alerts through all configured channels.

        Args:
            context: Execution context

        Returns:
            Results for each channel with status of each alert type
        """
        results: dict[str, bool | str] = {}

        # Create properly typed context for all helper methods
        typed_context: dict[str, Any] = context
        
        # Format message with replacements
        self.message = self._format_message(typed_context)
        
        # Track sale if configured
        if self.track_sale:
            results["sale_tracked"] = await self._track_sale(typed_context)

        # Send WhatsApp message if configured
        if self.whatsapp:
            results["whatsapp"] = await self._send_whatsapp_alert(typed_context)

        # Send email if configured
        if self.email:
            results["email"] = await self._send_email_alert(typed_context)

        # Send SMS if configured
        if self.sms:
            results["sms"] = await self._send_sms_alert(typed_context)

        # Pause number if configured
        if self.pause_number:
            results["paused"] = await self._pause_number(typed_context)

        return results

    def _format_message(self, context: dict[str, Any]) -> str:
        """
        Format message with replacements.

        Args:
            context: Execution context with values for replacement

        Returns:
            Formatted message
        """
        try:
            replacements = {
                "{phone_number}": context["phone_number"],
                "{summary_response}": self._get_conversation_summary(context),
            }

            formatted_message = self.message
            for key, value in replacements.items():
                if key in formatted_message:
                    formatted_message = formatted_message.replace(key, value)

            return formatted_message
        except Exception:
            return self.message

    def _get_conversation_summary(self, context: dict[str, Any]) -> str:
        """
        Get a summary of the conversation.

        Args:
            context: Execution context with phone number and conversation data

        Returns:
            Conversation summary
        """
        # Implementation would depend on external logic
        phone_number = context.get('phone_number', 'unknown')
        return f"Conversation with {phone_number}"

    async def _track_sale(self, context: dict[str, Any]) -> bool:
        """
        Track a sale conversion.

        Args:
            context: Execution context with user data

        Returns:
            Success status
        """
        # Parameter intentionally unused in this mock implementation
        _ = context
        # Mock implementation - no actual tracking
        return True

    async def _send_whatsapp_alert(self, context: dict[str, Any]) -> str:
        """
        Send WhatsApp alert.

        Args:
            context: Execution context with phone number and other data

        Returns:
            Message ID
        """
        message_service = context["lifespan_context"]["message_service"]

        # In a real implementation, this would call an external service
        external_id = str(uuid.uuid4())

        # Create outbound message
        outbound_message = self.get_outbound_message(
            external_id, context, self.message, "text", "alert"
        )

        # Store the message
        await message_service.insert_message(outbound_message)

        return external_id

    async def _send_email_alert(self, context: dict[str, Any]) -> bool:
        """
        Send email alert.

        Args:
            context: Execution context

        Returns:
            Success status
        """
        # Mock implementation - no actual email sending
        if not self.email:
            return False
            
        subject = self.email.get("subject", "Alert")
        # No need for isinstance check as subject is a str from the get call
        if "{phone_number}" in subject:
            phone_number = context.get("phone_number", "")
            if isinstance(phone_number, str):
                subject = subject.replace("{phone_number}", phone_number)

        return True

    async def _send_sms_alert(self, context: dict[str, Any]) -> bool:
        """
        Send SMS alert.

        Args:
            context: Execution context containing phone number and other data

        Returns:
            Success status
        """
        # Parameter intentionally unused in this mock implementation
        _ = context
        # Mock implementation - no actual SMS sending
        return True

    async def _pause_number(self, context: dict[str, Any]) -> bool:
        """
        Pause conversation for a number.

        Args:
            context: Execution context with phone number data

        Returns:
            Success status
        """
        # Mock implementation - no actual pausing
        return True

    def _get_push_notification_message(self, context: dict[str, Any]) -> str:
        """
        Get formatted push notification message.

        Args:
            context: Execution context with phone number and company data

        Returns:
            Notification message
        """
        company_name = "Company"  # In real impl, get from metadata

        messages = {
            "venta": f"'{company_name}': 🤑 Ya! vendiste! Venta confirmada de '{context['phone_number']}'",
            "derivación": f"'{company_name}': '{context['phone_number']}' necesita tu ayuda 🆘",
        }

        # Get SMS type with explicit type handling
        sms_type_value: Any = self.sms.get("type") if self.sms else None
        
        # Ensure we have a valid string key
        sms_type: str = "derivación"  # Default
        if isinstance(sms_type_value, str):
            sms_type = sms_type_value
            
        return messages.get(sms_type, messages["derivación"])
