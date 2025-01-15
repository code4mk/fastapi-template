from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import uuid

# Pydantic model for creating a new user
class UserCreateSchema(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


# Pydantic model for updating user data
class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserLoginSchema(BaseModel):
    id: str
    name: str
    email: EmailStr