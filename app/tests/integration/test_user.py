import io

from fastapi import status

_user_id: str | None = None
_access_token: str | None = None


def _auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {_access_token}"}


def test_user_registration(client):
    global _user_id
    user_data = {"name": "Test User", "email": "test@example.com", "password": "password123"}

    response = client.post("/api/v1/users/registration", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["message"] == "Registration successful"
    assert data["user"]["email"] == user_data["email"]
    _user_id = data["user"]["id"]


def test_user_login(client):
    global _access_token
    login_data = {"email": "test@example.com", "password": "password123"}

    response = client.post("/api/v1/users/login", json=login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Login successful"
    assert "access_token" in data
    assert "refresh_token" in data
    _access_token = data["access_token"]


def test_get_users(client):
    response = client.get("/api/v1/users", headers=_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "users" in data
    assert len(data["users"]) >= 1


def test_get_user_by_id(client):
    response = client.get(f"/api/v1/users/{_user_id}", headers=_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["id"] == _user_id


def test_update_user(client):
    response = client.put(
        f"/api/v1/users/{_user_id}/update",
        json={"name": "Updated User"},
        headers=_auth_headers(),
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "User updated successfully"
    assert data["user"]["name"] == "Updated User"


def test_profile_image_upload(client):
    fake_image = io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 64)
    response = client.post(
        "/api/v1/users/profile-image",
        files={"image": ("avatar.png", fake_image, "image/png")},
        headers=_auth_headers(),
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["profile_image"] == "avatar.png"
    assert data["profile_image_content_type"] == "image/png"


def test_raw_sql_get_users(client):
    response = client.get("/api/v1/users/raw-sql/users", headers=_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "users" in data
    assert len(data["users"]) >= 1


def test_raw_sql_get_user_by_id(client):
    response = client.get(f"/api/v1/users/raw-sql/users/{_user_id}", headers=_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test@example.com"


def test_delete_user(client):
    response = client.delete(f"/api/v1/users/{_user_id}/delete", headers=_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "User deleted successfully"
