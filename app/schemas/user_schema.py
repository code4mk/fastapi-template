from pydantic import BaseModel, EmailStr, field_validator


# Pydantic model for creating a new user
class UserCreateSchema(BaseModel):
    """User create schema."""

    name: str | None = None
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        """Validate the password."""
        min_len = 8
        min_len_error = f"Password must be at least {min_len} characters long"

        if len(v) < min_len:
            raise ValueError(min_len_error)

        return v


# Pydantic model for updating user data
class UserUpdateSchema(BaseModel):
    """User update schema."""

    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserLoginSchema(BaseModel):
    """User login schema."""

    id: str
    name: str
    email: EmailStr
