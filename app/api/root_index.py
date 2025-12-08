import os

# datetime imports removed as we're using _delay parameter instead
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.tasks.my_task import task_test_by_mk
from app.utils.tskq.task_invoker import invoke_task

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
