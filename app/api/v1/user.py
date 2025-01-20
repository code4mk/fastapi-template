from fastapi import APIRouter, Request, status, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from fastapi_pundra.rest.validation import dto
from fastapi_pundra.rest.helpers import the_query


# Create a api router
router = APIRouter()

# User service
user_service = UserService()

# Registration route
@router.post("/users/registration")
@dto(UserCreateSchema)
async def registration(request: Request, background_tasks: BackgroundTasks):
    
    # Retrieve data from the request
    request_data = await the_query(request)
    data = UserCreateSchema(**request_data)
    
    output = await user_service.s_registration(request, data, background_tasks)
    return JSONResponse(content=output, status_code=status.HTTP_201_CREATED)

@router.post("/users/login")
async def login(request: Request):
    data = await user_service.s_login(request)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

@router.get("/users")
async def get_users(request: Request):
    data = await user_service.s_get_users(request)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

@router.get("/users/{id}")
async def get_user(request: Request, id: int|str):
    data = await user_service.s_get_user_by_id(request,user_id=id)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

@router.put("/users/{id}/update")
@dto(UserUpdateSchema)
async def update_user(request: Request, id: int|str):
    data = await user_service.s_update_user(request, user_id=id)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

@router.delete("/users/{id}/delete")
async def delete_user(request: Request, id: int|str):
    data = await user_service.s_delete_user(request, user_id=id)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)