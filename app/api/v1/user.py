from __future__ import annotations

from fastapi import APIRouter, Request, status, Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_pundra.rest.helpers import the_query
from fastapi_pundra.rest.validation import dto
from sqlalchemy.orm import Session
from app.database.database import get_db_session
from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from app.services.user_service import UserService

# Create a api router
router = APIRouter()

# User service
user_service = UserService()


# Registration route
@router.post("/users/registration")
@dto(UserCreateSchema)
async def registration(
    request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db_session)
) -> JSONResponse:
    """Register a new user."""
    # Retrieve data from the request
    request_data = await the_query(request)
    data = UserCreateSchema(**request_data)

    output = await user_service.s_registration(request, db, data, background_tasks)
    return JSONResponse(content=output, status_code=status.HTTP_201_CREATED)


@router.post("/users/login")
async def login(request: Request, db: Session = Depends(get_db_session)) -> JSONResponse:
    """Login a user."""
    data = await user_service.s_login(request, db)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


@router.get("/users")
async def get_users(request: Request, db: Session = Depends(get_db_session)) -> JSONResponse:
    """Get all users."""
    data = await user_service.s_get_users(request, db)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


@router.get("/users/{user_id}")
async def get_user(
    request: Request, user_id: int | str, db: Session = Depends(get_db_session)
) -> JSONResponse:
    """Get a user by id."""
    data = await user_service.s_get_user_by_id(request, db, user_id=user_id)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


@router.put("/users/{user_id}/update")
@dto(UserUpdateSchema)
async def update_user(
    request: Request, user_id: int | str, db: Session = Depends(get_db_session)
) -> JSONResponse:
    """Update a user by id."""
    data = await user_service.s_update_user(request, db, user_id=user_id)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


@router.delete("/users/{user_id}/delete")
async def delete_user(
    request: Request, user_id: int | str, db: Session = Depends(get_db_session)
) -> JSONResponse:
    """Delete a user by id."""
    data = await user_service.s_delete_user(request, db, user_id=user_id)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)
