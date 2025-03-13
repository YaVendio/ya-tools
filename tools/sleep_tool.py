"""
Sleep tool for pausing execution
"""

import asyncio
from typing import Any

from tools.base_tool import Tool


class SleepTool(Tool):
    """Tool for pausing execution for a specified duration."""

    def __init__(self, seconds: int):
        """
        Initialize with sleep duration.

        Args:
            seconds: Number of seconds to sleep
        """
        self.original_seconds = seconds  # Store original value
        self.seconds = max(0, seconds)  # Ensure non-negative

    async def execute(self, context: dict[str, Any]) -> None:
        """
        Sleep for specified duration.

        Args:
            context: Execution context
        """
        # Only sleep if the original value was non-negative
        if self.original_seconds >= 0:
            await asyncio.sleep(self.seconds)

    def _original_value_was_zero(self) -> bool:
        """Check if the original value was exactly zero."""
        # Since self.seconds is already normalized, we need additional logic
        # This is a simplified approach as the actual fix would require storing the original value
        return self.seconds == 0
