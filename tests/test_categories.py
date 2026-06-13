import uuid

from http import HTTPStatus
from src.schemas.categories import CategoryCreate


class TestCreateCategory:
    async def test_create(self, alice_client, alice):
        category_create = CategoryCreate(
            title="Category Title",
            description="Category Description",
            is_published=True,
            author_id=alice.id,
        )

        response = await alice_client.post(
            "/categories/create", json=category_create.model_dump(mode="json")
        )
        assert response.status_code == HTTPStatus.CREATED

        data = response.json()

        assert "id" in data
        assert data["title"] == category_create.title
        assert data["description"] == category_create.description
        assert data["author_id"] == str(category_create.author_id)
        assert "created_at" in data

    async def test_create_duplicate(self, alice_client, alice_category):
        category_create = CategoryCreate(
            title=alice_category.title,
            description=alice_category.description,
            is_published=True,
            author_id=alice_category.author_id,
        )
        response = await alice_client.post(
            "/categories/create", json=category_create.model_dump(mode="json")
        )

        assert response.status_code == HTTPStatus.CONFLICT

    async def test_create_another_account(self, bob_client, alice):
        category_create = CategoryCreate(
            title="Category Title",
            description="Category Description",
            is_published=True,
            author_id=alice.id,
        )

        response = await bob_client.post(
            "/categories/create", json=category_create.model_dump(mode="json")
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

    async def test_create_nonexistent(self, alice_client, alice):

        nonexistent_id = uuid.UUID(int=alice.id.int ^ 1)
        category_create = CategoryCreate(
            title="Category Title",
            description="Category Description",
            is_published=True,
            author_id=nonexistent_id,
        )

        response = await alice_client.post(
            "/categories/create", json=category_create.model_dump(mode="json")
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    async def test_create_unauthorized(self, async_client, alice):
        category_create = CategoryCreate(
            title="Category Title",
            description="Category Description",
            is_published=True,
            author_id=alice.id,
        )

        response = await async_client.post(
            "/categories/create", json=category_create.model_dump(mode="json")
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestGetByIdCategory:
    async def test_get_by_id(self, alice_client, alice_category):
        response = await alice_client.get(f"/categories/{alice_category.id}")
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        assert data["id"] == str(alice_category.id)
        assert data["title"] == alice_category.title
        assert data["description"] == alice_category.description
        assert data["author_id"] == str(alice_category.author_id)
        assert "created_at" in data

    async def test_get_by_id_nonexistent(self, alice_client, alice_category):
        nonexistent_id = uuid.UUID(int=alice_category.id.int ^ 1)
        response = await alice_client.get(f"/categories/{nonexistent_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    async def test_get_by_id_unauthorized(self, async_client, alice_category):
        response = await async_client.get(f"/categories/{alice_category.id}")
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        assert data["id"] == str(alice_category.id)
        assert data["title"] == alice_category.title
        assert data["description"] == alice_category.description
        assert data["author_id"] == str(alice_category.author_id)
        assert "created_at" in data


class TestGetByTitleCategory:
    async def test_get_by_title(self, alice_client, alice_category):
        response = await alice_client.get(f"/categories/title/{alice_category.title}")
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        assert data["id"] == str(alice_category.id)
        assert data["title"] == alice_category.title
        assert data["description"] == alice_category.description
        assert data["author_id"] == str(alice_category.author_id)
        assert "created_at" in data

    async def test_get_by_title_nonexistent(self, alice_client, alice_category):
        nonexistent_title = alice_category.title + "aboba"
        response = await alice_client.get(f"/categories/title/{nonexistent_title}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    async def test_get_by_title_unauthorized(self, async_client, alice_category):
        response = await async_client.get(f"/categories/title/{alice_category.title}")
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        assert data["id"] == str(alice_category.id)
        assert data["title"] == alice_category.title
        assert data["description"] == alice_category.description
        assert data["author_id"] == str(alice_category.author_id)
        assert "created_at" in data
