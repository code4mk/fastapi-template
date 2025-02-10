from pydantic import BaseModel, EmailStr, field_validator


# Pydantic model for creating a new user
class UserCreateSchema(BaseModel):
    """User create schema."""

    MIN_PASSWORD_LENGTH = 8

    name: str | None = None
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(self, v: str) -> str:
        """Validate the password."""
        min_len_error = f"Password must be at least {self.MIN_PASSWORD_LENGTH} characters long"

        if len(v) < self.MIN_PASSWORD_LENGTH:
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
