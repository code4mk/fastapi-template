from __future__ import annotations

import sys
import socket
from loguru import logger
from loguru._logger import Logger as LoguruLogger


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


def get_logger() -> LoguruLogger:
    """Return the Loguru logger instance."""
    return logger
