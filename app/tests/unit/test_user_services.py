import pytest
from unittest.mock import Mock, patch
from fastapi import Request
from app.services.user_service import UserService
from app.tests.factories.user_factory import UserFactory
from fastapi_pundra.rest.exceptions import ItemNotFoundException, UnauthorizedException, BaseAPIException
from app.schemas.user_schema import UserCreateSchema
from app.models.users import User
from fastapi_pundra.common.password import compare_hashed_password

@pytest.fixture
def user_service():
    """Return a UserService instance."""
    return UserService()

@pytest.mark.asyncio
async def test_get_users(user_service, db):
    # Create some test users
    users = [UserFactory(status="active") for _ in range(3)]
    users.extend([UserFactory(status="inactive") for _ in range(2)])
    for user in users:
        db.add(user)
    db.commit()

    # Mock request
    mock_request = Mock(spec=Request)
    mock_request.query_params = {}

    result = await user_service.s_get_users(mock_request, db)
    assert "users" in result
    assert len(result["users"]) == 6
   
@pytest.mark.asyncio
async def test_registration_success(user_service, db):
    mock_request = Mock(spec=Request)
    user_data = UserCreateSchema(
        email="mostafa@example.com",
        password="password123",
        name="Test User mostafa"
    )

    result = await user_service.s_registration(mock_request, db, user_data)
    
    assert result["message"] == "Registration successful"
    assert result["user"]["email"] == "mostafa@example.com"
    assert result["user"]["name"] == "Test User mostafa"
    assert result["user"]["status"] == "active"

@pytest.mark.asyncio
async def test_registration_duplicate_email(user_service, db):
    mock_request = Mock(spec=Request)
    user_data = UserCreateSchema(
        email="mostafa@example.com",  # Using the same email as existing_user
        password="password123",
        name="Test User mostafa"
    )

    with pytest.raises(BaseAPIException) as exc:
        await user_service.s_registration(mock_request, db, user_data)
    assert str(exc.value.message) == "Email already registered"  # Fixed assertion to be outside the with block

@pytest.mark.asyncio
async def test_get_user_by_id(user_service, db):
    user = UserFactory()
    db.add(user)
    db.commit()

    mock_request = Mock(spec=Request)
    result = await user_service.s_get_user_by_id(mock_request, db, str(user.id))
    assert result["id"] == str(user.id)

@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_service, db):
    mock_request = Mock(spec=Request)
    nonexistent_uuid = "123e4567-e89b-12d3-a456-426614174000"  # Valid UUID format
    with pytest.raises(ItemNotFoundException):
        await user_service.s_get_user_by_id(mock_request, db, nonexistent_uuid)

@pytest.mark.asyncio
async def test_login_success(user_service, db):
    password = "password123"
    email = "mostafa@example.com"

    mock_request = Mock(spec=Request)
    mock_request.json = Mock(return_value={"email": email, "password": password})

    with patch('app.services.user_service.the_query') as mock_the_query:
        mock_the_query.return_value = {"email": email, "password": password}
        result = await user_service.s_login(mock_request, db)

    assert result["message"] == "Login successful"
    assert "access_token" in result
    assert "refresh_token" in result
    assert result["user"]["email"] == email

@pytest.mark.asyncio
async def test_login_invalid_credentials(user_service, db):
    user = UserFactory()
    db.add(user)
    db.commit()

    mock_request = Mock(spec=Request)
    with patch('app.services.user_service.the_query') as mock_the_query:
        mock_the_query.return_value = {"email": user.email, "password": "wrong_password"}
        with pytest.raises(UnauthorizedException):
            await user_service.s_login(mock_request, db)

@pytest.mark.asyncio
async def test_update_user(user_service, db):
    user = UserFactory()
    db.add(user)
    db.commit()

    mock_request = Mock(spec=Request)
    new_name = "Updated Name"
    
    with patch('app.services.user_service.the_query') as mock_the_query:
        mock_the_query.return_value = {"name": new_name}
        result = await user_service.s_update_user(mock_request, db, str(user.id))

    assert result["message"] == "User updated successfully"
    assert result["user"]["name"] == new_name

@pytest.mark.asyncio
async def test_update_user_not_found(user_service, db):
    mock_request = Mock(spec=Request)
    nonexistent_uuid = "123e4567-e89b-12d3-a456-426614174000"  # Valid UUID format
    with patch('app.services.user_service.the_query') as mock_the_query:
        mock_the_query.return_value = {"name": "New Name"}
        with pytest.raises(ItemNotFoundException):
            await user_service.s_update_user(mock_request, db, nonexistent_uuid)

@pytest.mark.asyncio
async def test_delete_user(user_service, db):
    user = UserFactory()
    db.add(user)
    db.commit()

    mock_request = Mock(spec=Request)
    result = await user_service.s_delete_user(mock_request, db, str(user.id))
    assert result["message"] == "User deleted successfully"

    # Verify user is deleted
    deleted_user = db.query(User).filter_by(id=user.id).first()
    assert deleted_user is None

@pytest.mark.asyncio
async def test_delete_user_not_found(user_service, db):
    mock_request = Mock(spec=Request)
    nonexistent_uuid = "123e4567-e89b-12d3-a456-426614174000"  # Valid UUID format
    with pytest.raises(ItemNotFoundException):
        await user_service.s_delete_user(mock_request, db, nonexistent_uuid)

@pytest.mark.asyncio
async def test_update_user_email_and_password(user_service, db):
    user = UserFactory()
    db.add(user)
    db.commit()

    mock_request = Mock(spec=Request)
    new_email = "newemail@example.com"
    new_password = "newpassword123"
    
    with patch('app.services.user_service.the_query') as mock_the_query:
        mock_the_query.return_value = {
            "email": new_email,
            "password": new_password
        }
        result = await user_service.s_update_user(mock_request, db, str(user.id))

    assert result["message"] == "User updated successfully"
    assert result["user"]["email"] == new_email
    
    # Verify password was hashed and updated
    updated_user = db.query(User).filter_by(id=user.id).first()
    assert compare_hashed_password(new_password, updated_user.password)
