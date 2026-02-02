# Task Scheduler - Quick Start Guide

## Environment Setup

Add to your `.env` file:

```bash
REDIS_URL=redis://localhost:6379/0
```


## 1. Create a Task

Create tasks in `app/tasks/` directory:

```python
from app.taskiq import get_taskiq_broker

tskq_broker = get_taskiq_broker()

@tskq_broker.task(task_name="send_email")
async def send_email(data: dict | None = None) -> dict:
    """Send email task."""
    data = data or {}
    email = data.get("email", "user@example.com")
    
    # Your task logic here
    print(f"[TASK] Sending email to {email}")
    
    return {
        "status": "success",
        "email": email,
        "message": "Email sent successfully"
    }
```

---

## 2. Invoke Tasks

### Immediate Execution

```python
from app.tasks.my_task import send_email
from app.lib.tskq.task_invoker import invoke_task

# Execute immediately
await invoke_task(
    send_email,
    data={"email": "user@example.com"}
)
```

### Delayed Execution

```python
# Execute after 60 seconds delay
await invoke_task(
    send_email,
    data={"email": "user@example.com"},
    delay=60
)
```



## 3. Create a Schedule Task (Recurring)

### Static Schedule (Decorator-Based)

Create scheduled tasks in `app/tasks/` directory using the `schedule` parameter:

```python
from app.taskiq import get_taskiq_broker

tskq_broker = get_taskiq_broker()

@tskq_broker.task(
    task_name="task-schedule-test",
    schedule=[{"cron": "*/1 * * * *"}],  # every 1 minute
)
async def task_schedule_test() -> str:
    """My schedule task."""
    message = "schedule task is running every 1 minute"
    print(f"[TASK EXECUTION] {message}")
    return message
```

**Note**: These tasks will automatically run on schedule when the scheduler is started.


## 4. Running Locally

### Start Worker (Required for task execution)

```bash
bash scripts/taskiq-worker.sh
```

### Start Scheduler (Required for scheduled tasks)

```bash
bash scripts/taskiq-scheduler.sh
```

**Note**: Both worker and scheduler must be running for scheduled tasks to execute.

---

