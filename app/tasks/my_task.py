from app.taskiq import get_taskiq_broker

tskq_broker = get_taskiq_broker()


@tskq_broker.task(task_name="mail_now")
async def mail_now() -> str:
    """Send mail now."""
    message = "mail task is running"
    print(f"[TASK EXECUTION] {message}")  # noqa: T201
    return message


@tskq_broker.task(
    task_name="process_user_registration",
)
async def process_user_registration(data: dict | None = None) -> dict:
    """Process user registration tasks like sending welcome email and setting up profile."""
    data = data or {}
    user_id = data.get("user_id", 10)
    email = data.get("email", "test@example.com")

    print(f"[TASK EXECUTION] Processing registration for user {user_id} ({email})")  # noqa: T201
    # Simulate sending welcome email
    # Simulate creating user profile defaults
    # Simulate triggering analytics event
    return {
        "status": "success",
        "user_id": user_id,
        "email": email,
        "message": "User registration processed successfully",
    }


@tskq_broker.task(task_name="generate_monthly_report")
async def generate_monthly_report(data: dict | None = None) -> dict:
    """Generate and send monthly analytics report."""
    data = data or {}
    month = data.get("month")
    year = data.get("year")

    print(f"[TASK EXECUTION] Generating monthly report for {month}/{year}")  # noqa: T201
    # Simulate data aggregation
    # Simulate report generation
    # Simulate sending report to stakeholders
    return {
        "status": "completed",
        "report_period": f"{month}/{year}",
        "message": "Monthly report generated and sent successfully",
    }
