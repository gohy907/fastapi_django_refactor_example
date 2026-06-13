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


class TestGetCategory:
    async def test_get_by_id(self, alice_client, alice_category):
        response = await alice_client.get(f"/categories/{alice_category.id}")
        assert response.status_code == HTTPStatus.OK

    async def test_get_by_id_nonexistent(self, alice_client, alice_category):
        nonexistent_id = uuid.UUID(int=alice_category.id.int ^ 1)
        response = await alice_client.get(f"/categories/{nonexistent_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    async def test_get_by_id_unauthorized(self, async_client, alice_category):
        response = await async_client.get(f"/categories/{alice_category.id}")
        assert response.status_code == HTTPStatus.OK
