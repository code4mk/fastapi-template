from app.taskiq import get_taskiq_broker


tskq_broker = get_taskiq_broker()


@tskq_broker.task(
    name="task-schedule-test-by-mk",
    schedule=[{"cron": "*/1 * * * *"}],  # every 1 minute
)
async def task_schedule_test_by_mk() -> str:
    """My schedule task."""
    message = "🚀 My schedule task is running, every 1 minute"
    print(f"[TASK EXECUTION] {message}")  # noqa: T201
    return message


@tskq_broker.task(name="mail_now_schedule", schedule=[{"cron": "*/1 * * * *"}])
async def mail_now_schedule() -> str:
    """Send mail now."""
    message = "🚀 Sending mail now schedule"
    print(f"[TASK EXECUTION] {message}")  # noqa: T201
    return message
