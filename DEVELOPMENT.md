# Development Guidelines

This document outlines the development standards and best practices for the YaVendió Tools project. Following these guidelines ensures consistency and maintainability across the codebase.

## Development Environment

### Package Management

- **Always use `uv` package manager**, never use `pip` directly
- Dependencies are managed through `pyproject.toml`
- Run `make sync` to update all dependencies
- For adding new dependencies, update `pyproject.toml` and then run `make sync`

```bash
# Install dependencies
make sync

# Development dependencies only
make dev-install
```

### Code Style and Formatting

- Run `make format` to automatically format code
- Format checks are enforced by ruff
- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Import order: standard library imports first, followed by third-party packages, then local imports

```bash
# Format code
make format

# Check formatting
make lint
```

## Type Safety

- Code must pass Pyright type checking in strict mode
- All function parameters and return values must have explicit type annotations
- No implicit Any types allowed
- Use proper collection type annotations (e.g., `list[str]` instead of just `list`)
- TypedDict access must use string literals for keys, not variables
- Always check for None when handling Optional types

### Type Safety Best Practices

1. **Dictionary contexts**: Always use `dict[str, Any]` instead of just `dict` for context parameters
2. **Safe access**: Use `get()` method with default values (e.g., `context.get('phone_number', 'unknown')`)
3. **Type narrowing**: Use explicit type variables to fix argument passing issues:
   ```python
   typed_context: dict[str, Any] = context
   ```
4. **Optional handling**: Check if optional attributes are None before accessing them:
   ```python
   if not self.email:
       return False
   ```
5. **Type verification**: Use `isinstance()` checks to verify types before operations, especially for strings
6. **Type guards**: Add type guards before performing operations on values from dictionaries

## Error Handling

- Exception handlers must always capture the exception variable:
  ```python
  try:
      # code
  except Exception as e:
      # handle error
  ```
- Use specific exception types when possible
- Handle exceptions at the appropriate level
- Log exceptions with appropriate context using structlog

## Testing

- Write tests for all new functionality
- Use pytest for testing
- Mock external dependencies in tests
- Aim for high test coverage for core functionality
- Run tests with `make test`

## Logging and Debugging

- Use structlog for logging, never use `print` statements
- Use rich for console output
- Configure log levels appropriately:
  - DEBUG: Detailed debugging information
  - INFO: Confirmation of normal actions
  - WARNING: Indication of a potential issue
  - ERROR: Error conditions that should be addressed
  - CRITICAL: Critical failures requiring immediate attention

```python
import structlog

logger = structlog.get_logger()
logger.info("Processing request", user_id=user_id, request_time=request_time)
```

## External Services and Integrations

- Infisical SDK is used for secret management (not Redis)
- WhatsApp client uses Infisical to store and retrieve credentials
- No direct use of Redis in new code
- Use pywa for WhatsApp client implementation
- Use pydantic for data validation
- Use MCP for communication between services

## Handling Unused Parameters

When implementing methods with unused parameters (particularly in mock implementations):

1. For methods where parameters are intentionally unused, add them to an underscore variable:
   ```python
   # Parameters intentionally unused in this mock implementation
   _ = param1, param2, param3
   ```

2. Add clear comments explaining that parameters are intentionally unused in mock implementations

## Pull Request Process

1. Ensure all tests pass (`make test`)
2. Run linting checks (`make lint`)
3. Format code (`make format`)
4. Update documentation if necessary
5. Include test coverage for new functionality
6. Address all code review comments

## Code Organization

- Group related functionality in modules
- Keep files focused on a single responsibility
- Use clear, descriptive naming conventions for files, classes, and functions
- Document public APIs with clear docstrings

## Documentation

- Include docstrings for all modules, classes, and functions
- Use type annotations consistently
- Keep README up to date with new features
- Document configuration options
- Update DEVELOPMENT.md with new development standards

By following these guidelines, we maintain a high-quality, type-safe, and maintainable codebase that is easy to extend and collaborate on.
