#!/bin/bash

set -e
set -x

echo "Starting Taskiq scheduler..."

uv run python -m taskiq scheduler app.taskiq:taskiq_scheduler --skip-first-run --update-interval=10
