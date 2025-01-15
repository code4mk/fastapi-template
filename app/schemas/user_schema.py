from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

# Pydantic model for creating a new user
class UserCreateSchema(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str


# Pydantic model for updating user data
class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserLoginSchema(BaseModel):
    id: str
    name: str
    email: EmailStr