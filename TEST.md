# Testing Guide for YaVendió Tools

This document outlines how to run and write tests for the YaVendió Tools project.

## Running Tests

Tests are organized by module and use pytest with pytest-asyncio for async test support:

```bash
# Run all tests
make test

# Run tests with coverage
make coverage

# Run specific test file
make test TEST_PATH=tests/tools/test_text_tool.py

# Run tests with specific marker
make test TEST_ARGS="-m 'not slow'"

# Run only app and tools tests (excluding server tests)
make test TEST_PATH="tests/app tests/tools"

# Run with verbose output
make test TEST_ARGS="-v"
```

## Writing Tests

### Example Tool Test

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

### Testing Best Practices

1. **Use Type Annotations**: Ensure all test functions have proper type annotations
2. **Mock External Dependencies**: Use pytest fixtures to mock external services
3. **Test Error Handling**: Verify that functions handle exceptions properly
4. **Use Descriptive Names**: Test names should clearly describe what is being tested
5. **Isolate Tests**: Each test should be independent and not rely on state from other tests

### Test Structure

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test interactions between components
- **Functional Tests**: Test complete features from user perspective

### Test Fixtures

The project provides several fixtures to simplify testing:

- `test_context`: Provides a mock execution context with all necessary services
- `message_service`: Mock message service for testing message tools
- `whatsapp_service`: Mock WhatsApp service for testing client operations

## Test Coverage

Run test coverage reports to identify areas of the code that need more testing:

```bash
make coverage
```

This will generate an HTML report in the `htmlcov` directory showing line-by-line coverage.
