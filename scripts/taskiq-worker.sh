#!/bin/bash

set -e
set -x

# Run Taskiq worker
# This script starts a Taskiq worker that will process tasks from app/tasks/my_taskiq_task.py

echo "Starting Taskiq worker..."
echo "Make sure Redis is running on redis://localhost:6379/0 or set REDIS_URL environment variable"

# Run the taskiq worker command
uv run python -m taskiq worker app.taskiq:taskiq_broker "${@}"
