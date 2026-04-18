from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from app.config.settings import settings

# Create a api router
router = APIRouter()


# root index
@router.get("/")
async def root_index() -> JSONResponse:
    """Root endpoint that confirms API is running."""
    data = {
        "message": "FastAPI project is running...",
        "version": settings.project_version,
    }
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)


@router.get("/the-index")
async def the_index(request: Request) -> JSONResponse:
    """Alternative index endpoint that confirms API is running."""
    data = {
        "message": "FastAPI project is running...",
        "version": settings.project_version,
    }

    return JSONResponse(content=data, status_code=status.HTTP_200_OK)
