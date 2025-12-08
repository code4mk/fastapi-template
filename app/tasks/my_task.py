from app.taskiq import get_taskiq_broker

tskq_broker = get_taskiq_broker()


@tskq_broker.task(name="task-test-by-mk")
async def task_test_by_mk(data: dict | None = None) -> str:
    """My taskiq task."""
    message = "🚀 My taskiq task is running, pundra!"
    print(f"[TASK EXECUTION] {message} {data.get('name')}")  # noqa: T201
    return message
