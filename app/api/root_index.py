import os
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

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
