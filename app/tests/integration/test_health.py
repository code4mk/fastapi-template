from fastapi import status


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


def test_root_index(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "FastAPI is running..."}


def test_the_index(client):
    response = client.get("/the-index")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "FastAPI is running..."}
