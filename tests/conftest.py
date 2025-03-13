"""
Common test fixtures for the entire project.
"""

from typing import Any

import pytest

from services.message_service_mock import MockMessageService


@pytest.fixture
def mock_services() -> dict[str, Any]:
    """Fixture providing mock services for tests."""
    return {
        "message_service": MockMessageService(),
    }


@pytest.fixture
def test_context(mock_services: dict[str, Any]) -> dict[str, Any]:
    """Fixture providing test context with mock services."""
    return {
        "lifespan_context": mock_services,
        "phone_number": "1234567890",
        "company_id": "test-company",
    }
