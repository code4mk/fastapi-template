import asyncio
from datetime import UTC, datetime

from app.taskiq import get_taskiq_broker

broker = get_taskiq_broker()


def resolve_task(task_ref: object) -> object:
    """
    Resolve a task reference to a TaskIQ task object.

    Accepts a task object and returns the taskiq Task object.
    """
    if not task_ref:
        error_msg = "Task reference cannot be empty."
        raise ValueError(error_msg)

    # If already a task function → return
    if hasattr(task_ref, "kiq"):
        return task_ref

    error_msg = "Invalid task reference. Pass task object."
    raise ValueError(error_msg)


async def invoke_task(
    task_ref: object,
    data: dict[str, object] | None = None,
    delay: int | None = None,
) -> object:
    """
    Invoke a TaskIQ task immediately or with delay.

    Note: Delay is implemented using asyncio.sleep before task execution.
    For production use, consider using a proper task scheduler like taskiq-scheduler.

    :param task_ref: task object
    :param data: data dict to pass as the 'data' parameter to the task
    :param delay: seconds (int) if delayed execution
    """
    data = data or {}
    task = resolve_task(task_ref)

    # 1️⃣ Run immediately
    if delay is None:
        return await task.kiq(data=data)

    # 2️⃣ Simple delay implementation
    # Note: This creates a background task that waits and then executes
    async def delayed_execution() -> object:
        await asyncio.sleep(delay)
        return await task.kiq(data=data)

    # Create and return the background task
    # The task will execute after the delay
    background_task = asyncio.create_task(delayed_execution())

    # Keep a reference to prevent garbage collection
    # Store it in a module-level set or similar in production
    background_tasks = getattr(invoke_task, "background_tasks", set())
    background_tasks.add(background_task)
    background_task.add_done_callback(background_tasks.discard)
    invoke_task.background_tasks = background_tasks

    # Return a mock result immediately for API response
    class MockTaskResult:
        def __init__(self, task_id: str) -> None:
            self.task_id = task_id

    return MockTaskResult(f"delayed-{task.task_name}-{datetime.now(UTC).timestamp()}")
