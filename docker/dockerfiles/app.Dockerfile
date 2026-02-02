# Build arguments
ARG PYTHON_VERSION=3.12-slim

# Base image
FROM python:${PYTHON_VERSION}

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore \
    DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        supervisor \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

# Supervisor directories & permissions
RUN mkdir -p \
        /var/log/supervisord \
        /var/run/supervisord \
    && chown -R appuser:appuser \
        /var/log/supervisord \
        /var/run/supervisord

# Supervisor configuration
COPY docker/config/supervisor/supervisord.conf \
     /etc/supervisor/conf.d/supervisord.conf

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /var/www/app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Change ownership of .venv to appuser
RUN chown -R appuser:appuser /var/www/app/.venv

# Copy project files (with ownership)
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port (FastAPI)
EXPOSE 8000

# Start supervisor
CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
