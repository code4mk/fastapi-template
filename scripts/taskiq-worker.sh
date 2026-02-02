#!/bin/bash

set -e
set -x

echo "Starting Taskiq worker..."

uv run python -m taskiq worker app.taskiq:taskiq_broker --workers 1 "${@}"
