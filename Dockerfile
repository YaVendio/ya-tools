FROM python:3.13-slim

WORKDIR /app

# Install system dependencies including Node.js
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy only the necessary files for installation
COPY pyproject.toml README.md ./
COPY app ./app
COPY services ./services
COPY tools ./tools

# Install the package and MCP with CLI
RUN pip install -e .
RUN pip install "mcp[cli]"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Default command uses MCP to run the server
CMD ["mcp", "run", "app/server.py"]