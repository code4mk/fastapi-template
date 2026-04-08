import uuid

import factory

from app.models.users import User
from fastapi_pundra.common.password import generate_password_hash

DEFAULT_FACTORY_PASSWORD = "factory_password_123"


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: generate_password_hash(DEFAULT_FACTORY_PASSWORD))
    status = "active"
