from __future__ import annotations
from typing import Any
from fastapi import APIRouter, Request, status, Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_pundra.rest.helpers import the_query
from fastapi_pundra.rest.validation import dto
from fastapi_pundra.rest.openapi import openapi_request_body_schema
from sqlalchemy.orm import Session
from app.lib.database import get_db_session
from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema, UserLoginSchema
from app.services.user_service import UserService

# Create a api router
router = APIRouter(prefix="/api/v1", tags=["User"])

# User service
user_service = UserService()


# Registration route
@router.post("/users/registration", openapi_extra={**openapi_request_body_schema(UserCreateSchema)})
@dto(UserCreateSchema)
async def registration(
    request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db_session)
) -> dict[str, Any]:
    """Register a new user."""
    # Retrieve data from the request
    request_data = await the_query(request)
    data = UserCreateSchema(**request_data)

    output = await user_service.s_registration(request, db, data, background_tasks)
    return JSONResponse(content=output, status_code=status.HTTP_201_CREATED)


@router.post("/users/login", openapi_extra={**openapi_request_body_schema(UserLoginSchema)})
@dto(UserLoginSchema)
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


@router.put(
    "/users/{user_id}/update", openapi_extra={**openapi_request_body_schema(UserUpdateSchema)}
)
@dto(UserUpdateSchema)
async def update_user(
    request: Request, user_id: int | str, db: Session = Depends(get_db_session)
) -> dict[str, Any]:
    """
    Update a user by id.

    The request body will be validated against UserUpdateSchema.
    """
    # The validated data is now available in request.state.validated_data
    data = request.state.validated_data

    data = await user_service.s_update_user(request, db, user_id=user_id)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


@router.delete("/users/{user_id}/delete")
async def delete_user(
    request: Request, user_id: int | str, db: Session = Depends(get_db_session)
) -> JSONResponse:
    """Delete a user by id."""
    data = await user_service.s_delete_user(request, db, user_id=user_id)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


@router.get("/users/raw-sql/users")
async def raw_sql_get_users(
    request: Request, db: Session = Depends(get_db_session)
) -> JSONResponse:
    """Get users using raw SQL."""
    data = await user_service.s_raw_sql_get_users(request, db)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


@router.get("/users/raw-sql/users/{user_id}")
async def raw_sql_get_user_by_id(
    request: Request, user_id: str, db: Session = Depends(get_db_session)
) -> JSONResponse:
    """Get user by id using raw SQL."""
    data = await user_service.s_raw_sql_get_user_by_id(request, db, user_id=user_id)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)
