from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

# Create a api router
router = APIRouter()

# root index
@router.get("/")
async def root_index(request: Request):
    data = {
      'message': 'fastapi is running....'
    }
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)

@router.get("/the-index")
async def the_index(request: Request):
    data = {
      'message': 'fastapi is running....'
    }
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    