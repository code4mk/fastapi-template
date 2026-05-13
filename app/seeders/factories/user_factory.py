"""Factory for generating User model instances."""

import secrets
import uuid

import factory

from app.models.users import User
from fastapi_pundra.common.password import generate_password_hash


def random_plain_password() -> str:
    """Return a URL-safe random string for local dev credentials."""
    return secrets.token_urlsafe(16)


class UserFactory(factory.Factory):
    """Factory for generating User model instances."""

    class Meta:  # noqa: D106
        model = User

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.LazyFunction(
        lambda: generate_password_hash(random_plain_password()),
    )
    status = "active"
