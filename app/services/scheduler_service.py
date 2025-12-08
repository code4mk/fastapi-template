"""Scheduler service for managing TaskIQ scheduled tasks."""

from typing import Any

from taskiq.scheduler.scheduled_task import ScheduledTask
from app.taskiq import get_taskiq_scheduler, get_dynamic_schedule_source


class SchedulerService:
    """Service for managing scheduled tasks."""

    def __init__(self) -> None:
        """Initialize the scheduler service."""
        self.scheduler = get_taskiq_scheduler()
        self.dynamic_source = get_dynamic_schedule_source()

    async def add_scheduled_task(self, scheduled_task: ScheduledTask) -> dict[str, Any]:
        """
        Add a scheduled task to the scheduler.

        Args:
            scheduled_task: The ScheduledTask object to add

        Returns:
            dict: Response containing task information

        """
        try:
            # Add the task to the dynamic schedule source
            await self.dynamic_source.add_schedule(scheduled_task)
        except (ValueError, TypeError, RuntimeError) as e:
            return {
                "success": False,
                "message": f"Failed to register scheduled task: {e!s}",
                "task_info": None,
            }
        else:
            return {
                "success": True,
                "message": f"Scheduled task '{scheduled_task.task_name}' registered successfully",
                "task_info": {
                    "task_name": scheduled_task.task_name,
                    "schedule_id": scheduled_task.schedule_id,
                    "cron": scheduled_task.cron,
                    "labels": scheduled_task.labels,
                    "args": scheduled_task.args,
                    "kwargs": scheduled_task.kwargs,
                },
            }

    async def remove_scheduled_task(self, schedule_id: str) -> dict[str, Any]:
        """
        Remove a scheduled task from the scheduler.

        Args:
            schedule_id: The ID of the scheduled task to remove

        Returns:
            dict: Response containing removal status

        """
        try:
            # Remove the task from the dynamic schedule source
            await self.dynamic_source.delete_schedule(schedule_id)
        except KeyError:
            return {
                "success": False,
                "message": f"Scheduled task with ID '{schedule_id}' not found",
            }
        except (ValueError, TypeError, RuntimeError) as e:
            return {
                "success": False,
                "message": f"Failed to remove scheduled task: {e!s}",
            }
        else:
            return {
                "success": True,
                "message": f"Scheduled task with ID '{schedule_id}' removed successfully",
            }

    async def list_scheduled_tasks(self) -> dict[str, Any]:
        """
        List all scheduled tasks.

        Returns:
            dict: Response containing list of scheduled tasks

        """
        try:
            # Get all scheduled tasks from the dynamic source
            scheduled_tasks = await self.dynamic_source.get_schedules()

            # Convert to serializable format
            tasks_data = [
                {
                    "task_name": task.task_name,
                    "schedule_id": task.schedule_id,
                    "cron": task.cron,
                    "labels": task.labels,
                    "args": task.args,
                    "kwargs": task.kwargs,
                    "task_id": task.task_id,
                    "time": task.time.isoformat() if task.time else None,
                    "interval": str(task.interval) if task.interval else None,
                }
                for task in scheduled_tasks
            ]

            return {
                "success": True,
                "message": f"Retrieved {len(tasks_data)} scheduled tasks successfully",
                "tasks": tasks_data,
                "count": len(tasks_data),
            }
        except (ValueError, TypeError, RuntimeError) as e:
            return {
                "success": False,
                "message": f"Failed to retrieve scheduled tasks: {e!s}",
                "tasks": [],
                "count": 0,
            }

    async def get_scheduled_task(self, schedule_id: str) -> dict[str, Any]:
        """
        Get a specific scheduled task by ID.

        Args:
            schedule_id: The ID of the scheduled task to retrieve

        Returns:
            dict: Response containing task information

        """
        try:
            task = await self.dynamic_source.get_schedule_by_id(schedule_id)

            if task is None:
                return {
                    "success": False,
                    "message": f"Scheduled task with ID '{schedule_id}' not found",
                    "task_info": None,
                }

            return {
                "success": True,
                "message": f"Retrieved scheduled task '{task.task_name}' successfully",
                "task_info": {
                    "task_name": task.task_name,
                    "schedule_id": task.schedule_id,
                    "cron": task.cron,
                    "labels": task.labels,
                    "args": task.args,
                    "kwargs": task.kwargs,
                    "task_id": task.task_id,
                    "time": task.time.isoformat() if task.time else None,
                    "interval": str(task.interval) if task.interval else None,
                },
            }
        except (ValueError, TypeError, RuntimeError) as e:
            return {
                "success": False,
                "message": f"Failed to retrieve scheduled task: {e!s}",
                "task_info": None,
            }

    async def clear_all_scheduled_tasks(self) -> dict[str, Any]:
        """
        Clear all scheduled tasks from the dynamic source.

        Returns:
            dict: Response containing clearing status

        """
        try:
            count = await self.dynamic_source.clear_all_schedules()
        except (ValueError, TypeError, RuntimeError) as e:
            return {
                "success": False,
                "message": f"Failed to clear scheduled tasks: {e!s}",
                "cleared_count": 0,
            }
        else:
            return {
                "success": True,
                "message": f"Cleared {count} scheduled tasks successfully",
                "cleared_count": count,
            }

    async def get_scheduled_task_count(self) -> int:
        """
        Get the number of scheduled tasks in the dynamic source.

        Returns:
            int: Number of scheduled tasks

        """
        # Use async method for Redis-backed source
        if hasattr(self.dynamic_source, "get_schedule_count_async"):
            return await self.dynamic_source.get_schedule_count_async()
        return self.dynamic_source.get_schedule_count()


# Create a global instance
scheduler_service = SchedulerService()


def get_scheduler_service() -> SchedulerService:
    """Get the scheduler service instance."""
    return scheduler_service
