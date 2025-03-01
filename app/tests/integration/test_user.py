from fastapi import status


def test_user_registration(client):
    user_data = {"name": "Test User", "email": "test@example.com", "password": "password123"}

    response = client.post("/api/v1/users/registration", json=user_data)
    print(response.json())
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["message"] == "Registration successful"
    assert data["user"]["email"] == user_data["email"]


def test_user_login(client):

    # Then try to login
    login_data = {"email": "test@example.com", "password": "password123"}

    response = client.post("/api/v1/users/login", json=login_data)
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Login successful"
    assert "access_token" in data
    assert "refresh_token" in data
