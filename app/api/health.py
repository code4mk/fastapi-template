from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

# Create a api router
router = APIRouter(prefix="/health")


# Health check route
@router.get("/")
async def health() -> JSONResponse:
    """Health check route."""
    data = {"status": "ok"}
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)


@router.get("/check")
async def health_check() -> JSONResponse:
    """Health check route."""
    data = {"status": "check ok"}
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)
