from uuid import UUID

from pydantic import BaseModel, EmailStr, field_serializer


class UserSerializer(BaseModel):
    """User serializer."""

    id: UUID
    name: str | None = None
    email: EmailStr | None = None
    status: str | None = None

    @field_serializer("id")
    def serialize_id(self, uuid: UUID) -> str:
        """Serialize the id."""
        return str(uuid)

    model_config = {"from_attributes": True}


class UserLoginSerializer(BaseModel):
    """User login serializer."""

    id: UUID
    name: str | None = None
    email: EmailStr | None = None
    status: str | None = None

    @field_serializer("id")
    def serialize_id(self, uuid: UUID) -> str:
        """Serialize the id."""
        return str(uuid)

    model_config = {"from_attributes": True}
