# from app.taskiq import get_taskiq_broker

# tskq_broker = get_taskiq_broker()


# @tskq_broker.task(
#     task_name="task-schedule-test",
#     schedule=[{"cron": "*/1 * * * *"}],  # every 1 minute
# )
# async def task_schedule_test() -> str:
#     """My schedule task."""
#     message = "schedule task is running every 1 minute"
#     print(f"[TASK EXECUTION] {message}")
#     return message


# @tskq_broker.task(
#     task_name="mail_schedule_task",
#     schedule=[{"cron": "*/2 * * * *"}] # every 2 minute
# )
# async def mail_schedule_task() -> str:
#     """Send mail now."""
#     message = "mail schedule task is running every 2 minute"
#     print(f"[TASK EXECUTION] {message}")
#     return message
