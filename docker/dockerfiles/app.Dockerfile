# Use build argument to set Python version, default is 3.12-slim
ARG PYTHON_VERSION=3.12-slim

# Base image with configurable Python version
FROM python:${PYTHON_VERSION}

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore

# Update package lists and install supervisor and nginx without recommended packages to keep the image slim
RUN apt-get update && apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    supervisor \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && rm /etc/nginx/sites-enabled/default

# Copy nginx configuration file to the appropriate directory
COPY docker/config/nginx/app.conf /etc/nginx/sites-enabled/app.conf

# Copy supervisor configuration file to the appropriate directory
COPY docker/config/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create necessary directories for supervisor logs and runtime files
RUN mkdir -p /var/log/supervisord /var/run/supervisord

# Set the working directory for subsequent commands
WORKDIR /var/www/app

# Install uv for faster dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files and README (required by hatchling build)
COPY pyproject.toml uv.lock  ./


# Install dependencies (remove any existing venv first)
RUN rm -rf .venv && uv sync --frozen


# Copy the entire application code to the working directory
COPY ./app ./app

# Expose port 8000 for the application
EXPOSE 8000

# Command to start supervisor with the specified configuration file, running in the foreground
CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]