"""
Tests for SleepTool.
"""

import time
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from tools.sleep_tool import SleepTool


@pytest.mark.asyncio
async def test_sleep_tool_execution(test_context: dict[str, Any]) -> None:
    """Test that SleepTool sleeps for the specified duration."""
    # Arrange
    duration = 1  # 1 second, using int
    sleep_tool = SleepTool(duration)

    # Patch asyncio.sleep to avoid actually sleeping in tests
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        # Act
        start_time = time.time()
        result = await sleep_tool.execute(test_context)
        end_time = time.time()

        # Assert
        mock_sleep.assert_called_once_with(duration)
        assert result is None, "SleepTool should return None"
        # Since we mock asyncio.sleep, execution should be very fast
        assert end_time - start_time < 0.1, (
            "Execution shouldn't take much time with mocked sleep"
        )


@pytest.mark.asyncio
async def test_sleep_tool_zero_duration(test_context: dict[str, Any]) -> None:
    """Test SleepTool with zero duration."""
    # Arrange
    sleep_tool = SleepTool(0)

    # Patch asyncio.sleep to verify it's called even with zero
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        # Act
        await sleep_tool.execute(test_context)

        # Assert
        mock_sleep.assert_called_once_with(0)


@pytest.mark.asyncio
async def test_sleep_tool_negative_duration(test_context: dict[str, Any]) -> None:
    """Test SleepTool with negative duration."""
    # Arrange
    sleep_tool = SleepTool(-1)

    # Patch asyncio.sleep to verify it's not called with negative values
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        # Act
        await sleep_tool.execute(test_context)

        # Assert
        mock_sleep.assert_not_called()


@pytest.mark.asyncio
async def test_sleep_tool_actual_sleep() -> None:
    """Test that SleepTool actually sleeps (integration test)."""
    # This test should be marked as slow as it actually sleeps
    # Arrange
    duration = 1  # 1 second, using int
    sleep_tool = SleepTool(duration)
    test_context = {"foo": "bar"}  # minimal context for this test

    # Act
    start_time = time.time()
    await sleep_tool.execute(test_context)
    end_time = time.time()

    # Assert
    elapsed = end_time - start_time
    assert elapsed >= duration, (
        f"Should sleep at least {duration} seconds (slept {elapsed})"
    )
    # Allow some margin for execution overhead
    assert elapsed < duration + 0.5, (
        f"Sleep shouldn't take much longer than {duration} seconds (took {elapsed})"
    )
