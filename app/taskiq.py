import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from taskiq import AsyncBroker

from app.utils.tskq.taskiq_broker import create_broker
from dotenv import load_dotenv
from app.utils.tskq.taskiq_helper import discover_and_import_tasks
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

load_dotenv()


def create_taskiq_broker() -> AsyncBroker:
    """Create and configure the Taskiq broker."""
    broker_type = os.getenv("TASKIQ_BROKER_TYPE", "redis-stream")
    backend_type = os.getenv("TASKIQ_BACKEND_TYPE", "redis")
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Optional cluster/sentinel configuration
    cluster_hosts = None
    if cluster_hosts_env := os.getenv("REDIS_CLUSTER_HOSTS"):
        cluster_hosts = cluster_hosts_env.split(",")

    sentinel_hosts = None
    if sentinel_hosts_env := os.getenv("REDIS_SENTINEL_HOSTS"):
        sentinel_hosts = sentinel_hosts_env.split(",")

    sentinel_service = os.getenv("REDIS_SENTINEL_SERVICE")

    return create_broker(
        broker_type=broker_type,
        backend_type=backend_type,
        url=redis_url,
        cluster_hosts=cluster_hosts,
        sentinel_hosts=sentinel_hosts,
        sentinel_service=sentinel_service,
    )


# Create the global broker instance
taskiq_broker = create_taskiq_broker()


@asynccontextmanager
async def taskiq_lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage Taskiq broker lifecycle."""
    # Startup
    await taskiq_broker.startup()

    yield

    # Shutdown
    await taskiq_broker.shutdown()


def setup_taskiq(app: FastAPI) -> None:
    """Set up Taskiq integration with FastAPI application."""
    # Add the lifespan context manager to the app
    if not hasattr(app, "router") or not app.router.lifespan_context:
        app.router.lifespan_context = taskiq_lifespan
    else:
        # If there's already a lifespan, we need to combine them
        existing_lifespan = app.router.lifespan_context

        @asynccontextmanager
        async def combined_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
            async with existing_lifespan(app), taskiq_lifespan(app):
                yield

        app.router.lifespan_context = combined_lifespan


def get_taskiq_broker() -> AsyncBroker:
    """Get the configured Taskiq broker instance."""
    return taskiq_broker


discover_and_import_tasks()


# Create scheduler with label schedule source
taskiq_scheduler = TaskiqScheduler(
    broker=taskiq_broker,
    sources=[LabelScheduleSource(taskiq_broker)],
)
