from pydantic import BaseModel, EmailStr, field_serializer
from uuid import UUID

class UserSerializer(BaseModel):
    id: UUID
    name: str | None = None
    email: EmailStr | None = None
    status: str | None = None

    @field_serializer('id')
    def serialize_id(self, id: UUID):
        return str(id)

    class Config:
        from_orm = True
        from_attributes = True

class UserLoginSerializer(BaseModel):
    id: UUID
    name: str | None = None
    email: EmailStr | None = None
    status: str | None = None

    @field_serializer('id')
    def serialize_id(self, id: UUID):
        return str(id)

    class Config:
        from_orm = True
        from_attributes = True