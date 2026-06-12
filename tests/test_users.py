import uuid
from http import HTTPStatus

from src.schemas.users import UserUpdate


class TestCreateUser:
    async def test_create(self, async_client):
        response = await async_client.post(
            "/users/create",
            json={"login": "user", "password": "aboba"},
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


class TestGetUserById:
    async def test_get_by_id(self, alice_client, alice):
        response = await alice_client.get(f"/users/id/{alice.id}")
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        assert data["login"] == alice.login
        assert data["id"] == str(alice.id)

    async def test_get_by_id_nonexistent(self, alice_client, alice):

        nonexistent_id = uuid.UUID(int=alice.id.int ^ 1)
        # если использовать uuid.uuid4(), то раз в триллион запусков тест упадёт
        # я не хочу полагаться на рандом)
        response = await alice_client.get(f"/users/id/{nonexistent_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    async def test_get_by_id_unauthorized(self, async_client, alice):
        response = await async_client.get(f"/users/id/{alice.id}")
        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestGetUserByLogin:
    async def test_get_by_login(self, alice_client, alice):
        response = await alice_client.get(f"/users/login/{alice.login}")
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        assert data["login"] == alice.login
        assert data["id"] == str(alice.id)

    async def test_get_by_login_nonexistent(self, alice_client, alice):
        nonexistent_login = "koitese"
        response = await alice_client.get(f"/users/login/{nonexistent_login}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    async def test_get_by_login_unauthorized(self, async_client, alice):
        response = await async_client.get(f"/users/login/{alice.login}")
        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestUpdateUser:
    async def test_update(self, alice, alice_client, new_alice):
        response = await alice_client.post(
            f"/users/update/{alice.id}",
            json={"login": new_alice.login, "password": new_alice.password},
        )
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["login"] == new_alice.login
        assert data["id"] == str(alice.id)

    async def test_update_nonauthorized(self, alice, async_client, new_alice):
        response = await async_client.post(
            f"/users/update/{alice.id}",
            json={"login": new_alice.login, "password": new_alice.password},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_update_forbidden(self, alice, bob_client, new_alice):
        response = await bob_client.post(
            f"/users/update/{alice.id}",
            json={"login": new_alice.login, "password": new_alice.password},
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
