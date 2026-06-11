from src.schemas.users import UserResponse
from http import HTTPStatus


class TestCreateUser:
    async def test_create(self, async_client):
        response = await async_client.post(
            "/users/create",
            json={
                "login": "user",
                "password": "aboba",
            },
        )
        assert response.status_code == HTTPStatus.CREATED

        data = response.json()
        assert data["login"] == "user"
        assert "id" in data
        assert "created_at" in data

    async def test_duplicate_login(self, async_client):
        await async_client.post(
            "/users/create",
            json={"login": "dup", "password": "first"},
        )
        response = await async_client.post(
            "/users/create",
            json={"login": "dup", "password": "second"},
        )
        assert response.status_code == HTTPStatus.CONFLICT

    async def test_validation_error(self, async_client):
        response = await async_client.post(
            "/users/create", json={"login": "абоба", "password": "aboba"}
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
