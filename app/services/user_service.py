from fastapi import Request
from fastapi_pundra.common.jwt_utils import create_access_token, create_refresh_token
from fastapi_pundra.common.password import compare_hashed_password, generate_password_hash
from fastapi_pundra.rest.exceptions import (
    BaseAPIException,
    ItemNotFoundException,
    UnauthorizedException,
)
from fastapi_pundra.rest.helpers import the_query, the_sorting
from fastapi_pundra.rest.paginate import paginate
from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.user_schema import UserCreateSchema
from app.serializers.user_serializer import UserLoginSerializer, UserSerializer


class UserService:
    """User service."""

    async def s_registration(self, request: Request, db: Session, data: UserCreateSchema) -> dict:
        """Register a new user."""
        db_user = db.query(User).filter(User.email == data.email).first()

        if db_user:
            raise BaseAPIException(message="Email already registered", status_code=400)

        new_user = User()
        new_user.email = data.email
        new_user.password = generate_password_hash(data.password)
        new_user.name = data.name
        new_user.status = "active"

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        user_data = UserSerializer(**new_user.as_dict())

        # Send welcome email in background
        # template_name = "welcome_email.html"
        # context = {
        #     "name": new_user.name or new_user.email,
        #     "activation_link": f"{request.base_url}api/v1/users/activate",
        # }

        # await send_mail_background(
        #     background_tasks=background_tasks,
        #     subject=f"Welcome, {new_user.name or new_user.email}!",
        #     to=[new_user.email],
        #     template_name=template_name,
        #     context=context,
        # )

        return {"message": "Registration successful", "user": user_data.model_dump()}

    async def s_get_users(self, request: Request, db: Session) -> dict:
        """Get users."""
        query = db.query(User)

        # TODO: add logic here if you want to filter users

        query = the_sorting(request, query)

        def additional_data(data: list) -> dict:
            total_active_users = len([user for user in data if user.status == "active"])
            total_inactive_users = len([user for user in data if user.status == "inactive"])
            return {"active_users": total_active_users, "inactive_users": total_inactive_users}

        return paginate(
            request,
            query,
            serilizer=UserSerializer,
            wrap="users",
            additional_data=additional_data,
        )

    async def s_get_user_by_id(self, request: Request, db: Session, user_id: str) -> User:
        """Get user by id."""
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise ItemNotFoundException(message="User not found")
        return user

    async def s_login(self, request: Request, db: Session) -> dict:
        """Login a user."""
        # Get data from request
        the_data = await the_query(request)
        email = the_data.get("email")
        password = the_data.get("password")

        # Find user by email
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise UnauthorizedException(message="Invalid credentials")

        # Verify password
        if not compare_hashed_password(password, user.password):
            raise UnauthorizedException(message="Invalid credentials")

        # Create token payload
        token_payload = {
            "user_id": str(user.id),
            "name": user.name,
            "email": user.email,
            "status": user.status,
        }

        # Generate tokens
        access_token = create_access_token(token_payload)
        refresh_token = create_refresh_token(token_payload)

        user_data = UserLoginSerializer(**user.as_dict())

        return {
            "message": "Login successful",
            "user": user_data.model_dump(),
            "type": "Bearer",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def s_update_user(self, request: Request, db: Session, user_id: str) -> dict:
        """Update a user."""
        the_data = await the_query(request)
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise ItemNotFoundException(message="User not found")

        if the_data.get("name"):
            user.name = the_data.get("name")
        if the_data.get("email"):
            user.email = the_data.get("email")
        if the_data.get("password"):
            user.password = generate_password_hash(the_data.get("password"))
        db.commit()
        db.refresh(user)

        user_data = UserSerializer(**user.as_dict())
        return {"message": "User updated successfully", "user": user_data.model_dump()}

    async def s_delete_user(self, request: Request, db: Session, user_id: str) -> dict:
        """Delete a user."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ItemNotFoundException(message="User not found")
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
