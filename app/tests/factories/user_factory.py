import uuid

import factory
from factory.fuzzy import FuzzyText

from app.models.users import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: "hashed_" + FuzzyText(length=10).fuzz())
    status = "active"
