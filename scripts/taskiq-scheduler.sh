#!/bin/bash

set -e
set -x

# Run Taskiq worker
# This script starts a Taskiq worker that will process tasks from app/tasks/my_taskiq_task.py

echo "Starting Taskiq scheduler..."
echo "Make sure Redis is running on redis://localhost:6379/0 or set REDIS_URL environment variable"

# Run the taskiq scheduler command
uv run python -m taskiq scheduler app.taskiq:taskiq_scheduler --skip-first-run
