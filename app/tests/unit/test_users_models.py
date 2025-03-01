from app.models.users import User
from app.tests.factories.user_factory import UserFactory


def test_user_model_creation():
    user = UserFactory.build()
    assert isinstance(user, User)
    assert user.email is not None
    assert user.name is not None
    assert user.status == "active"


def test_user_as_dict():
    user = UserFactory.build()
    user_dict = user.as_dict()
    assert isinstance(user_dict, dict)
    assert "id" in user_dict
    assert "email" in user_dict
    assert "name" in user_dict
