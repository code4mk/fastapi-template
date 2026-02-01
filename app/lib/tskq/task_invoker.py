from app.taskiq import get_taskiq_broker
from datetime import UTC, datetime, timedelta
from app.taskiq import get_list_schedule_source


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
    task_ref: str | object,
    data: dict[str, object] | None = None,
    delay: int | None = None,
) -> object:
    """
    Invoke a TaskIQ task immediately or schedule it for later.

    :param task_ref: task name (string) or task object
    :param data: data dict to pass as the 'data' parameter to the task
    :param delay: delay in seconds to schedule the task
    :return: the task result or scheduled task id
    """
    data = data or {}
    task = resolve_task(task_ref)

    if delay:
        return await task.kicker().schedule_by_time(
            get_list_schedule_source(), datetime.now(UTC) + timedelta(seconds=delay), data=data
        )

    return await task.kiq(data=data)
