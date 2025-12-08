import os

# datetime imports removed as we're using _delay parameter instead
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.tasks.my_task import task_test_by_mk
from app.utils.tskq.task_invoker import invoke_task
from taskiq.scheduler.scheduled_task import ScheduledTask
from app.services.scheduler_service import get_scheduler_service

# Create a api router
router = APIRouter()


# root index
@router.get("/")
async def root_index() -> JSONResponse:
    """Root endpoint that confirms API is running."""
    data = {
        "message": "FastAPI project is running...",
        "version": os.getenv("PROJECT_VERSION", "1.0.0"),
    }
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)


@router.get("/the-index")
async def the_index() -> JSONResponse:
    """Alternative index endpoint that confirms API is running."""
    data = {
        "message": "FastAPI project is running...",
        "version": os.getenv("PROJECT_VERSION", "1.0.0"),
    }
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)


@router.get("/taskiq-test")
async def taskiq_test() -> JSONResponse:
    """Test endpoint to trigger a TaskIQ task immediately (no delay)."""
    try:
        task_result = await invoke_task(task_test_by_mk, data={"name": "John Doe"})

        return JSONResponse(
            content={
                "message": "TaskIQ task queued immediately",
                "task_id": (
                    str(task_result.task_id) if hasattr(task_result, "task_id") else "unknown"
                ),
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:  # noqa: BLE001
        return JSONResponse(
            content={
                "error": "Failed to queue immediate task",
                "details": str(e),
                "note": "Make sure Redis is running on redis://localhost:6379",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/schedule-test")
async def schedule_test() -> JSONResponse:
    """Test endpoint to schedule a task."""
    try:
        # Create the scheduled task
        scheduled_task = ScheduledTask(
            task_name="app.tasks.my_task:mail_now",  # Full module path to the task
            cron="*/1 * * * *",
            labels={"task-type": "schedule"},
            args=[],
            kwargs={},
        )

        # Register the task with the scheduler service
        scheduler_service = get_scheduler_service()
        result = await scheduler_service.add_scheduled_task(scheduled_task)

        return JSONResponse(content=result, status_code=status.HTTP_200_OK)

    except Exception as e:  # noqa: BLE001
        return JSONResponse(
            content={
                "success": False,
                "message": f"Failed to schedule task: {e!s}",
                "task_info": None,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/schedule-list")
async def schedule_list() -> JSONResponse:
    """List all scheduled tasks."""
    try:
        scheduler_service = get_scheduler_service()
        result = await scheduler_service.list_scheduled_tasks()
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except Exception as e:  # noqa: BLE001
        return JSONResponse(
            content={
                "success": False,
                "message": f"Failed to list scheduled tasks: {e!s}",
                "tasks": [],
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.delete("/schedule-remove/{schedule_id}")
async def schedule_remove(schedule_id: str) -> JSONResponse:
    """Remove a scheduled task."""
    try:
        scheduler_service = get_scheduler_service()
        result = await scheduler_service.remove_scheduled_task(schedule_id)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except Exception as e:  # noqa: BLE001
        return JSONResponse(
            content={
                "success": False,
                "message": f"Failed to remove scheduled task: {e!s}",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/schedule-get/{schedule_id}")
async def schedule_get(schedule_id: str) -> JSONResponse:
    """Get a specific scheduled task by ID."""
    try:
        scheduler_service = get_scheduler_service()
        result = await scheduler_service.get_scheduled_task(schedule_id)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except Exception as e:  # noqa: BLE001
        return JSONResponse(
            content={
                "success": False,
                "message": f"Failed to get scheduled task: {e!s}",
                "task_info": None,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.delete("/schedule-clear-all")
async def schedule_clear_all() -> JSONResponse:
    """Clear all scheduled tasks."""
    try:
        scheduler_service = get_scheduler_service()
        result = await scheduler_service.clear_all_scheduled_tasks()
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except Exception as e:  # noqa: BLE001
        return JSONResponse(
            content={
                "success": False,
                "message": f"Failed to clear scheduled tasks: {e!s}",
                "cleared_count": 0,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/schedule-count")
async def schedule_count() -> JSONResponse:
    """Get the count of scheduled tasks."""
    try:
        scheduler_service = get_scheduler_service()
        count = await scheduler_service.get_scheduled_task_count()
        return JSONResponse(
            content={
                "success": True,
                "message": f"Currently have {count} scheduled tasks",
                "count": count,
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:  # noqa: BLE001
        return JSONResponse(
            content={
                "success": False,
                "message": f"Failed to get scheduled task count: {e!s}",
                "count": 0,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
