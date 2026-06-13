from src.schemas.posts import PostCreate
from http import HTTPStatus


class TestPostCreate:
    async def test_create(self, alice_client, alice, alice_category):
        post_create = PostCreate(
            title="Alice's Post",
            body="Post Description",
            datetime_to_publish="2000-01-01T00:00:00Z",
            category_id=alice_category.id,
            author_id=alice.id,
        )

        response = await alice_client.post(
            "/posts/create", json=post_create.model_dump(mode="json")
        )
        assert response.status_code == HTTPStatus.CREATED

    async def test_create_duplicate(self, alice_client, alice, alice_post):
        post_create = PostCreate(
            title=alice_post.title,
            body=alice_post.body,
            datetime_to_publish=alice_post.datetime_to_publish,
            category_id=alice_post.category_id,
            author_id=alice.id,
        )

        response = await alice_client.post(
            "/posts/create", json=post_create.model_dump(mode="json")
        )
        assert response.status_code == HTTPStatus.CREATED

    # Проверяет, что можно создать пост только от своего имени и нельзя от чьего либо ещё
    async def test_create_another_account(self, bob_client, alice, alice_category):
        post_create = PostCreate(
            title="Alice's Post",
            body="Post Description",
            datetime_to_publish="2000-01-01T00:00:00Z",
            category_id=alice_category.id,
            author_id=alice.id,
        )

        response = await bob_client.post(
            "/posts/create", json=post_create.model_dump(mode="json")
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

    async def test_create_unauthorized(self, async_client, alice, alice_category):
        post_create = PostCreate(
            title="Alice's Post",
            body="Post Description",
            datetime_to_publish="2000-01-01T00:00:00Z",
            category_id=alice_category.id,
            author_id=alice.id,
        )

        response = await async_client.post(
            "/posts/create", json=post_create.model_dump(mode="json")
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
