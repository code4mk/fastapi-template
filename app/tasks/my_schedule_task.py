from app.taskiq import get_taskiq_broker

tskq_broker = get_taskiq_broker()


@tskq_broker.task(
    task_name="task-schedule-test-by-mk",
    schedule=[{"cron": "*/2 * * * *"}],  # every 1 minute
)
async def task_schedule_test_by_mk() -> str:
    """My schedule task."""
    message = "🚀 My schedule task is running, every 2 minute"
    print(f"[TASK EXECUTION] {message}")  # noqa: T201
    return message


@tskq_broker.task(task_name="mail_now_schedule", schedule=[{"cron": "*/2 * * * *"}])
async def mail_now_schedule() -> str:
    """Send mail now."""
    message = "🚀 Sending mail now schedule every 2 minute"
    print(f"[TASK EXECUTION] {message}")  # noqa: T201
    return message
