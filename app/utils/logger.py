from __future__ import annotations

import sys
import socket
from loguru import logger, Logger


def get_host_ip() -> str:
    """Get the IP address of the host."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        return "unknown"


# Remove default Loguru handler
logger.remove()

# Bind IP to logger context
logger = logger.bind(ip=get_host_ip())

# Remove background from CRITICAL logs
logger.level("CRITICAL", color="<red>")

# Console handler (colorized)
logger.add(
    sys.stdout,
    level="DEBUG",
    colorize=True,
    diagnose=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>",
)

# File handler (no color, with rotation & retention)
logger.add(
    "logs/app.log",
    level="DEBUG",
    rotation="10 MB",  # Rotate after 10MB
    retention="10 days",  # Keep for 10 days
    compression="zip",  # Compress old logs
    encoding="utf-8",
    backtrace=True,
    diagnose=True,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
)


def get_logger() -> Logger:
    """Return the Loguru logger instance."""
    return logger
