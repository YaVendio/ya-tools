"""
Tests for the application structure.
"""

import importlib.util
from pathlib import Path


def test_app_structure():
    """Test that the basic app structure exists."""
    # Root directories
    root_dir = Path(__file__).parents[2]
    app_dir = root_dir / "app"
    services_dir = root_dir / "services"
    tools_dir = root_dir / "tools"

    # Assert directories exist
    assert app_dir.exists(), "app directory should exist"
    assert services_dir.exists(), "services directory should exist"
    assert tools_dir.exists(), "tools directory should exist"

    # Check for key files
    assert (app_dir / "server.py").exists(), "server.py should exist"
    assert (app_dir / "logging.py").exists(), "logging.py should exist"
    assert (tools_dir / "base_tool.py").exists(), "base_tool.py should exist"
    assert (services_dir / "interfaces.py").exists(), "interfaces.py should exist"


def test_tools_implementation():
    """Test that all required tools are implemented."""
    # Root directory
    root_dir = Path(__file__).parents[2]
    tools_dir = root_dir / "tools"

    # Required tools
    required_tools = [
        "text_tool.py",
        "image_tool.py",
        "video_tool.py",
        "document_tool.py",
        "alert_tool.py",
        "button_tool.py",
        "sleep_tool.py",
    ]

    # Check each required tool exists
    for tool in required_tools:
        assert (tools_dir / tool).exists(), f"{tool} should exist"


def test_services_implementation():
    """Test that all required services are implemented."""
    # Root directory
    root_dir = Path(__file__).parents[2]
    services_dir = root_dir / "services"

    # Required services
    required_services = [
        "message_service.py",
    ]

    # Check each required service exists
    for service in required_services:
        assert (services_dir / service).exists(), f"{service} should exist"


def test_test_coverage():
    """Test that there are tests for all major components."""
    # Root directory
    root_dir = Path(__file__).parents[2]
    tests_dir = root_dir / "tests"

    # Required test directories
    required_test_dirs = [
        "tools",
        "services",
        "app",
    ]

    # Check each required test directory exists
    for test_dir in required_test_dirs:
        assert (tests_dir / test_dir).exists(), (
            f"{test_dir} test directory should exist"
        )


def test_imports_valid():
    """Test that key modules can be imported."""
    # This is a simple check that validates imports without executing any code
    # It catches syntax errors and missing dependencies
    root_dir = Path(__file__).parents[2]

    # Test importing interfaces to check service contracts
    interfaces_path = root_dir / "services" / "interfaces.py"
    assert interfaces_path.exists(), "interfaces.py should exist"

    spec = importlib.util.spec_from_file_location("interfaces", interfaces_path)
    assert spec is not None, "Could not create module spec for interfaces.py"

    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None, "Module loader should not be None"
    spec.loader.exec_module(module)

    # Test importing base_tool to check tool contracts
    base_tool_path = root_dir / "tools" / "base_tool.py"
    assert base_tool_path.exists(), "base_tool.py should exist"

    spec = importlib.util.spec_from_file_location("base_tool", base_tool_path)
    assert spec is not None, "Could not create module spec for base_tool.py"

    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None, "Module loader should not be None"
    spec.loader.exec_module(module)

    # Success if no exceptions were raised
